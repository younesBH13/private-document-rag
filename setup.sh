#!/usr/bin/env bash
set -e

echo ""
echo "  ========================================================="
echo "   PrivateDoc RAG v2.0  |  100% Local Offline Document AI"
echo "  ========================================================="
echo ""

# ── Colour helpers ─────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
ok()   { echo -e "${GREEN}[OK]${NC}    $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC}  $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ── Check Python 3.10+ ────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
    err "Python3 not found. Install Python 3.10+ from https://python.org"
fi
PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
    err "Python 3.10+ required, found $PY_VERSION"
fi
ok "Python $PY_VERSION detected."

# ── Check Ollama ──────────────────────────────────────────────────────────────
if ! command -v ollama &>/dev/null; then
    err "Ollama not found. Install from https://ollama.com then re-run this script."
fi
ok "Ollama detected."

# ── Virtual Environment ───────────────────────────────────────────────────────
echo ""
if [ ! -d "venv" ]; then
    echo "[1/4] Creating Python virtual environment..."
    python3 -m venv venv
    ok "Virtual environment created."
else
    echo "[1/4] Virtual environment already exists."
fi

source venv/bin/activate
ok "Virtual environment activated."

# ── Install Dependencies ──────────────────────────────────────────────────────
echo ""
echo "[2/4] Installing Python dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
ok "Dependencies installed."

# ── Pull Ollama Models ────────────────────────────────────────────────────────
echo ""
echo "[3/4] Pulling Ollama models (skipped if already downloaded)..."
ollama pull llama3.1:8b
ollama pull nomic-embed-text
ok "Models ready."

# ── Launch App ───────────────────────────────────────────────────────────────
echo ""
echo "[4/4] Launching PrivateDoc RAG..."
echo "      → Open http://localhost:8501 in your browser"
echo ""
streamlit run app.py --server.headless false --browser.gatherUsageStats false
