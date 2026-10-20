# 🔒 PrivateDoc RAG — Private Local Document AI

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.2-green.svg)](https://www.langchain.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Offline%20LLMs-black.svg)](https://ollama.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-purple.svg)](https://www.trychroma.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> **100% offline. Zero cloud APIs. Your documents never leave your machine.**

PrivateDoc RAG is a **production-ready, turnkey RAG (Retrieval-Augmented Generation) boilerplate** for developers and privacy-conscious professionals who need accurate, cite-referenced answers from their own documents — without sending data to OpenAI, Anthropic, or any third-party service.

---

## ✨ Features at a Glance

| Feature | Details |
|---------|---------|
| **100% Offline & Private** | Powered by [Ollama](https://ollama.com) — zero external API calls |
| **Multi-Format Ingestion** | PDF, DOCX, TXT, CSV, Markdown — drag & drop upload |
| **Conversational Memory** | Multi-turn chat with sliding-window context (remembers last N exchanges) |
| **Page-Level Citations** | Every answer cites the exact document, page number, and text snippet |
| **Adjustable Chunking** | Set chunk size & overlap directly in the UI — no code changes needed |
| **Dynamic Model Switching** | Switch between Llama 3.1, Qwen 2.5, Mistral, Gemma 2, Phi-3 on the fly |
| **Persistent Vector Store** | ChromaDB persists your index across restarts |
| **1-Click Setup** | `setup.bat` (Windows) / `setup.sh` (macOS & Linux) handle everything |
| **Docker Ready** | Included `Dockerfile` for containerized deployment |

---

## 🚀 Quick Start (1 Click)

### Prerequisites
1. **Python 3.10+** → [python.org](https://python.org)
2. **Ollama** → [ollama.com](https://ollama.com) (free, runs locally)

### Windows — Double-click to launch:
```
setup.bat
```

### macOS / Linux:
```bash
chmod +x setup.sh
./setup.sh
```

The script will:
1. ✅ Validate Python & Ollama
2. ✅ Create a Python virtual environment
3. ✅ Install all dependencies
4. ✅ Pull `llama3.1:8b` and `nomic-embed-text` via Ollama
5. ✅ Launch the Streamlit web interface at **http://localhost:8501**

---

## 🧠 How It Works

```
Documents (PDF/DOCX/TXT/CSV/MD)
        │
        ▼
┌─────────────────────────────┐
│   Universal Document Loader │  ← Extracts text + metadata (page numbers)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   Recursive Chunker         │  ← Splits into overlapping chunks (configurable)
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   Ollama Embeddings         │  ← nomic-embed-text (local, no API key)
│   ChromaDB Vector Store     │  ← Persisted to disk
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┐
    │  User Query + Chat  │
    │       History       │
    └──────────┬──────────┘
               │
               ▼
┌─────────────────────────────┐
│   Similarity Retrieval      │  ← Top-K relevant chunks
│   ConversationalRAG Chain   │  ← LangChain with memory
│   Local LLM (Ollama)        │  ← Llama 3.1, Qwen 2.5, etc.
└──────────────┬──────────────┘
               │
               ▼
     Answer + Page Citations
```

---

## 📂 Project Structure

```
private-document-rag/
├── core/
│   ├── __init__.py
│   ├── document_loader.py    # PDF, DOCX, TXT, CSV, MD parsing + metadata
│   ├── text_splitter.py      # Recursive semantic chunking with overlap
│   ├── vector_store.py       # ChromaDB create / load / clear operations
│   └── rag_engine.py         # ConversationalRetrievalChain + citation engine
├── tests/
│   └── test_document_loader.py  # 16-test pytest suite (no Ollama required)
├── app.py                    # Streamlit web UI (premium dark theme)
├── config.py                 # All settings — env-var overridable
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker deployment
├── setup.bat                 # 1-Click installer & launcher (Windows)
├── setup.sh                  # 1-Click installer & launcher (macOS / Linux)
└── README.md
```

---

## ⚙️ Configuration

All settings are in [`config.py`](./config.py) and can be overridden via environment variables:

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `DEFAULT_LLM_MODEL` | `llama3.1:8b` | Default LLM loaded at startup |
| `DEFAULT_EMBED_MODEL` | `nomic-embed-text` | Embedding model for ChromaDB |
| `CHUNK_SIZE` | `1000` | Characters per document chunk |
| `CHUNK_OVERLAP` | `150` | Overlap between consecutive chunks |
| `TOP_K` | `4` | Chunks retrieved per query |
| `TEMPERATURE` | `0.2` | LLM creativity (0 = deterministic) |
| `MEMORY_WINDOW` | `6` | Number of previous turns to remember |
| `CHROMA_PERSIST_DIR` | `./chroma_db` | ChromaDB persistence path |

---

## 🤖 Supported Models

**LLMs (via Ollama)**
- `llama3.1:8b` ← Recommended default
- `llama3.2:3b` ← Fastest, lower RAM
- `qwen2.5:7b` / `qwen2.5:3b`
- `mistral:7b`
- `gemma2:9b`
- `deepseek-r1:7b`
- `phi3:mini`

**Embedding Models**
- `nomic-embed-text` ← Recommended default
- `bge-m3` ← Multilingual support
- `all-minilm` ← Lightest weight

Pull any model with: `ollama pull <model-name>`

---

## 🐳 Docker Deployment

```bash
# Build
docker build -t privatedoc-rag .

# Run (Ollama must be running on host)
docker run -p 8501:8501 --add-host=host.docker.internal:host-gateway privatedoc-rag
```

---

## 🧪 Running Tests

```bash
# Activate your virtual environment first
pytest tests/ -v
```

Tests run **without** a live Ollama instance (RAG chain calls are mocked).

---

## ❓ FAQ

**Q: Does this send my documents to OpenAI or any cloud?**
No. Everything runs locally via Ollama. Zero external API calls.

**Q: How much RAM do I need?**
- `llama3.2:3b` → ~4 GB VRAM / 8 GB system RAM
- `llama3.1:8b` → ~8 GB VRAM / 16 GB system RAM
- CPU-only mode works but is slower.

**Q: Can I use a different vector database?**
Yes — swap `core/vector_store.py` for any LangChain-compatible store (Qdrant, FAISS, Weaviate, etc.).

**Q: Can I add more document types?**
Yes — add your loader to the `SUPPORTED_EXTENSIONS` dict in `core/document_loader.py`.

---

## 📄 License

MIT License — see [LICENSE](./LICENSE).
