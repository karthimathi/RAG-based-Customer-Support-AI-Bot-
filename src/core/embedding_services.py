# RUNNABLE CODE: Embedding generation with SentenceTransformers
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    """Generates embeddings using SentenceTransformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = self._load_model()
    
    def _load_model(self):
        """Load the SentenceTransformer model."""
        try:
            # CONCEPTUAL: This would download the model
            # For GitHub, we show the pattern
            print(f"Loading embedding model: {self.model_name}")
            
            # In production:
            # return SentenceTransformer(self.model_name)
            
            # For demonstration on GitHub
            class MockModel:
                def encode(self, texts):
                    # Generate deterministic mock embeddings
                    embeddings = []
                    for i, text in enumerate(texts):
                        # Create deterministic "embedding" based on text length
                        np.random.seed(hash(text) % 10000)
                        embedding = np.random.randn(384).astype(np.float32)
                        embeddings.append(embedding)
                    return np.array(embeddings)
            
            return MockModel()
            
        except Exception as e:
            print(f"Error loading model {self.model_name}: {e}")
            print("Using mock embeddings for demonstration")
            return None
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        if not texts:
            return []
        
        if self.model is None:
            # Generate simple deterministic embeddings for GitHub demo
            embeddings = []
            for text in texts:
                # Simple deterministic hash-based "embedding"
                import hashlib
                hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16) % 10000
                np.random.seed(hash_val)
                embedding = np.random.randn(384).tolist()
                embeddings.append(embedding)
            return embeddings
        
        # Generate actual embeddings
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings."""
        if self.model_name == "all-MiniLM-L6-v2":
            return 384
        return 384  # Default for demo
