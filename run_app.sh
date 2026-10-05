#!/bin/bash
echo "======================================================"
echo " PrivateDoc RAG: 100% Local Offline Document AI"
echo "======================================================"

echo "[1/3] Installing dependencies..."
pip install -r requirements.txt

echo "[2/3] Pulling Ollama models..."
ollama pull llama3.1:8b
ollama pull nomic-embed-text

echo "[3/3] Launching PrivateDoc RAG Application..."
streamlit run app.py
