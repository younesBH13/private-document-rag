import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader
)

class UniversalDocumentLoader:
    """Loads various document formats and enriches metadata with source info."""
    
    SUPPORTED_EXTENSIONS = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".txt": TextLoader,
        ".csv": CSVLoader,
        ".md": TextLoader
    }
    
    @classmethod
    def load_file(cls, file_path: str, original_filename: str = None) -> List[Document]:
        """Loads a single file using the appropriate loader based on extension."""
        _, ext = os.path.splitext(file_path.lower())
        
        if ext not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{ext}'. Supported: {list(cls.SUPPORTED_EXTENSIONS.keys())}")
            
        loader_cls = cls.SUPPORTED_EXTENSIONS[ext]
        try:
            loader = loader_cls(file_path)
            documents = loader.load()
            
            # Standardize and enhance metadata
            for doc in documents:
                doc.metadata["source_name"] = original_filename or os.path.basename(file_path)
                doc.metadata["file_type"] = ext.replace(".", "").upper()
                if "page" not in doc.metadata:
                    doc.metadata["page"] = 1
                else:
                    # PyPDFLoader is 0-indexed, let's normalize to 1-indexed for human readability
                    if isinstance(doc.metadata["page"], int):
                        doc.metadata["page"] = doc.metadata["page"] + 1
                        
            return documents
        except Exception as e:
            raise RuntimeError(f"Error reading {original_filename or file_path}: {str(e)}")
