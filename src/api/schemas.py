# RUNNABLE CODE: Pydantic schemas for API
from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentUpload(BaseModel):
    """Schema for document upload."""
    filename: str = Field(..., description="Name of the document")
    content_type: str = Field(..., description="MIME type of the document")

class QueryRequest(BaseModel):
    """Schema for user query."""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")
    top_k: Optional[int] = Field(3, ge=1, le=10, description="Number of results to retrieve")

class QueryResponse(BaseModel):
    """Schema for query response."""
    answer: str = Field(..., description="Generated answer")
    sources: List[str] = Field(..., description="Source documents used")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Time taken in seconds")

class IngestionResponse(BaseModel):
    """Schema for ingestion response."""
    document_id: str = Field(..., description="Unique document identifier")
    chunks_created: int = Field(..., description="Number of text chunks created")
    status: str = Field(..., description="Ingestion status")

class HealthResponse(BaseModel):
    """Schema for health check."""
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether models are loaded")
