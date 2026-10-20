import os
from dataclasses import dataclass, field
from typing import List


@dataclass
class AppConfig:
    # ── LLM / Embedding Model Settings ─────────────────────────────────────────
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "llama3.1:8b")
    DEFAULT_EMBED_MODEL: str = os.getenv("DEFAULT_EMBED_MODEL", "all-minilm")

    AVAILABLE_LLMS: List[str] = field(
        default_factory=lambda: [
            "llama3.1:8b",
            "qwen2.5:7b",
            "qwen2.5-coder:7b",
            "llama3.2:3b",
            "qwen2.5:3b",
            "mistral:7b",
            "gemma2:9b",
            "deepseek-r1:7b",
            "phi3:mini",
        ]
    )

    AVAILABLE_EMBEDDINGS: List[str] = field(
        default_factory=lambda: [
            "all-minilm",
            "nomic-embed-text",
            "bge-m3",
        ]
    )

    # ── Chunking Settings ───────────────────────────────────────────────────────
    DEFAULT_CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "800"))
    DEFAULT_CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    MIN_CHUNK_SIZE: int = 200
    MAX_CHUNK_SIZE: int = 3000

    # ── Storage Paths ───────────────────────────────────────────────────────────
    PERSIST_DIRECTORY: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    UPLOAD_TEMP_DIR: str = "./temp_uploads"
    SAMPLE_DOCS_DIR: str = "./sample_docs"

    # ── Retrieval & Inference Settings ─────────────────────────────────────────
    TOP_K_RETRIEVAL: int = int(os.getenv("TOP_K", "3"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.15"))
    MEMORY_WINDOW: int = int(os.getenv("MEMORY_WINDOW", "6"))  # turns to remember

    # ── App Metadata ────────────────────────────────────────────────────────────
    APP_TITLE: str = "PrivateDoc RAG"
    APP_VERSION: str = "2.1.0"
    APP_TAGLINE: str = "100% Offline · Air-Gapped · Local Vector Intelligence"


config = AppConfig()
