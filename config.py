import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    # Model Configurations
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "llama3.1:8b")
    DEFAULT_EMBED_MODEL: str = os.getenv("DEFAULT_EMBED_MODEL", "nomic-embed-text")
    
    # Available Models for UI dropdown
    AVAILABLE_LLMS = [
        "llama3.1:8b",
        "llama3.2:3b",
        "qwen2.5:7b",
        "qwen2.5:3b",
        "mistral:7b",
        "gemma2:9b"
    ]
    
    AVAILABLE_EMBEDDINGS = [
        "nomic-embed-text",
        "bge-m3",
        "all-minilm"
    ]
    
    # Chunking Configurations
    DEFAULT_CHUNK_SIZE: int = 1000
    DEFAULT_CHUNK_OVERLAP: int = 150
    
    # Storage Paths
    PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    UPLOAD_TEMP_DIR: str = "./temp_uploads"
    
    # Retrieval Configurations
    TOP_K_RETRIEVAL: int = 4
    TEMPERATURE: float = 0.2

config = AppConfig()
