#!/bin/zsh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
else
  source venv/bin/activate
fi

echo "Starting backend at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo "Press CTRL+C to stop."
echo ""

uvicorn main:app --reload
