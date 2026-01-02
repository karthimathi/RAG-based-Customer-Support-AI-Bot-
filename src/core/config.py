# CONCEPTUAL: This configuration shows production setup
# For GitHub hosting, these would be environment variables
import os
from typing import Optional

class Config:
    """Configuration manager for the RAG system."""
    
    # API Keys (would be environment variables in production)
    PINECONE_API_KEY: Optional[str] = "pinecone-api-key-here"
    PINECONE_ENVIRONMENT: Optional[str] = "gcp-starter"
    PINECONE_INDEX_NAME: str = "customer-support-rag"
    
    # LLM Configuration
    LLAMA_API_KEY: Optional[str] = "llama-api-key-here"
    LLAMA_API_URL: str = "https://api.llama.ai/v1/chat/completions"
    
    # Embedding Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Retrieval Settings
    TOP_K_RESULTS: int = 3
    
    @classmethod
    def validate_config(cls):
        """Validate all required configurations are set."""
        required_vars = [
            ("PINECONE_API_KEY", cls.PINECONE_API_KEY),
            ("LLAMA_API_KEY", cls.LLAMA_API_KEY)
        ]
        
        for var_name, value in required_vars:
            if not value or "here" in value:
                print(f"⚠️  {var_name} not set - some features will not work")
        
        return True

# CONCEPTUAL: In production, use environment variables
# import os
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
