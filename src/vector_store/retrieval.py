# RUNNABLE CODE: Retrieval logic
from typing import List, Dict, Any
from src.core.embedding_service import EmbeddingService
from src.vector_store.pinecone_service import PineconeService

class RetrievalService:
    """Orchestrates the retrieval of relevant document chunks."""
    
    def __init__(self, config):
        self.config = config
        self.embedding_service = EmbeddingService(config.EMBEDDING_MODEL)
        self.pinecone_service = PineconeService(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT,
            index_name=config.PINECONE_INDEX_NAME
        )
    
    def retrieve_relevant_context(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Retrieve relevant document chunks for a query."""
        if top_k is None:
            top_k = self.config.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = self.embedding_service.generate_embeddings([query])[0]
        
        # Query Pinecone for similar vectors
        results = self.pinecone_service.query_vectors(
            query_embedding=query_embedding,
            top_k=top_k
        )
        
        # Extract context from results
        context_chunks = []
        for result in results:
            if 'metadata' in result and 'text' in result['metadata']:
                context_chunks.append({
                    'text': result['metadata']['text'],
                    'source': result['metadata'].get('source', 'unknown'),
                    'score': result.get('score', 0.0)
                })
        
        return context_chunks
