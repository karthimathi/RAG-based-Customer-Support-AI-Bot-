# RUNNABLE CODE: Document processing functionality
from typing import List, Union, BinaryIO
import tempfile
from pathlib import Path

class DocumentLoader:
    """Handles loading and preprocessing of company documents."""
    
    def __init__(self):
        self.supported_extensions = {'.pdf', '.txt', '.md'}
    
    def load_document(self, file_path: Union[str, Path]) -> str:
        """Load document content from file path."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        if path.suffix not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        
        # Text files
        if path.suffix == '.txt':
            return self._load_text_file(path)
        elif path.suffix == '.md':
            return self._load_text_file(path)
        # PDF files
        elif path.suffix == '.pdf':
            return self._load_pdf_file(path)
    
    def _load_text_file(self, path: Path) -> str:
        """Load content from text-based files."""
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def _load_pdf_file(self, path: Path) -> str:
        """Extract text from PDF files."""
        try:
            # CONCEPTUAL: In production, use PyPDF2 or similar
            # This demonstrates the approach
            print(f"Loading PDF: {path.name}")
            # Simulated PDF text extraction
            return f"Extracted text from PDF: {path.name}"
            
            # Actual implementation would be:
            # from pypdf import PdfReader
            # reader = PdfReader(path)
            # text = ""
            # for page in reader.pages:
            #     text += page.extract_text()
            # return text
        except Exception as e:
            raise Exception(f"Error reading PDF {path}: {str(e)}")
    
    def load_from_bytes(self, file_bytes: BinaryIO, filename: str) -> str:
        """Load document from bytes (for API uploads)."""
        with tempfile.NamedTemporaryFile(suffix=Path(filename).suffix, delete=False) as tmp:
            tmp.write(file_bytes.read())
            tmp_path = tmp.name
        
        try:
            content = self.load_document(tmp_path)
        finally:
            Path(tmp_path).unlink()
        
        return content
