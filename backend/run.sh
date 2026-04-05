#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
REQUIREMENTS="$SCRIPT_DIR/requirements.txt"

# Check and create venv if not exists
if [ ! -d "$VENV_DIR" ]; then
    echo ">>> Virtual environment not found. Creating..."
    python3 -m venv "$VENV_DIR"
    echo ">>> Installing dependencies..."
    "$VENV_DIR/bin/pip" install --upgrade pip
    "$VENV_DIR/bin/pip" install -r "$REQUIREMENTS"
    echo ">>> Setup complete."
fi

# Activate venv
source "$VENV_DIR/bin/activate"

case "${1:-dev}" in
    dev)
        echo ">>> Starting DEV server (with reload)..."
        uvicorn main:app --reload --port 8000
        ;;
    prod)
        echo ">>> Starting PROD server..."
        uvicorn main:app --host 0.0.0.0 --port 8000
        ;;
    install)
        echo ">>> Installing/updating dependencies..."
        pip install --upgrade pip
        pip install -r "$REQUIREMENTS"
        ;;
    test)
        pytest tests/ -v
        ;;
    *)
        echo "Usage: ./run.sh [dev|prod|install|test]"
        echo "  dev     - Run with hot reload (default)"
        echo "  prod    - Run production server"
        echo "  install - Reinstall dependencies"
        echo "  test    - Run tests"
        exit 1
        ;;
esac
