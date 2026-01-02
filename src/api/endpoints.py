# RUNNABLE CODE: FastAPI endpoints
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import time

from src.api.schemas import (
    QueryRequest, QueryResponse, 
    IngestionResponse, HealthResponse
)
from src.data.document_loader import DocumentLoader
from src.data.chunking import TextChunker
from src.core.embedding_service import EmbeddingService
from src.vector_store.retrieval import RetrievalService
from src.core.llm_service import LlamaService
from src.core.config import Config

# Initialize services
config = Config()
document_loader = DocumentLoader()
text_chunker = TextChunker(
    chunk_size=config.CHUNK_SIZE,
    chunk_overlap=config.CHUNK_OVERLAP
)
embedding_service = EmbeddingService(config.EMBEDDING_MODEL)
retrieval_service = RetrievalService(config)
llama_service = LlamaService(
    api_key=config.LLAMA_API_KEY,
    api_url=config.LLAMA_API_URL
)

app = FastAPI(
    title="Customer Support RAG Bot API",
    description="Retrieval-Augmented Generation API for customer support",
    version="1.0.0"
)

# In-memory storage for demo (conceptual)
# In production, this would be a database
document_store = []

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        model_loaded=embedding_service.model is not None
    )

@app.post("/ingest", response_model=IngestionResponse)
async def ingest_document(file: UploadFile = File(...)):
    """
    Ingest a document (PDF or TXT) into the vector database.
    
    CONCEPTUAL: For GitHub demo, this simulates the ingestion process.
    In production, this would actually process and store documents.
    """
    start_time = time.time()
    
    # Validate file type
    allowed_types = {"application/pdf", "text/plain", "text/markdown"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Supported: PDF, TXT, MD"
        )
    
    try:
        # Load document
        document_content = document_loader.load_from_bytes(
            file.file, file.filename
        )
        
        # Chunk document
        chunks = text_chunker.chunk_document(document_content)
        
        # Generate embeddings
        embeddings = embedding_service.generate_embeddings(chunks)
        
        # Prepare vectors for Pinecone
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{file.filename}_chunk_{i}"
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": file.filename,
                    "chunk_index": i
                }
            })
        
        # Store in vector database (conceptual)
        # In production: pinecone_service.upsert_vectors(vectors)
        
        # Store metadata locally for demo
        document_store.append({
            "filename": file.filename,
            "chunks": len(chunks),
            "timestamp": time.time()
        })
        
        processing_time = time.time() - start_time
        
        return IngestionResponse(
            document_id=f"doc_{len(document_store)}",
            chunks_created=len(chunks),
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_rag_system(request: QueryRequest):
    """
    Query the RAG system with a customer support question.
    
    RUNNABLE: This demonstrates the complete RAG pipeline.
    """
    start_time = time.time()
    
    try:
        # Step 1: Retrieve relevant context
        context_chunks = retrieval_service.retrieve_relevant_context(
            query=request.question,
            top_k=request.top_k
        )
        
        # Extract text from context chunks
        context_texts = [chunk['text'] for chunk in context_chunks]
        sources = list(set([chunk['source'] for chunk in context_chunks]))
        
        # Step 2: Generate response using LLM
        answer = llama_service.generate_response(
            user_query=request.question,
            context=context_texts
        )
        
        # Calculate confidence (simplified)
        confidence = 0.0
        if context_chunks:
            confidence = sum(chunk['score'] for chunk in context_chunks) / len(context_chunks)
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
            processing_time=processing_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List ingested documents."""
    return {
        "documents": document_store,
        "total": len(document_store)
    }

# CONCEPTUAL: Additional endpoints for production
# @app.delete("/documents/{doc_id}")
# @app.get("/statistics")
# @app.post("/batch_ingest")
