#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
BACKEND="$ROOT/backend"
FRONTEND="$ROOT/frontend"

# ── colours ────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; NC='\033[0m'
info()  { echo -e "${GREEN}[medaudit]${NC} $*"; }
warn()  { echo -e "${YELLOW}[medaudit]${NC} $*"; }
error() { echo -e "${RED}[medaudit]${NC} $*"; exit 1; }

# ── cleanup on Ctrl+C ──────────────────────────────────────────────────────
PIDS=()
cleanup() {
  echo ""
  info "Shutting down..."
  for pid in "${PIDS[@]}"; do
    kill "$pid" 2>/dev/null || true
  done
  exit 0
}
trap cleanup INT TERM

# ── checks ─────────────────────────────────────────────────────────────────
command -v python3 &>/dev/null || error "python3 not found. Install Python 3.11+."
command -v node   &>/dev/null || error "node not found. Install Node.js 18+."
command -v npm    &>/dev/null || error "npm not found. Install Node.js 18+."

# ── .env ───────────────────────────────────────────────────────────────────
if [ ! -f "$ROOT/.env" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  warn ".env not found — copied from .env.example"
  warn "Add your CLAUDE_API_KEY to .env before using AI features."
fi

# ── Python venv ────────────────────────────────────────────────────────────
VENV="$BACKEND/.venv"
if [ ! -d "$VENV" ]; then
  info "Creating Python virtual environment..."
  python3 -m venv "$VENV"
fi

info "Installing/verifying backend dependencies..."
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$BACKEND/requirements.txt"

# ── frontend deps ──────────────────────────────────────────────────────────
if [ ! -d "$FRONTEND/node_modules" ]; then
  info "Installing frontend dependencies..."
  npm --prefix "$FRONTEND" install --silent
fi

# ── start backend ──────────────────────────────────────────────────────────
info "Starting backend on http://localhost:8000 ..."
cd "$BACKEND"
"$VENV/bin/uvicorn" app.main:app --host 0.0.0.0 --port 8000 --reload &
PIDS+=($!)
cd "$ROOT"

# give the backend a moment to start
sleep 2

# ── start frontend ─────────────────────────────────────────────────────────
info "Starting frontend on http://localhost:5173 ..."
npm --prefix "$FRONTEND" run dev &
PIDS+=($!)

echo ""
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "  Frontend : http://localhost:5173"
info "  Backend  : http://localhost:8000"
info "  API docs : http://localhost:8000/docs"
info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
info "Press Ctrl+C to stop."
echo ""

wait
