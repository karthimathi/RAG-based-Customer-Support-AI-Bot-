# RUNNABLE CODE: Text chunking implementation
from typing import List
import re

class TextChunker:
    """Splits documents into manageable chunks for embedding."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
    def chunk_document(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        if not text.strip():
            return []
        
        # Split by paragraphs first
        paragraphs = self._split_by_paragraphs(text)
        
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap
                current_chunk = self._get_overlap(current_chunk) + paragraph + " "
            else:
                current_chunk += paragraph + " "
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # If any chunks are still too large, split by sentences
        final_chunks = []
        for chunk in chunks:
            if len(chunk) > self.chunk_size * 1.5:
                final_chunks.extend(self._split_by_sentences(chunk))
            else:
                final_chunks.append(chunk)
        
        return final_chunks
    
    def _split_by_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs."""
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _split_by_sentences(self, text: str) -> List[str]:
        """Split text by sentences (fallback for long paragraphs)."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence + " "
                else:
                    # Single sentence is longer than chunk size
                    chunks.append(sentence[:self.chunk_size])
                    current_chunk = sentence[self.chunk_size:] + " "
            else:
                current_chunk += sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _get_overlap(self, chunk: str) -> str:
        """Get overlapping text from the end of a chunk."""
        if not chunk or len(chunk) <= self.chunk_overlap:
            return ""
        
        # Get last chunk_overlap characters
        overlap_text = chunk[-self.chunk_overlap:]
        
        # Try to end at a sentence boundary
        last_period = overlap_text.rfind('. ')
        if last_period != -1:
            return overlap_text[last_period + 2:] + " "
        
        last_space = overlap_text.rfind(' ')
        if last_space != -1:
            return overlap_text[last_space + 1:] + " "
        
        return overlap_text + " "
