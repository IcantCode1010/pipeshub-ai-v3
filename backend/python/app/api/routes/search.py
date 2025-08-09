import asyncio
from typing import Any, Dict, List, Optional

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.config.configuration_service import ConfigurationService
from app.modules.retrieval.retrieval_arango import ArangoService
from app.modules.retrieval.retrieval_service import RetrievalService
from app.setups.query_setup import AppContainer
from app.utils.query_transform import setup_query_transformation
from app.utils.aircraft_normalizer import normalize_aircraft
import time

router = APIRouter()


# Pydantic models
class SearchQuery(BaseModel):
    query: str
    limit: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = {}


class SimilarDocumentQuery(BaseModel):
    document_id: str
    limit: Optional[int] = 5
    filters: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    query: str
    topK: int = 20
    filtersV1: List[Dict[str, List[str]]]


async def get_retrieval_service(request: Request) -> RetrievalService:
    container: AppContainer = request.app.container
    retrieval_service = await container.retrieval_service()
    return retrieval_service


async def get_arango_service(request: Request) -> ArangoService:
    container: AppContainer = request.app.container
    arango_service = await container.arango_service()
    return arango_service


async def get_config_service(request: Request) -> ConfigurationService:
    container: AppContainer = request.app.container
    config_service = container.config_service()
    return config_service


@router.post("/search")
@inject
async def search(
    request: Request,
    body: SearchQuery,
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    arango_service: ArangoService = Depends(get_arango_service),
):
    """Perform semantic search across documents"""
    try:
        container = request.app.container
        logger = container.logger()
        llm = retrieval_service.llm
        if llm is None:
            llm = await retrieval_service.get_llm_instance()
            if llm is None:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to initialize LLM service. LLM configuration is missing.",
                )

        # Aircraft scoping headers and behavior
        client = (request.headers.get("x-client") or "generic_rag").lower()
        strict_scope = (request.headers.get("x-strict-scope", "").lower() in ("1", "true", "yes"))

        # Prefer header x-aircraft; fallback to body.filters.aircraft[0] if present
        aircraft_input = request.headers.get("x-aircraft")
        try:
            if (not aircraft_input) and body.filters and isinstance(body.filters.get("aircraft"), list) and body.filters["aircraft"]:
                aircraft_input = body.filters["aircraft"][0]
        except Exception:
            pass

        # Enforce strict scoping for efb_ai when requested
        if client == "efb_ai" and strict_scope and not aircraft_input:
            raise HTTPException(status_code=400, detail="Select aircraft")

        # Normalize to canonical; do not prefilter on 'unknown'
        aircraft_canonical = None
        if aircraft_input:
            canonical_candidate, _aliases = normalize_aircraft(aircraft_input)
            if canonical_candidate != "unknown":
                aircraft_canonical = canonical_candidate

        # Setup query transformation
        rewrite_chain, expansion_chain = setup_query_transformation(llm)

        # Run query transformations in parallel
        rewritten_query, expanded_queries = await asyncio.gather(
            rewrite_chain.ainvoke(body.query), expansion_chain.ainvoke(body.query)
        )

        logger.debug(f"Rewritten query: {rewritten_query}")
        logger.debug(f"Expanded queries: {expanded_queries}")

        expanded_queries_list = [
            q.strip() for q in expanded_queries.split("\n") if q.strip()
        ]

        queries = [rewritten_query.strip()] if rewritten_query.strip() else []
        queries.extend([q for q in expanded_queries_list if q not in queries])

        start_ts = time.monotonic()
        results = await retrieval_service.search_with_filters(
            queries=queries,
            org_id=request.state.user.get("orgId"),
            user_id=request.state.user.get("userId"),
            limit=body.limit,
            filter_groups=body.filters,
            aircraft_canonical=aircraft_canonical,
            arango_service=arango_service,
        )
        latency = time.monotonic() - start_ts
        candidate_count = len((results or {}).get("searchResults", []) or [])
        logger.info(
            f"[retrieval] client={client} aircraft={aircraft_canonical or 'null'} "
            f"collection={getattr(retrieval_service, 'collection_name', 'unknown')} "
            f"candidates={candidate_count} latency={latency:.3f}s"
        )
        custom_status_code = results.get("status_code", 500)
        logger.info(f"Custom status code: {custom_status_code}")
        logger.info(f"Results: {results}")

        return JSONResponse(status_code=custom_status_code, content=results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
