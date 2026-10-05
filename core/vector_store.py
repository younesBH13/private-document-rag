import os
import shutil
from typing import List, Optional
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

class VectorStoreManager:
    """Manages persistent embeddings and Chroma vector database operations."""
    
    def __init__(self, persist_directory: str = "./chroma_db", embedding_model: str = "nomic-embed-text"):
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.embeddings = OllamaEmbeddings(model=embedding_model)

    def create_or_update_index(self, documents: List[Document]) -> Chroma:
        """Indexes chunked documents into ChromaDB."""
        if not documents:
            raise ValueError("Cannot index an empty document list.")
            
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        return vectorstore

    def get_vectorstore(self) -> Optional[Chroma]:
        """Loads an existing Chroma vector store from disk."""
        if not os.path.exists(self.persist_directory) or not os.listdir(self.persist_directory):
            return None
            
        return Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def clear_index(self) -> None:
        """Deletes the existing Chroma database."""
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
