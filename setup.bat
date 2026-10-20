@echo off
setlocal enabledelayedexpansion
title PrivateDoc RAG — Setup & Launch

echo.
echo  =========================================================
echo   PrivateDoc RAG v2.0  ^|  100%% Local Offline Document AI
echo  =========================================================
echo.

:: ── Check Python ──────────────────────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% detected.

:: ── Check Ollama ──────────────────────────────────────────────────────────────
where ollama >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Ollama not found. Please install from https://ollama.com then re-run.
    pause
    exit /b 1
)
echo [OK] Ollama detected.

:: ── Virtual Environment ───────────────────────────────────────────────────────
if not exist "venv\" (
    echo.
    echo [1/4] Creating Python virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created.
) else (
    echo [1/4] Virtual environment already exists.
)

:: ── Activate Venv ─────────────────────────────────────────────────────────────
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated.

:: ── Install Dependencies ──────────────────────────────────────────────────────
echo.
echo [2/4] Installing Python dependencies (this may take a few minutes)...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo [OK] Dependencies installed.

:: ── Pull Ollama Models ────────────────────────────────────────────────────────
echo.
echo [3/4] Pulling Ollama models (will skip if already downloaded)...
ollama pull llama3.1:8b
ollama pull nomic-embed-text
echo [OK] Models ready.

:: ── Launch App ───────────────────────────────────────────────────────────────
echo.
echo [4/4] Launching PrivateDoc RAG...
echo       Open http://localhost:8501 in your browser.
echo.
streamlit run app.py --server.headless false --browser.gatherUsageStats false

pause
