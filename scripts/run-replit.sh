#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
npm ci --no-audit --no-fund
# Replit's system Python is read-only. Keep dependencies in its project package
# directory without creating a virtual environment or modifying the Nix store.
uv pip install --target .pythonlibs/lib/python3.12/site-packages -r requirements.txt
VITE_BACKEND_ENABLED=true npm run build
exec python -m backend.main
