# Running BridgeNext on Replit

The project root is the directory containing `package.json`, `backend/`, and
`scripts/run-replit.sh`.

## Run in Preview

Use the Replit Run button. The `Start application` workflow runs
`PORT=5000 bash scripts/run-replit.sh`. It installs the locked Node and Python
dependencies, builds the React app with `VITE_BACKEND_ENABLED=true`, then starts
FastAPI on port 5000. FastAPI serves both the built `dist/` frontend and `/api/*`
from the same origin.

The Replit environment uses Node.js 24 and Python 3.12. Python dependencies are
installed with `uv` into Replit's `.pythonlibs` project package directory, not
the read-only system interpreter. To run manually:

```sh
PORT=5000 bash scripts/run-replit.sh
```

The production settings in `.replit` build the frontend and start FastAPI on its
default port 5000, mapped to external HTTP port 80. Preview uses this same mapping.
The shared Replit environment sets `PIP_USER=false` and
`PIP_TARGET=.pythonlibs/lib/python3.12/site-packages`. Local managed pip
installation succeeds with these settings. They are available to production,
but the hosted preliminary installer has still failed with a disabled-user-site
error; publishing is not yet verified. The explicit deployment build installs
dependencies with `uv`, but cannot run until that earlier phase succeeds.

## Optional AI integration

The questionnaire, matching, career recommendations, and learning pathways work
without an AI credential. Gemini-powered skill suggestions are optional and are
not connected by default. To enable them, connect Replit AI Integrations for
Gemini and configure the server-side Secrets `AI_INTEGRATIONS_GEMINI_API_KEY`
and `AI_INTEGRATIONS_GEMINI_BASE_URL` with the values provided by that
integration. Never put these values in frontend variables or source files.

## Publishing and data

The current interface uses a browser-session-only test prototype; it does not
save profiles or pathways to a persistent account. Publishing can use an
Autoscale deployment for this preliminary prototype. Before enabling real
account saves, configure durable storage for the backend SQLite data; local
deployment files should not be treated as durable account storage. The
in-process evidence refresh also only runs while the server instance is awake.
