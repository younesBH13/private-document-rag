import pytest
import os
import tempfile
from core.document_loader import UniversalDocumentLoader
from core.text_splitter import DocumentChunker

def test_text_file_loading_and_chunking():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_file:
        temp_file.write("PrivateDoc RAG is an offline AI assistant. " * 50)
        temp_path = temp_file.name

    try:
        # Test loader
        docs = UniversalDocumentLoader.load_file(temp_path, original_filename="test.txt")
        assert len(docs) > 0
        assert docs[0].metadata["source_name"] == "test.txt"
        assert docs[0].metadata["file_type"] == "TXT"
        
        # Test chunker
        chunker = DocumentChunker(chunk_size=200, chunk_overlap=50)
        chunks = chunker.split_documents(docs)
        assert len(chunks) > 1
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_unsupported_file_extension():
    with pytest.raises(ValueError):
        UniversalDocumentLoader.load_file("test.exe")
