"""
PrivateDoc RAG — Unit Test Suite
Run with: pytest tests/ -v
"""

import pytest
import os
import tempfile
from unittest.mock import MagicMock, patch

from core.document_loader import UniversalDocumentLoader
from core.text_splitter import DocumentChunker
from langchain_core.documents import Document


# ─────────────────────────────────────────────────────────────────────────────
# Document Loader Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestUniversalDocumentLoader:

    def test_txt_file_loads_correctly(self):
        """TXT files should load and carry correct metadata."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("PrivateDoc RAG is an offline AI assistant for confidential documents. " * 20)
            temp_path = f.name
        try:
            docs = UniversalDocumentLoader.load_file(temp_path, original_filename="sample.txt")
            assert len(docs) > 0
            assert docs[0].metadata["source_name"] == "sample.txt"
            assert docs[0].metadata["file_type"] == "TXT"
            assert "page" in docs[0].metadata
        finally:
            os.remove(temp_path)

    def test_md_file_loads_correctly(self):
        """Markdown files should load via TextLoader."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".md", encoding="utf-8") as f:
            f.write("# Test\n\nThis is a markdown document for testing. " * 10)
            temp_path = f.name
        try:
            docs = UniversalDocumentLoader.load_file(temp_path, original_filename="doc.md")
            assert len(docs) > 0
            assert docs[0].metadata["file_type"] == "MD"
        finally:
            os.remove(temp_path)

    def test_unsupported_extension_raises_value_error(self):
        """Unsupported file formats should raise ValueError immediately."""
        with pytest.raises(ValueError, match="Unsupported file format"):
            UniversalDocumentLoader.load_file("malicious.exe")

    def test_missing_file_raises_runtime_error(self):
        """Non-existent file path should raise RuntimeError."""
        with pytest.raises(RuntimeError):
            UniversalDocumentLoader.load_file("/nonexistent/path/file.txt", original_filename="file.txt")

    def test_page_metadata_defaults_to_1_for_txt(self):
        """Non-PDF docs without a page field should default to page 1."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt", encoding="utf-8") as f:
            f.write("Hello world test content.")
            temp_path = f.name
        try:
            docs = UniversalDocumentLoader.load_file(temp_path, original_filename="hello.txt")
            assert docs[0].metadata["page"] == 1
        finally:
            os.remove(temp_path)


# ─────────────────────────────────────────────────────────────────────────────
# Document Chunker Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestDocumentChunker:

    def _make_doc(self, content: str) -> Document:
        return Document(page_content=content, metadata={"source_name": "test.txt", "page": 1})

    def test_single_short_doc_produces_at_least_one_chunk(self):
        chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
        docs = [self._make_doc("This is a short document.")]
        chunks = chunker.split_documents(docs)
        assert len(chunks) >= 1

    def test_long_doc_produces_multiple_chunks(self):
        chunker = DocumentChunker(chunk_size=200, chunk_overlap=20)
        content = "The quick brown fox jumps over the lazy dog. " * 100
        docs = [self._make_doc(content)]
        chunks = chunker.split_documents(docs)
        assert len(chunks) > 1

    def test_empty_document_list_returns_empty(self):
        chunker = DocumentChunker()
        assert chunker.split_documents([]) == []

    def test_chunk_size_respected(self):
        """No chunk should significantly exceed the target chunk size."""
        chunk_size = 300
        chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=30)
        content = "Word " * 500
        chunks = chunker.split_documents([self._make_doc(content)])
        # Allow 10% buffer for splitter boundary decisions
        for chunk in chunks:
            assert len(chunk.page_content) <= chunk_size * 1.1

    def test_metadata_preserved_across_chunks(self):
        chunker = DocumentChunker(chunk_size=100, chunk_overlap=10)
        docs = [self._make_doc("Hello world test content. " * 50)]
        docs[0].metadata["source_name"] = "my_doc.pdf"
        chunks = chunker.split_documents(docs)
        for chunk in chunks:
            assert chunk.metadata.get("source_name") == "my_doc.pdf"


# ─────────────────────────────────────────────────────────────────────────────
# Config Tests
# ─────────────────────────────────────────────────────────────────────────────

class TestConfig:

    def test_config_defaults_are_valid(self):
        from config import config
        assert config.DEFAULT_CHUNK_SIZE >= config.MIN_CHUNK_SIZE
        assert config.DEFAULT_CHUNK_SIZE <= config.MAX_CHUNK_SIZE
        assert 0.0 <= config.TEMPERATURE <= 1.0
        assert config.TOP_K_RETRIEVAL >= 1
        assert config.MEMORY_WINDOW >= 1

    def test_available_llms_is_non_empty(self):
        from config import config
        assert len(config.AVAILABLE_LLMS) > 0

    def test_available_embeddings_is_non_empty(self):
        from config import config
        assert len(config.AVAILABLE_EMBEDDINGS) > 0


# ─────────────────────────────────────────────────────────────────────────────
# RAG Engine Tests (mocked — no Ollama required)
# ─────────────────────────────────────────────────────────────────────────────

class TestRAGEngine:

    @patch("core.rag_engine.Ollama")
    @patch("core.rag_engine.ConversationalRetrievalChain")
    def test_answer_query_raises_without_vectorstore(self, mock_chain, mock_ollama):
        """Should raise ValueError if no vector store is available."""
        from core.rag_engine import RAGEngine

        mock_vm = MagicMock()
        mock_vm.get_vectorstore.return_value = None  # no index

        engine = RAGEngine(model_name="llama3.1:8b")
        with pytest.raises(ValueError, match="No indexed knowledge base"):
            engine.answer_query("What is RAG?", mock_vm)

    @patch("core.rag_engine.Ollama")
    @patch("core.rag_engine.ConversationalRetrievalChain")
    def test_clear_memory_does_not_raise(self, mock_chain, mock_ollama):
        """Memory clear should not throw exceptions."""
        from core.rag_engine import RAGEngine
        engine = RAGEngine()
        engine.clear_memory()  # should not raise
