#!/bin/bash

# Set working directories
BACKEND_DIR="./backend"
FRONTEND_DIR="./frontend"

# Start backend with hot reload
start_backend() {
  echo "🚀 Starting FastAPI backend with reload..."
  cd "$BACKEND_DIR"
  uvicorn app.main:app --reload --port 8001
}

# Start frontend
start_frontend() {
  echo "🌐 Starting frontend..."
  cd "$FRONTEND_DIR"
  npm run dev
}

# Show usage
usage() {
  echo "Usage: ./dev.sh [backend|frontend|both]"
}

# Main logic
case "$1" in
  backend)
    start_backend
    ;;
  frontend)
    start_frontend
    ;;
  both)
    echo "🔧 Starting both backend and frontend..."
    gnome-terminal -- bash -c "cd $BACKEND_DIR && uvicorn app.main:app --reload --port 8001; exec bash" &
    gnome-terminal -- bash -c "cd $FRONTEND_DIR && npm run dev; exec bash" &
    ;;
  *)
    usage
    ;;
esac
