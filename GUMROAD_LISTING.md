# 🏷️ Gumroad Product Listing Kit — PrivateDoc RAG

Use this exact copy and layout to publish your product on **Gumroad** (or Lemon Squeezy / Payhip).

---

## 1. Product Name & Tagline

- **Product Name:** `PrivateDoc RAG: Turnkey Local Document AI Boilerplate (100% Offline)`
- **Subtitle / 1-Line Pitch:** `Chat privately with your PDFs, Word docs & text files with page-level citations using Ollama & ChromaDB. Zero cloud APIs, zero subscriptions, 100% confidential.`

---

## 2. Recommended Pricing Tiers

| Tier | Price | Who It's For | What's Included |
|------|-------|--------------|-----------------|
| **Starter / Personal** | **$19** | Students, solo researchers, individual developers | Full source code, 1-click Windows/Mac setup scripts, sample docs, personal use license. |
| **Commercial / Freelancer (Recommended)** | **$39** | Freelancers, agency owners, consultants | Everything in Starter + **Commercial Redistribution License** (use for client projects & client deliverables). |
| **Complete Developer Bundle** | **$69** | Teams, agencies, advanced devs | Everything in Commercial + Docker deployment config, architectural walkthrough video guide, and priority email support. |

---

## 3. Product Description (Paste directly into Gumroad)

```markdown
### 🔒 Tired of leaking sensitive client files or internal docs to OpenAI?

Most developers and privacy-conscious teams waste 15–20+ hours wrestling with LangChain version breaks, vector store configs, chunking errors, and UI styling just to get a local RAG app working.

**PrivateDoc RAG solves this in 1 click.**

It is a production-ready, turnkey Python boilerplate with a clean modern Streamlit UI, powered by **Ollama** and **ChromaDB**. Your documents never leave your machine or office desktop.

---

### ⚡ What You Can Do in 3 Minutes:
1. **Double-click `setup.bat`** (Windows) or `./setup.sh` (Mac/Linux).
2. The script configures the virtual environment, installs dependencies, pulls the lightweight LLM & embedding model, and boots the browser app.
3. Drag & drop your PDFs, DOCX, TXT, or CSV files.
4. Ask any question — get instant, streamed answers with **exact page number citations** and source text snippets.

---

### ✨ Key Features Included:
- 🛡️ **100% Air-Gapped & Offline:** Powered by Ollama (`llama3.1:8b`, `qwen2.5:3b`, `mistral`, etc.) and `nomic-embed-text`.
- 📑 **Multi-Format Ingestion:** Drag-and-drop support for PDF, Word (.docx), Plain Text (.txt), CSV, and Markdown (.md).
- 📌 **Verifiable Page Citations:** Every answer cites the exact filename, page number, and relevant text snippet in an interactive drawer.
- ⚙️ **On-the-Fly Tuning:** Adjust chunk size (500–2000 chars) and overlap directly in the sidebar without editing code.
- 💬 **Conversational Memory:** Remembers multi-turn chat context across queries.
- 💾 **Persistent Storage:** Local ChromaDB persists your indexed documents across restarts.
- 🐳 **Docker Ready:** Includes tested Dockerfile for containerized deployments.
- 📄 **Sample Documents Included:** Includes pre-formatted sample files so you can test right out of the box.

---

### 📦 What's Inside the Download:
- `app.py`: Complete, modular, beautifully-styled Streamlit application
- `core/`:
  - `document_loader.py` (Universal document parser)
  - `text_splitter.py` (Smart recursive chunker)
  - `vector_store.py` (Local ChromaDB manager)
  - `rag_engine.py` (LangChain + Ollama RAG pipeline with citations)
- `setup.bat` & `setup.sh`: Automated 1-click installer scripts
- `run_app.bat` & `run_app.sh`: Fast launcher scripts
- `Dockerfile`: Containerized local deployment
- `sample_docs/`: HR handbook & financial report test data
- `README.md`: Complete documentation & troubleshooting guide
- `LICENSE`: Commercial or personal license

---

### 💻 System Requirements:
- **Operating System:** Windows 10/11, macOS (Intel & Apple Silicon), or Linux
- **RAM:** 8GB minimum (16GB recommended for 8B models)
- **Software:** Python 3.10+ and [Ollama](https://ollama.com) (free)

---

### ❓ Frequently Asked Questions (FAQ)

**Q: Do I need an expensive NVIDIA GPU?**  
A: No! Modern models like `qwen2.5:3b` or `llama3.2:3b` run fast on regular laptop CPUs (Apple Silicon or Intel/AMD). If you have an NVIDIA GPU, Ollama will automatically accelerate it.

**Q: Can I use this for client projects on Fiverr / Upwork?**  
A: Yes! Choose the **Commercial / Freelancer License** and you can customize and deploy this system for unlimited freelance clients.

**Q: Do I need an OpenAI API key or subscription?**  
A: Never. All embeddings and LLM reasoning run 100% locally on your hardware. Zero API costs forever.
```

---

## 4. Post-Purchase Thank You Note (Gumroad "Receipt & Content")

```markdown
Thank you for purchasing PrivateDoc RAG! 🎉

Here is your download link:
👉 [Download PrivateDoc-RAG-v1.0-Turnkey-Boilerplate.zip]

Getting Started:
1. Unzip the archive to any folder on your computer.
2. Install Ollama from https://ollama.com (if you haven't already).
3. On Windows: Double-click `setup.bat`.
   On Mac/Linux: Run `chmod +x setup.sh && ./setup.sh` in terminal.
4. Your browser will automatically open to http://localhost:8501.

If you have any questions or need assistance, reply to your receipt email or reach out directly.
Happy building!
```
