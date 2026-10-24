#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

npm ci --no-audit --no-fund
# Use the existing project package target, not the read-only Nix Python prefix.
uv pip install --target .pythonlibs/lib/python3.12/site-packages -r requirements.txt
VITE_BACKEND_ENABLED=true npm run build
