@echo off
echo ======================================================
echo  PrivateDoc RAG: 100%% Local Offline Document AI
echo ======================================================

echo [1/3] Checking Python dependencies...
pip install -r requirements.txt

echo [2/3] Checking Ollama Models...
echo Pulling Llama 3.1 8B (LLM)...
ollama pull llama3.1:8b
echo Pulling Nomic Embed Text (Embeddings)...
ollama pull nomic-embed-text

echo [3/3] Launching PrivateDoc RAG Application...
streamlit run app.py

pause
