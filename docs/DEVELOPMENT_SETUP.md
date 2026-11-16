# Platform foundation setup

PowerShell commands below start at repository root. Tested: Windows 11, Python
3.14.6, Node.js 24.19.0, npm 11.17.0. Next.js 16 requires Node >=20.9; use a
supported Node LTS. npm.cmd works without changing the policy blocking npm.ps1.

## Install

Reuse .venv. Only if missing, run `python -m venv .venv` first.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip install -e ./backend
.\.venv\Scripts\python.exe -m pip check
Set-Location frontend
npm.cmd ci --no-fund
Set-Location ..
```

Install the local root package first: backend depends on it to reuse the engine.
Do not fetch a similarly named package from a registry. One shared venv is used.
Root requirements and requirements-verified.txt are unchanged; the latter remains
the original snapshot, not a new platform lock. No new Python runtime dependency
or database driver was added. package-lock.json records frontend resolution.

## Configuration and startup

No credentials or .env files are required locally. Optional copies (only if absent):

```powershell
Copy-Item backend/.env.example backend/.env
Copy-Item frontend/.env.example frontend/.env.local
```

APP_ENV: development (default), test, production. LOG_LEVEL: INFO (default), DEBUG,
WARNING, ERROR, CRITICAL. Invalid values fail safely without echoing input.
Backend reads process environment; add `--env-file backend/.env` to Uvicorn to
load a copied file explicitly. Frontend NEXT_PUBLIC_API_BASE_URL is reserved for
future API integration and currently unused. NEXT_PUBLIC_* is public; never put
credentials there. No Neon, Clerk or DATABASE_URL is required. Env files are ignored.

Terminal 1, root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend/src --host 127.0.0.1 --port 8000 --no-access-log
```

Terminal 2, root:

```powershell
Set-Location frontend
npm.cmd run dev
```

Frontend: http://127.0.0.1:3000. Backend docs: http://127.0.0.1:8000/docs.
Health endpoints on backend: /api/v1/health/live and /api/v1/health/ready.
Legacy /health and /api/v1/analyze remain available too. Stop servers with Ctrl+C.
Optional backend --reload adds a watcher; default commands omit it to reduce
process use. Do not run extra legacy servers while using the platform.

To serve a production frontend, stop dev, then from frontend:

```powershell
npm.cmd run build
npm.cmd run start
```

Both dev and start use port 3000; run only one. No Windows security settings need
changing. If policy blocks approved interpreters/downloads, ask IT for an approved
environment or mirror; do not use execution-policy bypass flags.

## Checks

From root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m pytest backend/tests -q
.\.venv\Scripts\python.exe -m compileall -q src backend/src backend/tests scripts
.\.venv\Scripts\python.exe -m pip check
Set-Location frontend
npm.cmd run typecheck
npm.cmd run build
Set-Location ..
.\.venv\Scripts\python.exe scripts/verify_platform.py
git status --short
git diff --check
```

Root Pytest discovers both suites. The smoke script needs installed packages and
a completed frontend build. It starts backend then frontend on temporary loopback
ports, sequentially, checks HTTP and stops both. Ignored reports/platform-*.log
capture server output. This checks HTTP, not browser rendering.

## Actual verification, 2026-11-16

| Check | Observed result |
| --- | --- |
| Existing suite before edits | 35 passed in 3.96s |
| Combined suite after changes | 52 passed in 3.26s, no warnings |
| Backend editable install | Passed |
| pip check | No broken requirements found |
| Python compileall | Exit 0 |
| npm install | 48 packages added; audit reported zero vulnerabilities |
| Frontend versions | Next 16.4.6, React/React DOM 19.3.1, Tailwind/PostCSS plugin 4.3.5, TypeScript 5.9.3 |
| npm run typecheck | Passed: route type generation and tsc |
| npm run build | Passed: static homepage and not-found routes |
| Live backend | Both probes 200, request IDs correlated, database not_configured |
| Legacy API through platform | Sample 4 findings, score 8, High Risk; old /health preserved |
| Frontend production HTTP | 200; landing content and asset references present |
| New browser tests / visual inspection | Not executed; deferred |

Initial npm/pip requests were sandbox-blocked; approved elevated installation
succeeded. No security settings changed. A fresh Python venv and other OS/runtime
combinations were not tested. Audit results describe installation time only.
No lint tool was installed; typechecking/build do not claim lint coverage.

## Manual verification checklist

- [ ] Open backend /docs and inspect legacy analysis and new health routes.
- [ ] GET live: ok/liveness, request_id, empty dependencies.
- [ ] GET ready: startup/risk_engine ok, database not_configured.
- [ ] Send X-Request-ID: manual-check; compare response header/body and JSON logs.
- [ ] Analyze test-data/sample_contract.txt: four findings, score 8, High Risk.
- [ ] Review frontend at desktop/mobile widths and navigate using keyboard.
- [ ] Check skip link, approach/roadmap anchors and static-sample label.
- [ ] Confirm no login/upload/live assessment workflow is claimed.
- [ ] In a separate shell, verify invalid APP_ENV fails without echoing its value.
- [ ] Stop servers; review diff/status for env files or generated output.
- [ ] Review foundation before starting the next milestone.

## Exact file inventory

Modified: `.gitignore`, root `pyproject.toml`, `README.md`.
Legacy source, tests, documentation and dependency files are unchanged. No commit,
push, reset or history rewrite was performed.

Created:

```text
backend/.env.example
backend/pyproject.toml
backend/src/app/__init__.py
backend/src/app/main.py
backend/src/app/api/__init__.py
backend/src/app/api/health.py
backend/src/app/core/__init__.py
backend/src/app/core/config.py
backend/src/app/core/logging.py
backend/src/app/database/__init__.py
backend/src/app/models/__init__.py
backend/src/app/modules/__init__.py
backend/src/app/schemas/__init__.py
backend/src/app/schemas/health.py
backend/src/app/services/__init__.py
backend/src/app/services/readiness.py
backend/tests/conftest.py
backend/tests/api/test_platform_health.py
backend/tests/integration/test_legacy_routes.py
backend/tests/unit/test_configuration.py
backend/tests/unit/test_structured_logging.py
frontend/.env.example
frontend/next-env.d.ts
frontend/next.config.ts
frontend/package.json
frontend/package-lock.json
frontend/postcss.config.mjs
frontend/tsconfig.json
frontend/public/README.md
frontend/src/app/globals.css
frontend/src/app/layout.tsx
frontend/src/app/page.tsx
frontend/src/components/site-header.tsx
frontend/src/lib/platform.ts
frontend/src/services/README.md
frontend/src/types/README.md
docs/ARCHITECTURE.md
docs/DEVELOPMENT_SETUP.md
scripts/verify_platform.py
```

Local node_modules, .next, egg-info, caches and logs are generated/ignored. No
credential file was created. Existing historical Phase 1 reports remain intact.
