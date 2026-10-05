import streamlit as st
import os
import shutil
from config import config
from core.document_loader import UniversalDocumentLoader
from core.text_splitter import DocumentChunker
from core.vector_store import VectorStoreManager
from core.rag_engine import RAGEngine

# Page Configuration
st.set_page_config(
    page_title="PrivateDoc RAG - Offline AI Document Assistant",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern dark/light styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        color: #94A3B8;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .citation-card {
        padding: 10px 14px;
        background-color: rgba(59, 130, 246, 0.08);
        border-left: 3px solid #3B82F6;
        border-radius: 4px;
        margin-bottom: 8px;
        font-size: 0.88rem;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #10B981;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

# Instantiate Vector Manager
vector_manager = VectorStoreManager(
    persist_directory=config.PERSIST_DIRECTORY,
    embedding_model=config.DEFAULT_EMBED_MODEL
)

# Sidebar UI
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    selected_llm = st.selectbox(
        "Select Local LLM (Ollama)",
        options=config.AVAILABLE_LLMS,
        index=0
    )
    
    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=config.TEMPERATURE,
        step=0.05
    )
    
    top_k = st.slider(
        "Top-K Retrieval Chunks",
        min_value=1,
        max_value=8,
        value=config.TOP_K_RETRIEVAL,
        step=1
    )
    
    st.markdown("---")
    st.markdown("### 📂 Document Ingestion")
    
    uploaded_files = st.file_uploader(
        "Upload files (PDF, DOCX, TXT, CSV, MD)",
        accept_multiple_files=True,
        type=["pdf", "docx", "txt", "csv", "md"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        build_btn = st.button("⚡ Index Files", use_container_width=True, type="primary")
    with col2:
        clear_btn = st.button("🗑️ Clear Index", use_container_width=True)

    if clear_btn:
        vector_manager.clear_index()
        st.session_state.indexed_files = []
        st.session_state.messages = []
        st.success("Index reset successfully!")
        st.rerun()

    if build_btn:
        if not uploaded_files:
            st.warning("Please select at least one document.")
        else:
            with st.spinner("Processing and indexing documents..."):
                os.makedirs(config.UPLOAD_TEMP_DIR, exist_ok=True)
                raw_documents = []
                file_names = []
                
                for uploaded in uploaded_files:
                    temp_path = os.path.join(config.UPLOAD_TEMP_DIR, uploaded.name)
                    with open(temp_path, "wb") as f:
                        f.write(uploaded.getvalue())
                        
                    try:
                        docs = UniversalDocumentLoader.load_file(temp_path, original_filename=uploaded.name)
                        raw_documents.extend(docs)
                        file_names.append(uploaded.name)
                    except Exception as err:
                        st.error(f"Error loading {uploaded.name}: {err}")
                    finally:
                        if os.path.exists(temp_path):
                            os.remove(temp_path)
                            
                if raw_documents:
                    chunker = DocumentChunker(
                        chunk_size=config.DEFAULT_CHUNK_SIZE,
                        chunk_overlap=config.DEFAULT_CHUNK_OVERLAP
                    )
                    chunks = chunker.split_documents(raw_documents)
                    vector_manager.create_or_update_index(chunks)
                    st.session_state.indexed_files = list(set(file_names))
                    st.success(f"Indexed {len(raw_documents)} documents ({len(chunks)} chunks)!")
                else:
                    st.error("No valid text could be parsed.")

    if st.session_state.indexed_files:
        st.markdown("#### 📄 Active Index Files:")
        for fn in st.session_state.indexed_files:
            st.markdown(f"- `{fn}`")

# Main Interface
st.markdown('<div class="main-header">🔒 PrivateDoc RAG</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">100% Offline, Secure Document Intelligence Powered by Ollama, LangChain & ChromaDB</div>', unsafe_allow_html=True)

# Display Chat Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "citations" in msg and msg["citations"]:
            with st.expander("📍 Sources & Citations"):
                for cit in msg["citations"]:
                    st.markdown(f"""
                    <div class="citation-card">
                        <strong>📄 {cit['source']}</strong> — Page {cit['page']}<br>
                        <em>"{cit['preview']}"</em>
                    </div>
                    """, unsafe_allow_html=True)

# Chat Input & Inference
if prompt := st.chat_input("Ask a question about your uploaded documents..."):
    # Append user question
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant answer
    with st.chat_message("assistant"):
        vs = vector_manager.get_vectorstore()
        if not vs:
            st.warning("⚠️ No documents indexed yet. Please upload files and click **'⚡ Index Files'** in the sidebar.")
        else:
            with st.spinner("Analyzing documents & generating answer..."):
                try:
                    rag_engine = RAGEngine(
                        model_name=selected_llm,
                        temperature=temperature,
                        top_k=top_k
                    )
                    result = rag_engine.answer_query(prompt, vector_manager)
                    
                    st.markdown(result["answer"])
                    if result["citations"]:
                        with st.expander("📍 Sources & Citations"):
                            for cit in result["citations"]:
                                st.markdown(f"""
                                <div class="citation-card">
                                    <strong>📄 {cit['source']}</strong> — Page {cit['page']}<br>
                                    <em>"{cit['preview']}"</em>
                                </div>
                                """, unsafe_allow_html=True)
                                
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "citations": result["citations"]
                    })
                except Exception as e:
                    st.error(f"Error during query execution: {str(e)}")
