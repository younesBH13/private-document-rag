"""
PrivateDoc RAG — Ultra-Premium Local Document AI
Version 2.2 | 100% Offline · Air-Gapped · Clean White / Executive Light Mode
"""

import os
import time
import glob
import json
import urllib.request
import streamlit as st
from config import config
from core.document_loader import UniversalDocumentLoader
from core.text_splitter import DocumentChunker
from core.vector_store import VectorStoreManager
from core.rag_engine import RAGEngine

# ── Page Configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{config.APP_TITLE} · Enterprise Local AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": f"**{config.APP_TITLE} v{config.APP_VERSION}**\n\n{config.APP_TAGLINE}",
    },
)

# ── Clean White Mode Design System (CSS) ───────────────────────────────────────
st.markdown(
    """
<style>
/* ── Typography & Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    color: #0f172a !important;
}

/* ── Hide Streamlit Clutter ── */
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { 
    background: rgba(248, 250, 252, 0.9) !important; 
    backdrop-filter: blur(12px); 
    border-bottom: 1px solid #e2e8f0;
}
footer { visibility: hidden; }

/* ── App Canvas: Pure Clean White Theme ── */
.stApp {
    background: #f8fafc !important;
}

/* ── Sidebar Styling (Clean Slate / White) ── */
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.02);
}
section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ── Custom Light Glass Panels ── */
.white-panel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 16px;
    box-shadow: 0 4px 15px -3px rgba(0, 0, 0, 0.04), 0 2px 6px -2px rgba(0, 0, 0, 0.02);
}

/* ── Top Header Banner (Clean White Luxury) ── */
.privatedoc-hero {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 24px;
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
}
.privatedoc-brand {
    display: flex;
    align-items: center;
    gap: 16px;
}
.privatedoc-brand-icon {
    font-size: 2rem;
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    color: #ffffff;
}
.privatedoc-title {
    font-size: 1.65rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #0f172a !important;
    margin: 0;
    line-height: 1.2;
}
.privatedoc-sub {
    font-size: 0.85rem;
    color: #64748b !important;
    margin-top: 3px;
    font-weight: 400;
}
.hero-badges {
    display: flex;
    gap: 10px;
    align-items: center;
}

/* ── Status Pills (Light Mode) ── */
.badge-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}
.badge-pill.air-gapped {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    color: #047857;
}
.badge-pill.model-active {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    color: #1d4ed8;
}
.badge-pill.status-pulse::before {
    content: "";
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 8px #10b981;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
    70% { transform: scale(1.1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* ── Stats Dashboard Grid (Clean White Cards) ── */
.stats-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 22px;
}
.stat-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 14px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    transition: all 0.2s ease;
}
.stat-box:hover {
    border-color: #93c5fd;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
    transform: translateY(-2px);
}
.stat-val {
    font-size: 1.55rem;
    font-weight: 800;
    color: #0f172a;
    line-height: 1.2;
}
.stat-name {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748b;
    margin-top: 4px;
    font-weight: 600;
}

/* ── Suggested Questions Grid ── */
.prompt-chips-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin: 16px 0 24px;
}
.prompt-chip {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 16px;
    font-size: 0.88rem;
    color: #1e293b;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}
.prompt-chip:hover {
    background: #f0f7ff;
    border-color: #93c5fd;
    color: #1d4ed8;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.06);
}

/* ── Citations (White & Deep Blue) ── */
.cite-container {
    margin-top: 12px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}
.cite-item {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #0284c7;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    font-size: 0.85rem;
    line-height: 1.6;
}
.cite-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
}
.cite-source-tag {
    font-weight: 700;
    color: #0369a1;
    display: flex;
    align-items: center;
    gap: 6px;
}
.cite-page-badge {
    background: #e0f2fe;
    color: #0284c7;
    padding: 2px 9px;
    border-radius: 6px;
    font-size: 0.72rem;
    font-weight: 700;
}
.cite-quote {
    color: #334155;
    font-style: italic;
}

/* ── Sidebar Section Headers ── */
.sidebar-header {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    margin: 22px 0 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── File Badge in Sidebar ── */
.file-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.8rem;
}
.file-name {
    color: #0f172a;
    font-weight: 500;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 170px;
}
.file-size {
    color: #64748b;
    font-size: 0.72rem;
}

/* ── Response Meta Ribbon ── */
.answer-meta {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    font-size: 0.74rem;
    color: #475569;
    margin-top: 10px;
    padding: 5px 12px;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-weight: 500;
}

/* ── Chat Messages Container Styling ── */
div[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    padding: 16px 20px !important;
    margin-bottom: 14px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
}
div[data-testid="stChatMessage"] p {
    color: #0f172a !important;
    font-size: 0.95rem !important;
    line-height: 1.65 !important;
}

/* ── Chat Input Styling ── */
div[data-testid="stChatInput"] {
    border-radius: 12px !important;
    border: 1px solid #cbd5e1 !important;
    background: #ffffff !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04) !important;
}
div[data-testid="stChatInput"] textarea {
    color: #0f172a !important;
    background: #ffffff !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Helper Utilities ───────────────────────────────────────────────────────────

def get_installed_ollama_models() -> list[str]:
    """Auto-detects live models from local Ollama service."""
    try:
        req = urllib.request.Request("http://localhost:11434/api/tags", headers={"User-Agent": "PrivateDocRAG"})
        with urllib.request.urlopen(req, timeout=1.5) as resp:
            data = json.loads(resp.read().decode())
            models = [m["name"] for m in data.get("models", [])]
            if models:
                return models
    except Exception:
        pass
    return config.AVAILABLE_LLMS


def format_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    elif n < 1024 ** 2:
        return f"{n/1024:.1f} KB"
    return f"{n/1024**2:.1f} MB"


def file_icon(filename: str) -> str:
    ext = os.path.splitext(filename)[-1].lower()
    return {".pdf": "📕", ".docx": "📘", ".txt": "📄", ".csv": "📊", ".md": "📝"}.get(ext, "📎")


# ── Session State Initialization ──────────────────────────────────────────────
session_defaults = {
    "messages": [],
    "indexed_files": [],       # [{"name": ..., "size": ..., "pages": ...}]
    "total_chunks": 0,
    "rag_engine": None,
    "last_model": None,
    "last_temperature": None,
    "last_top_k": None,
    "pending_query": None,
}
for k, v in session_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Initialize Vector Manager
vector_manager = VectorStoreManager(
    persist_directory=config.PERSIST_DIRECTORY,
    embedding_model=config.DEFAULT_EMBED_MODEL,
)

# ── Check Existing Index On Startup ──
if not st.session_state.indexed_files:
    vs = vector_manager.get_vectorstore()
    if vs is not None:
        try:
            count = vs._collection.count()
            if count > 0:
                st.session_state.total_chunks = count
                st.session_state.indexed_files = [{"name": "Persistent Index", "size": 0, "pages": 1}]
        except Exception:
            pass

detected_models = get_installed_ollama_models()

# ── Sidebar (Clean White) ──────────────────────────────────────────────────────
with st.sidebar:
    # Sidebar Header
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
            <div style="font-size:1.6rem;background:linear-gradient(135deg, #2563eb, #4f46e5);
                        width:42px;height:42px;display:flex;align-items:center;justify-content:center;
                        border-radius:10px;box-shadow:0 4px 12px rgba(37,99,235,0.25);color:#fff;">🛡️</div>
            <div>
                <div style="font-weight:800;font-size:1.05rem;color:#0f172a;letter-spacing:-0.01em;">PrivateDoc AI</div>
                <div style="font-size:0.75rem;color:#64748b;">Enterprise Offline RAG · v2.2</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1-Click Demo Knowledge Base
    if st.button("🚀 Load Demo Knowledge Base", use_container_width=True, help="Index sample HR Handbook & Financial Summary instantly without uploading"):
        sample_files = glob.glob(os.path.join(config.SAMPLE_DOCS_DIR, "*.*"))
        if sample_files:
            with st.spinner("Indexing sample enterprise documents…"):
                raw_docs = []
                new_files = []
                for sp in sample_files:
                    fname = os.path.basename(sp)
                    docs = UniversalDocumentLoader.load_file(sp, original_filename=fname)
                    raw_docs.extend(docs)
                    new_files.append({"name": fname, "size": os.path.getsize(sp), "pages": len(docs)})
                
                chunker = DocumentChunker(chunk_size=config.DEFAULT_CHUNK_SIZE, chunk_overlap=config.DEFAULT_CHUNK_OVERLAP)
                chunks = chunker.split_documents(raw_docs)
                vector_manager.create_or_update_index(chunks)
                st.session_state.indexed_files = new_files
                st.session_state.total_chunks = len(chunks)
                st.session_state.rag_engine = None
                st.success(f"Loaded {len(new_files)} demo files ({len(chunks)} chunks)!")
                st.rerun()
        else:
            st.error("No sample docs found in sample_docs folder.")

    # ── Engine Configuration ──
    st.markdown('<div class="sidebar-header">⚙️ Model & Hardware</div>', unsafe_allow_html=True)

    selected_llm = st.selectbox(
        "Local LLM (via Ollama)",
        options=detected_models,
        index=0 if config.DEFAULT_LLM_MODEL not in detected_models else detected_models.index(config.DEFAULT_LLM_MODEL),
        key="sel_llm",
    )

    selected_embedding = st.selectbox(
        "Vector Embeddings",
        options=config.AVAILABLE_EMBEDDINGS,
        index=0,
        help="all-minilm uses built-in high-speed ONNX embeddings locally.",
        key="sel_emb",
    )

    with st.expander("🎛️ Tuning Parameters", expanded=False):
        temperature = st.slider("Temperature", 0.0, 1.0, config.TEMPERATURE, 0.05,
                                help="Lower = strict factual adherence to document text.")
        top_k = st.slider("Top-K Citations", 1, 8, config.TOP_K_RETRIEVAL, 1,
                          help="Number of retrieved chunks passed to context.")
        chunk_size = st.slider("Chunk Size", config.MIN_CHUNK_SIZE, config.MAX_CHUNK_SIZE, config.DEFAULT_CHUNK_SIZE, 50)
        chunk_overlap = st.slider("Chunk Overlap", 0, chunk_size // 2, config.DEFAULT_CHUNK_OVERLAP, 25)

    # ── Document Upload ──
    st.markdown('<div class="sidebar-header">📂 Ingest Documents</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Drag & drop PDF, DOCX, TXT, CSV, MD",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt", "csv", "md"],
        label_visibility="collapsed",
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        build_btn = st.button("⚡ Index Files", use_container_width=True, type="primary")
    with col_btn2:
        reset_btn = st.button("🗑️ Reset All", use_container_width=True)

    if reset_btn:
        vector_manager.clear_index()
        if st.session_state.rag_engine:
            st.session_state.rag_engine.clear_memory()
        st.session_state.indexed_files = []
        st.session_state.total_chunks = 0
        st.session_state.messages = []
        st.session_state.rag_engine = None
        st.success("Database and chat memory cleared.")
        st.rerun()

    if build_btn:
        if not uploaded_files:
            st.warning("Please select at least one file to index.")
        else:
            prog_bar = st.progress(0, text="Extracting documents…")
            os.makedirs(config.UPLOAD_TEMP_DIR, exist_ok=True)
            raw_docs = []
            new_records = []
            for i, uf in enumerate(uploaded_files):
                prog_bar.progress((i + 1) / (len(uploaded_files) + 1), text=f"Processing {uf.name}…")
                tpath = os.path.join(config.UPLOAD_TEMP_DIR, uf.name)
                try:
                    with open(tpath, "wb") as f:
                        f.write(uf.getvalue())
                    docs = UniversalDocumentLoader.load_file(tpath, original_filename=uf.name)
                    raw_docs.extend(docs)
                    new_records.append({"name": uf.name, "size": uf.size, "pages": len(docs)})
                finally:
                    if os.path.exists(tpath):
                        os.remove(tpath)

            if raw_docs:
                prog_bar.progress(0.85, text="Chunking and generating embeddings…")
                chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                chunks = chunker.split_documents(raw_docs)
                vector_manager.create_or_update_index(chunks)
                st.session_state.indexed_files = new_records
                st.session_state.total_chunks = len(chunks)
                st.session_state.rag_engine = None
                prog_bar.progress(1.0, text="Done!")
                time.sleep(0.3)
                prog_bar.empty()
                st.success(f"Indexed {len(new_records)} file(s) into {len(chunks)} vector chunks.")
                st.rerun()

    # ── Display Indexed Files List in Sidebar ──
    if st.session_state.indexed_files:
        st.markdown('<div class="sidebar-header">📑 Active Knowledge Base</div>', unsafe_allow_html=True)
        for f in st.session_state.indexed_files:
            icon = file_icon(f["name"])
            sz = format_bytes(f.get("size", 0)) if f.get("size", 0) > 0 else "Ready"
            st.markdown(
                f"""
                <div class="file-row">
                    <div style="display:flex;align-items:center;gap:6px;">
                        <span>{icon}</span>
                        <span class="file-name" title="{f['name']}">{f['name']}</span>
                    </div>
                    <span class="file-size">{sz}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("---")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.rag_engine:
            st.session_state.rag_engine.clear_memory()
        st.rerun()


# ── Main Interface Canvas (Clean White) ─────────────────────────────────────────

# 1. Hero Header
st.markdown(
    f"""
    <div class="privatedoc-hero">
        <div class="privatedoc-brand">
            <div class="privatedoc-brand-icon">🛡️</div>
            <div>
                <h1 class="privatedoc-title">PrivateDoc RAG</h1>
                <div class="privatedoc-sub">100% Offline Air-Gapped Intelligence · Zero Data Leaks</div>
            </div>
        </div>
        <div class="hero-badges">
            <span class="badge-pill air-gapped status-pulse">Air-Gapped & Secure</span>
            <span class="badge-pill model-active">🤖 {selected_llm}</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 2. Key Metrics Bar
total_files = len(st.session_state.indexed_files)
total_chunks = st.session_state.total_chunks
total_kb_size = sum(f.get("size", 0) for f in st.session_state.indexed_files)
status_str = "Active" if total_chunks > 0 else "Awaiting Data"

st.markdown(
    f"""
    <div class="stats-container">
        <div class="stat-box">
            <div class="stat-val">{total_files}</div>
            <div class="stat-name">Active Documents</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{total_chunks}</div>
            <div class="stat-name">Vector Chunks</div>
        </div>
        <div class="stat-box">
            <div class="stat-val">{format_bytes(total_kb_size) if total_kb_size > 0 else "0 KB"}</div>
            <div class="stat-name">Payload Size</div>
        </div>
        <div class="stat-box">
            <div class="stat-val" style="color: {'#059669' if total_chunks > 0 else '#64748b'};">{status_str}</div>
            <div class="stat-name">Knowledge Status</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# 3. Handle Clicked Suggested Prompt (if any)
if st.session_state.pending_query:
    active_prompt = st.session_state.pending_query
    st.session_state.pending_query = None
else:
    active_prompt = None

# 4. Empty State Hero with Clickable Suggestion Chips
if not st.session_state.messages and total_chunks == 0:
    st.markdown(
        """
        <div class="white-panel" style="text-align:center;padding:36px 24px;">
            <div style="font-size:3.2rem;margin-bottom:12px;">🔒</div>
            <h2 style="font-size:1.5rem;font-weight:800;color:#0f172a;margin-bottom:8px;">Your Private Enterprise AI Assistant</h2>
            <p style="color:#475569;max-width:620px;margin:0 auto 20px;font-size:0.92rem;line-height:1.6;">
                Upload confidential legal contracts, medical logs, or internal manuals.
                PrivateDoc RAG performs high-speed semantic retrieval directly on your local CPU/GPU with page-accurate citations.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("##### 💡 Try out sample questions (click to load demo knowledge base):")
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        if st.button("💼 What is the equipment reimbursement and remote work policy?", use_container_width=True):
            sample_files = glob.glob(os.path.join(config.SAMPLE_DOCS_DIR, "*.*"))
            if sample_files:
                raw_docs = []
                new_files = []
                for sp in sample_files:
                    fname = os.path.basename(sp)
                    docs = UniversalDocumentLoader.load_file(sp, original_filename=fname)
                    raw_docs.extend(docs)
                    new_files.append({"name": fname, "size": os.path.getsize(sp), "pages": len(docs)})
                chunker = DocumentChunker(chunk_size=config.DEFAULT_CHUNK_SIZE, chunk_overlap=config.DEFAULT_CHUNK_OVERLAP)
                chunks = chunker.split_documents(raw_docs)
                vector_manager.create_or_update_index(chunks)
                st.session_state.indexed_files = new_files
                st.session_state.total_chunks = len(chunks)
            st.session_state.pending_query = "What is the equipment reimbursement and remote work policy?"
            st.rerun()
            
        if st.button("🌴 How many PTO and sick leave days do employees get?", use_container_width=True):
            sample_files = glob.glob(os.path.join(config.SAMPLE_DOCS_DIR, "*.*"))
            if sample_files:
                raw_docs = []
                new_files = []
                for sp in sample_files:
                    fname = os.path.basename(sp)
                    docs = UniversalDocumentLoader.load_file(sp, original_filename=fname)
                    raw_docs.extend(docs)
                    new_files.append({"name": fname, "size": os.path.getsize(sp), "pages": len(docs)})
                chunker = DocumentChunker(chunk_size=config.DEFAULT_CHUNK_SIZE, chunk_overlap=config.DEFAULT_CHUNK_OVERLAP)
                chunks = chunker.split_documents(raw_docs)
                vector_manager.create_or_update_index(chunks)
                st.session_state.indexed_files = new_files
                st.session_state.total_chunks = len(chunks)
            st.session_state.pending_query = "How many PTO and sick leave days do employees get each year?"
            st.rerun()

    with pcol2:
        if st.button("📈 What was Apex Financial's Q3 revenue and net profit margin?", use_container_width=True):
            sample_files = glob.glob(os.path.join(config.SAMPLE_DOCS_DIR, "*.*"))
            if sample_files:
                raw_docs = []
                new_files = []
                for sp in sample_files:
                    fname = os.path.basename(sp)
                    docs = UniversalDocumentLoader.load_file(sp, original_filename=fname)
                    raw_docs.extend(docs)
                    new_files.append({"name": fname, "size": os.path.getsize(sp), "pages": len(docs)})
                chunker = DocumentChunker(chunk_size=config.DEFAULT_CHUNK_SIZE, chunk_overlap=config.DEFAULT_CHUNK_OVERLAP)
                chunks = chunker.split_documents(raw_docs)
                vector_manager.create_or_update_index(chunks)
                st.session_state.indexed_files = new_files
                st.session_state.total_chunks = len(chunks)
            st.session_state.pending_query = "What was Apex Financial's Q3 revenue and net profit margin?"
            st.rerun()

        if st.button("🛡️ What is the company policy regarding uploading data to public AI?", use_container_width=True):
            sample_files = glob.glob(os.path.join(config.SAMPLE_DOCS_DIR, "*.*"))
            if sample_files:
                raw_docs = []
                new_files = []
                for sp in sample_files:
                    fname = os.path.basename(sp)
                    docs = UniversalDocumentLoader.load_file(sp, original_filename=fname)
                    raw_docs.extend(docs)
                    new_files.append({"name": fname, "size": os.path.getsize(sp), "pages": len(docs)})
                chunker = DocumentChunker(chunk_size=config.DEFAULT_CHUNK_SIZE, chunk_overlap=config.DEFAULT_CHUNK_OVERLAP)
                chunks = chunker.split_documents(raw_docs)
                vector_manager.create_or_update_index(chunks)
                st.session_state.indexed_files = new_files
                st.session_state.total_chunks = len(chunks)
            st.session_state.pending_query = "What is the policy regarding uploading company data to public AI tools?"
            st.rerun()

elif not st.session_state.messages and total_chunks > 0:
    st.markdown(
        """
        <div class="white-panel" style="padding:20px;border-left:4px solid #10b981;">
            <div style="font-weight:700;color:#047857;font-size:1.05rem;margin-bottom:4px;">✅ Knowledge Base Active & Ready</div>
            <div style="color:#475569;font-size:0.9rem;">
                Ask any specific query below. You will receive an instant response along with exact page-level source citations.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 5. Render Chat Conversation History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🛡️"):
        st.markdown(msg["content"])
        
        # Display response metadata & citations
        if msg.get("citations"):
            citations = msg["citations"]
            elapsed = msg.get("elapsed", 0.0)
            st.markdown(
                f"""
                <div class="answer-meta">
                    <span>⚡ {elapsed:.2f}s latency</span>
                    <span>·</span>
                    <span>📍 {len(citations)} verified citation(s)</span>
                    <span>·</span>
                    <span>🔒 100% on-device</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander(f"📍 Inspect {len(citations)} Source Citation(s)", expanded=False):
                st.markdown('<div class="cite-container">', unsafe_allow_html=True)
                for cit in citations:
                    st.markdown(
                        f"""
                        <div class="cite-item">
                            <div class="cite-meta">
                                <span class="cite-source-tag">📄 {cit['source']}</span>
                                <span class="cite-page-badge">Page {cit['page']}</span>
                            </div>
                            <div class="cite-quote">"{cit['preview']}"</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown('</div>', unsafe_allow_html=True)

# 6. Chat Input & Processing Pipeline
user_input = st.chat_input("Ask a question about your indexed documents…")
query_to_run = active_prompt or user_input

if query_to_run:
    st.session_state.messages.append({"role": "user", "content": query_to_run})
    with st.chat_message("user", avatar="👤"):
        st.markdown(query_to_run)

    with st.chat_message("assistant", avatar="🛡️"):
        vs = vector_manager.get_vectorstore()
        if not vs:
            st.warning("⚠️ No documents indexed yet. Please upload documents or click 'Load Demo Knowledge Base'.")
        else:
            with st.spinner(f"Retrieving vector contexts with {selected_llm}…"):
                t_start = time.time()
                try:
                    if (
                        st.session_state.rag_engine is None
                        or st.session_state.last_model != selected_llm
                        or st.session_state.last_temperature != temperature
                        or st.session_state.last_top_k != top_k
                    ):
                        st.session_state.rag_engine = RAGEngine(
                            model_name=selected_llm,
                            temperature=temperature,
                            top_k=top_k,
                            memory_window=config.MEMORY_WINDOW,
                        )
                        st.session_state.last_model = selected_llm
                        st.session_state.last_temperature = temperature
                        st.session_state.last_top_k = top_k

                    ans_dict = st.session_state.rag_engine.answer_query(
                        query=query_to_run,
                        vector_manager=vector_manager,
                        chat_history=st.session_state.messages[:-1],
                    )
                    t_elapsed = time.time() - t_start

                    # Display Answer
                    st.markdown(ans_dict["answer"])

                    citations = ans_dict.get("citations", [])
                    st.markdown(
                        f"""
                        <div class="answer-meta">
                            <span>⚡ {t_elapsed:.2f}s latency</span>
                            <span>·</span>
                            <span>📍 {len(citations)} verified citation(s)</span>
                            <span>·</span>
                            <span>🔒 100% on-device</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    if citations:
                        with st.expander(f"📍 Inspect {len(citations)} Source Citation(s)", expanded=True):
                            st.markdown('<div class="cite-container">', unsafe_allow_html=True)
                            for cit in citations:
                                st.markdown(
                                    f"""
                                    <div class="cite-item">
                                        <div class="cite-meta">
                                            <span class="cite-source-tag">📄 {cit['source']}</span>
                                            <span class="cite-page-badge">Page {cit['page']}</span>
                                        </div>
                                        <div class="cite-quote">"{cit['preview']}"</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            st.markdown('</div>', unsafe_allow_html=True)

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": ans_dict["answer"],
                            "citations": citations,
                            "elapsed": t_elapsed,
                        }
                    )

                except Exception as exc:
                    err = f"❌ **Inference Error:** `{exc}`\n\nPlease verify Ollama is active (`ollama serve`)."
                    st.error(err)
                    st.session_state.messages.append({"role": "assistant", "content": err})

# 7. Action Bar for Export
if st.session_state.messages:
    st.markdown("<br>", unsafe_allow_html=True)
    c_exp1, c_exp2 = st.columns([1, 4])
    with c_exp1:
        # Generate Markdown export
        chat_transcript = "# PrivateDoc RAG — Q&A Transcript\n\n"
        for m in st.session_state.messages:
            sender = "User" if m["role"] == "user" else "PrivateDoc AI"
            chat_transcript += f"### {sender}:\n{m['content']}\n\n"
            if m.get("citations"):
                chat_transcript += "**Citations:**\n"
                for c in m["citations"]:
                    chat_transcript += f"- *{c['source']}* (Page {c['page']}): \"{c['preview']}\"\n"
                chat_transcript += "\n"

        st.download_button(
            label="📥 Export Chat (.md)",
            data=chat_transcript,
            file_name="privatedoc_rag_chat_transcript.md",
            mime="text/markdown",
            use_container_width=True,
        )
