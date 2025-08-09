import asyncio
import time
from typing import Any, Dict, List, Optional

from langchain.chat_models.base import BaseChatModel
from langchain.embeddings.base import Embeddings
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.http.models import FieldCondition, Filter, MatchValue

from app.config.configuration_service import config_node_constants
from app.config.utils.named_constants.ai_models_named_constants import (
    DEFAULT_EMBEDDING_MODEL,
)
from app.config.utils.named_constants.arangodb_constants import (
    CollectionNames,
    Connectors,
    RecordTypes,
)
from app.exceptions.embedding_exceptions import EmbeddingModelCreationError
from app.exceptions.fastapi_responses import Status
from app.exceptions.indexing_exceptions import IndexingError
from app.modules.retrieval.retrieval_arango import ArangoService
from app.utils.aimodels import (
    get_default_embedding_model,
    get_embedding_model,
    get_generator_model,
)


class RetrievalService:
    def __init__(
        self,
        logger,
        config_service,
        collection_name: str,
        qdrant_client: QdrantClient,
    ) -> None:
        """
        Initialize the retrieval service with necessary configurations.

        Args:
            collection_name: Name of the Qdrant collection
            qdrant_api_key: API key for Qdrant
            qdrant_host: Qdrant server host URL
        """

        self.logger = logger
        self.config_service = config_service
        self.llm = None

        # Initialize sparse embeddings
        try:
            self.sparse_embeddings = FastEmbedSparse(model_name="Qdrant/BM25")
        except Exception as e:
            self.logger.error("Failed to initialize sparse embeddings: " + str(e))
            self.sparse_embeddings = None
            raise Exception(
                "Failed to initialize sparse embeddings: " + str(e),
            )
        self.qdrant_client = qdrant_client
        self.collection_name = collection_name
        self.logger.info(f"Retrieval service initialized with collection name: {self.collection_name}")
        self.vector_store = None

    async def get_llm_instance(self) -> Optional[BaseChatModel]:
        try:
            self.logger.info("Getting LLM")
            ai_models = await self.config_service.get_config(
                config_node_constants.AI_MODELS.value
            )
            llm_configs = ai_models["llm"]

            # For now, we'll use the first available provider that matches our supported types
            # We will add logic to choose a specific provider based on our needs

            for config in llm_configs:
                provider = config["provider"]
                self.llm = get_generator_model(provider, config)
                if self.llm:
                    break
            if not self.llm:
                raise ValueError("No supported LLM provider found in configuration")

            self.logger.info("LLM created successfully")
            return self.llm
        except Exception as e:
            self.logger.error(f"Error getting LLM: {str(e)}")
            return None

    async def get_embedding_model_instance(self) -> Optional[Embeddings]:
        try:
            self.logger.info("Getting embedding model")
            embedding_model = await self.get_current_embedding_model_name()
            try:
                if not embedding_model or embedding_model == DEFAULT_EMBEDDING_MODEL:
                    self.logger.info("Using default embedding model")
                    embedding_model = DEFAULT_EMBEDDING_MODEL
                    dense_embeddings = get_default_embedding_model()
                else:
                    self.logger.info(f"Using embedding model: {getattr(embedding_model, 'model', embedding_model)}")
                    ai_models = await self.config_service.get_config(
                        config_node_constants.AI_MODELS.value
                    )
                    dense_embeddings = None
                    if ai_models["embedding"]:
                        config = ai_models["embedding"][0]
                        dense_embeddings = get_embedding_model(config["provider"], config)

            except Exception as e:
                self.logger.error(f"Error creating embedding model: {str(e)}")
                raise EmbeddingModelCreationError(
                    f"Failed to create embedding model: {str(e)}"
                ) from e

            # Get the embedding dimensions from the model
            try:
                sample_embedding = await dense_embeddings.aembed_query("test")
                embedding_size = len(sample_embedding)
            except Exception as e:
                self.logger.warning(
                    f"Error with configured embedding model: {str(e)}"
                )
                raise IndexingError(
                    "Failed to get embedding model: " + str(e),
                )

            self.logger.info(
                f"Using embedding model: {getattr(embedding_model, 'model', embedding_model)}, embedding_size: {embedding_size}"
            )
            return dense_embeddings
        except Exception as e:
            self.logger.error(f"Error getting embedding model: {str(e)}")
            return None

    async def get_current_embedding_model_name(self) -> Optional[str]:
        """Get the current embedding model name from configuration or instance."""
        try:
            # First try to get from AI_MODELS config
            ai_models = await self.config_service.get_config(
                config_node_constants.AI_MODELS.value
            )
            if ai_models and "embedding" in ai_models and ai_models["embedding"]:
                for config in ai_models["embedding"]:
                    # Only one embedding model is supported
                    if "configuration" in config and "model" in config["configuration"]:
                        return config["configuration"]["model"]

            # Return default model if no embedding config found
            return DEFAULT_EMBEDDING_MODEL
        except Exception as e:
            self.logger.error(f"Error getting current embedding model name: {str(e)}")
            return DEFAULT_EMBEDDING_MODEL

    def get_embedding_model_name(self, dense_embeddings: Embeddings) -> Optional[str]:
        if hasattr(dense_embeddings, "model_name"):
            return dense_embeddings.model_name
        elif hasattr(dense_embeddings, "model"):
            return dense_embeddings.model
        else:
            return None

    async def _preprocess_query(self, query: str) -> str:
        """
        Preprocess the query text.

        Args:
            query: Raw query text

        Returns:
            Preprocessed query text
        """
        try:
            # Get current model name from config
            model_name = await self.get_current_embedding_model_name()

            # Check if using BGE model before adding the prefix
            if model_name and "bge" in model_name.lower():
                return f"Represent this document for retrieval: {query.strip()}"
            return query.strip()
        except Exception as e:
            self.logger.error(f"Error in query preprocessing: {str(e)}")
            return query.strip()

    def _format_results(self, results: List[tuple]) -> List[Dict[str, Any]]:
        """Format search results into a consistent structure with flattened metadata."""
        formatted_results = []
        for doc, score in results:
            formatted_result = {
                "content": doc.page_content,
                "score": float(score),
                "citationType": "vectordb|document",
                "metadata": doc.metadata,
            }
            formatted_results.append(formatted_result)
        return formatted_results

    def _build_qdrant_filter(
        self,
        org_id: str,
        accessible_virtual_record_ids: List[str],
        aircraft_canonical: Optional[str] = None,
    ) -> Filter:
        """
        Build Qdrant filter for accessible records with both org_id and record_id conditions,
        and optional aircraft scoping.

        Args:
            org_id: Organization ID to filter
            accessible_virtual_record_ids: List of virtual record IDs the user has access to
            aircraft_canonical: Optional canonical aircraft code to scope results

        Returns:
            Qdrant Filter object
        """
        must_conditions = [
            FieldCondition(  # org_id condition
                key="metadata.orgId", match=MatchValue(value=org_id)
            ),
            Filter(  # recordId must be one of the accessible_records
                should=[
                    FieldCondition(
                        key="metadata.virtualRecordId", match=MatchValue(value=virtual_record_id)
                    )
                    for virtual_record_id in accessible_virtual_record_ids
                ]
            ),
        ]
        if aircraft_canonical:
            must_conditions.append(
                FieldCondition(
                    key="aircraft_canonical", match=MatchValue(value=aircraft_canonical)
                )
            )
        return Filter(must=must_conditions)

    async def search_with_filters(
        self,
        queries: List[str],
        user_id: str,
        org_id: str,
        filter_groups: Optional[Dict[str, List[str]]] = None,
        limit: int = 20,
        aircraft_canonical: Optional[str] = None,
        arango_service: Optional[ArangoService] = None,
    ) -> List[Dict[str, Any]]:
        """Perform semantic search on accessible records with multiple queries."""

        try:
            # Get accessible records
            if not arango_service:
                raise ValueError("ArangoService is required for permission checking")

            filter_groups = filter_groups or {}

            # Convert filter_groups to format expected by get_accessible_records
            arango_filters = {}
            if filter_groups:  # Only process if filter_groups is not empty
                for key, values in filter_groups.items():
                    # Convert key to match collection naming
                    metadata_key = (
                        key.lower()
                    )  # e.g., 'departments', 'categories', etc.
                    arango_filters[metadata_key] = values


            self.logger.info("Starting parallel initialization tasks")
            init_tasks = [
                self._get_accessible_records_task(user_id, org_id, filter_groups, arango_service),
                self._get_vector_store_task(),
                arango_service.get_user_by_user_id(user_id)  # Get user info in parallel
            ]

            self.logger.info("Executing parallel tasks")
            accessible_records, vector_store, user = await asyncio.gather(*init_tasks)
            self.logger.info(f"Parallel tasks completed. Records: {len(accessible_records) if accessible_records else 0}, User: {user is not None}")

            # Clean filter: Remove any None records immediately after reading from ArangoDB
            accessible_records = [r for r in accessible_records if r]

            # Add null checking for user
            if not user:
                self.logger.warning(f"User not found for user_id: {user_id}")
                user = {"email": ""}  # Provide default empty user

            if not accessible_records:
                return self._create_empty_response("No accessible records found for this user with provided filters.")

            # Collect accessible virtualRecordIds safely
            accessible_virtual_record_ids = []
            for record in accessible_records:
                if not record:
                    continue
                virtual_id = record.get("virtualRecordId")
                if virtual_id is not None:
                    accessible_virtual_record_ids.append(virtual_id)
            # Build Qdrant filter (with optional aircraft constraint)
            qdrant_filter =  self._build_qdrant_filter(
                org_id,
                accessible_virtual_record_ids,
                aircraft_canonical=aircraft_canonical
            )

            search_results = await self._execute_parallel_searches(queries, qdrant_filter, limit, vector_store)

            # Defensive post-filter: drop any hit that explicitly declares a mismatching aircraft_canonical
            # Keep results that do not have aircraft_canonical in metadata (backfilled points may only have root-level field)
            if aircraft_canonical:
                before_count = len(search_results or [])
                def _keep(r):
                    meta = (r.get("metadata") or {})
                    val = meta.get("aircraft_canonical")
                    # If field absent/empty in metadata, keep it; only drop explicit mismatches
                    return (val is None or val == "" or val == aircraft_canonical)
                search_results = [r for r in (search_results or []) if _keep(r)]
                after_count = len(search_results)
                self.logger.debug(
                    f"Post-filter by aircraft_canonical='{aircraft_canonical}': {before_count} -> {after_count}"
                )

            if not search_results:
                return self._create_empty_response("No search results found")


            # Collect virtualRecordIds safely from search results
            virtual_record_ids_set = set()
            for result in search_results:
                metadata = result.get("metadata") if result else None
                if metadata and metadata.get("virtualRecordId"):
                    virtual_record_ids_set.add(metadata["virtualRecordId"])
            virtual_record_ids = list(virtual_record_ids_set)
            virtual_to_record_map = self._create_virtual_to_record_mapping(accessible_records, virtual_record_ids)
            unique_record_ids = set(virtual_to_record_map.values())

            if not unique_record_ids:
                return self._create_empty_response("No accessible records found for this user with provided filters.")

            # Replace virtualRecordId with first accessible record ID in search results
            for result in search_results:
                if not result or not result.get("metadata"):
                    continue
                virtual_id = result["metadata"].get("virtualRecordId")
                if virtual_id and virtual_id in virtual_to_record_map:
                    record_id = virtual_to_record_map[virtual_id]
                    result["metadata"]["recordId"] = record_id
                    record = next((r for r in accessible_records if r["_key"] == record_id), None)
                    if record:
                        result["metadata"]["origin"] = record.get("origin")
                        result["metadata"]["connector"] = record.get("connectorName")
                        weburl = record.get("webUrl")
                        if weburl and weburl.startswith("https://mail.google.com/mail?authuser="):
                            weburl = weburl.replace("{user.email}", user["email"])
                        result["metadata"]["webUrl"] = weburl

                        if not weburl and record.get("recordType", "") == RecordTypes.FILE.value:
                            files = await arango_service.get_document(
                                record_id, CollectionNames.FILES.value
                            )
                            if files:  # Add null check
                                weburl = files.get("webUrl")
                                if weburl and record.get("connectorName", "") == Connectors.GOOGLE_MAIL.value:
                                    weburl = weburl.replace("{user.email}", user["email"])
                            result["metadata"]["webUrl"] = weburl

                        if not weburl and record.get("recordType", "") == RecordTypes.MAIL.value:
                            mail = await arango_service.get_document(
                                record_id, CollectionNames.MAILS.value
                            )
                            if mail:  # Add null check
                                weburl = mail.get("webUrl")
                                if weburl and weburl.startswith("https://mail.google.com/mail?authuser="):
                                    weburl = weburl.replace("{user.email}", user["email"])
                            result["metadata"]["webUrl"] = weburl

            # Get full record documents from Arango
            records = []
            if unique_record_ids:
                for record_id in unique_record_ids:
                    record = next((r for r in accessible_records if r["_key"] == record_id), None)
                    # Only append non-None records
                    if record:
                        records.append(record)

            if search_results or records:
                return {
                    "searchResults": search_results,
                    "records": records,
                    "status": Status.SUCCESS.value,
                    "status_code": 200,
                    "message": "Query processed successfully. Relevant records retrieved.",
                }
            else:
                return {
                    "searchResults": [],
                    "records": [],
                    "status": Status.EMPTY_RESPONSE.value,
                    "status_code": 200,
                    "message": "Query processed, but no relevant results were found.",
                }

        except Exception as e:
            self.logger.error(f"Filtered search failed: {str(e)}")
            # Add more detailed error logging
            try:
                import traceback
                self.logger.error(f"Full traceback: {traceback.format_exc()}")
            except Exception as trace_error:
                self.logger.error(f"Error getting traceback: {str(trace_error)}")
            
            return {
                "searchResults": [],
                "records": [],
                "status": Status.ERROR.value,
                "status_code": 500,
                "message": f"An error occurred during search: {str(e)}",
            }


    async def _get_accessible_records_task(self, user_id, org_id, filter_groups, arango_service) -> List[Dict[str, Any]]:
        """Separate task for getting accessible records"""
        filter_groups = filter_groups or {}
        arango_filters = {}

        if filter_groups:
            for key, values in filter_groups.items():
                metadata_key = key.lower()
                arango_filters[metadata_key] = values

        return await arango_service.get_accessible_records(
            user_id=user_id, org_id=org_id, filters=arango_filters
        )


    async def _get_vector_store_task(self) -> QdrantVectorStore:
        """Cached vector store retrieval"""
        if not self.vector_store:
            # Check collection exists
            try:
                collections = self.qdrant_client.get_collections()
                collection_exists = any(col.name == self.collection_name for col in collections.collections)
                
                if not collection_exists:
                    raise ValueError(f"Collection '{self.collection_name}' not found in Qdrant")
                
                collection_info = self.qdrant_client.get_collection(self.collection_name)
                
                if not collection_info:
                    raise ValueError(f"Could not retrieve collection info for '{self.collection_name}'")
                
                if hasattr(collection_info, 'points_count') and collection_info.points_count == 0:
                    self.logger.warning(f"Collection '{self.collection_name}' exists but has no points")
                    # Don't raise error, allow empty collection for now
                
            except Exception as e:
                self.logger.error(f"Error checking Qdrant collection: {str(e)}")
                raise ValueError(f"Vector DB collection check failed: {str(e)}")

            # Get cached embedding model
            dense_embeddings = await self.get_embedding_model_instance()
            if not dense_embeddings:
                raise ValueError("No dense embeddings found")

            self.vector_store = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.collection_name,
                vector_name="dense",
                sparse_vector_name="sparse",
                embedding=dense_embeddings,
                sparse_embedding=self.sparse_embeddings,
                retrieval_mode=RetrievalMode.HYBRID,
            )

        return self.vector_store


    async def _execute_parallel_searches(self, queries, qdrant_filter, limit, vector_store) -> List[Dict[str, Any]]:
        """Execute all searches in parallel"""
        all_results = []
        seen_chunks = set()

        # Process all queries in parallel
        search_tasks = [
            vector_store.asimilarity_search_with_score(
                query=await self._preprocess_query(query),
                k=limit,
                filter=qdrant_filter
            )
            for query in queries
        ]

        start_time = time.monotonic()
        search_results = await asyncio.gather(*search_tasks)
        elapsed = time.monotonic() - start_time
        self.logger.debug(f"VectorDB lookup for {len(queries)} queries took {elapsed:.3f} seconds.")

        # Deduplicate results with null checking
        for results in search_results:
            if results is None:
                self.logger.warning("Search results returned None, skipping")
                continue
            for doc, score in results:
                if doc is None or not hasattr(doc, 'page_content'):
                    self.logger.warning("Document is None or missing page_content, skipping")
                    continue
                if doc.page_content not in seen_chunks:
                    all_results.append((doc, score))
                    seen_chunks.add(doc.page_content)

        return self._format_results(all_results)


    def _create_empty_response(self, message: str) -> Dict[str, Any]:
        """Helper to create empty response"""
        return {
            "searchResults": [],
            "records": [],
            "status": Status.ACCESSIBLE_RECORDS_NOT_FOUND.value,
            "status_code": 200,
            "message": message,
        }


    def _create_virtual_to_record_mapping(
        self,
        accessible_records: List[Dict[str, Any]],
        virtual_record_ids: List[str]
    ) -> Dict[str, str]:
        """
        Create virtual record ID to record ID mapping from already fetched accessible_records.
        This eliminates the need for an additional database query.
        Args:
            accessible_records: List of accessible record documents (already fetched)
            virtual_record_ids: List of virtual record IDs from search results
        Returns:
            Dict[str, str]: Mapping of virtual_record_id -> first accessible record_id
        """
        # Create a mapping from virtualRecordId to list of record IDs
        virtual_to_records = {}
        for record in accessible_records:
            # Skip None or empty records to prevent AttributeError
            if not record:
                continue
            
            virtual_id = record.get("virtualRecordId")
            record_id = record.get("_key")

            if virtual_id and record_id:
                if virtual_id not in virtual_to_records:
                    virtual_to_records[virtual_id] = []
                virtual_to_records[virtual_id].append(record_id)

        # Create the final mapping using only the virtual record IDs from search results
        # Use the first record ID for each virtual record ID
        mapping = {}
        for virtual_id in virtual_record_ids:
            if virtual_id in virtual_to_records and virtual_to_records[virtual_id]:
                mapping[virtual_id] = virtual_to_records[virtual_id][0]  # Use first record

        return mapping
