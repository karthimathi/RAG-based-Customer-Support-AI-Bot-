# RUNNABLE CODE: Main application entry point
import uvicorn
from src.api.endpoints import app
from src.core.config import Config

if __name__ == "__main__":
    # Validate configuration
    Config.validate_config()
    
    print("=" * 60)
    print("Customer Support RAG Bot API")
    print("=" * 60)
    print("\n⚠️  IMPORTANT: This is a portfolio demonstration project")
    print("For GitHub hosting, API keys are placeholders")
    print("\nEndpoints:")
    print("  - POST /ingest    - Upload documents")
    print("  - POST /query     - Ask questions")
    print("  - GET  /health    - Health check")
    print("  - GET  /documents - List ingested documents")
    print("\nTo run locally (with actual services):")
    print("  1. Set environment variables:")
    print("     - PINECONE_API_KEY")
    print("     - LLAMA_API_KEY")
    print("  2. Run: uvicorn src.main:app --reload")
    print("\nFor GitHub portfolio: Code structure and patterns are shown")
    print("=" * 60)
    
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
