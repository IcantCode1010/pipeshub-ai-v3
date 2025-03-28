import asyncio
import os
from pydantic import BaseModel
from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional, Dict, Any, List
from app.setups.query_setup import AppContainer
from app.utils.logger import logger
from app.modules.retrieval.retrieval_service import RetrievalService
from app.modules.retrieval.retrieval_arango import ArangoService
from app.utils.query_transform import setup_query_transformation

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

class AzureLLMConfig(BaseModel):
    provider: str
    azure_endpoint: str
    azure_deployment: str
    azure_api_version: str
    api_key: str
    model: str
    temperature: float = 0.3

class LLMFactory:
    @staticmethod
    def create_async_llm(config: AzureLLMConfig):
        """Create an asynchronous LLM instance"""
        if config.provider == "azure":
            from langchain_openai import AzureChatOpenAI
            
            return AzureChatOpenAI(
                azure_endpoint=config.azure_endpoint,
                azure_deployment=config.azure_deployment,
                api_version=config.azure_api_version,
                api_key=config.api_key,
                temperature=config.temperature
            )
        raise ValueError(f"Unsupported provider: {config.provider}")


@router.post("/search")
@inject
async def search(request: Request, body: SearchQuery, 
                retrieval_service: RetrievalService = Depends(get_retrieval_service),
                arango_service: ArangoService = Depends(get_arango_service)):
    """Perform semantic search across documents"""
    try:
        print("orgId is ", request.state.user.get('orgId'))
                # Setup LLM configuration
        llm_config = AzureLLMConfig(
            provider="azure",
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME"),
            azure_api_version=os.getenv("AZURE_API_VERSION"),
            api_key=os.getenv("AZURE_API_KEY"),
            model="gpt-4o",
            temperature=0.3
        )
        # Create async LLM
        llm = LLMFactory.create_async_llm(llm_config)
        
        # Setup query transformation
        rewrite_chain, expansion_chain = await setup_query_transformation(llm)
        
        # Run query transformations in parallel
        rewritten_query, expanded_queries = await asyncio.gather(
            rewrite_chain.ainvoke(body.query),
            expansion_chain.ainvoke(body.query)
        )
        
        logger.info(f"Rewritten query: {rewritten_query}")
        logger.info(f"Expanded queries: {expanded_queries}")
        
        expanded_queries_list = [q.strip() for q in expanded_queries.split('\n') if q.strip()]

        queries = [rewritten_query.strip()] if rewritten_query.strip() else []
        queries.extend([q for q in expanded_queries_list if q not in queries])

        results = await retrieval_service.search_with_filters(
            queries=queries,
            org_id=request.state.user.get('orgId'),
            user_id=request.state.user.get('userId'),
            limit=body.limit,
            filter_groups=body.filters,
            arango_service=arango_service
        )
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
