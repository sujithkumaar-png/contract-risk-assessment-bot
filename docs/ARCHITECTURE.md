# Platform foundation architecture

## Repository inspection and migration

Starting HEAD: `04bf4b0`, following original Phase 1 commit `f97c637`. Clean working
tree; 35 existing tests passed before changes.

- `src/contract_risk/risk_engine.py`: canonical deterministic engine, unchanged.
  Weights 3/2/1, thresholds 0-3 / 4-6 / 7+, each phrase once, case-insensitive.
- `src/contract_risk/api.py`: existing FastAPI /health and /api/v1/analyze,
  unchanged, including its Pydantic models.
- `src/contract_risk/streamlit_app.py`: existing UI calls engine directly, unchanged.
- Root tests: unit, API and Streamlit AppTest; existing Playwright foundation has
  no browser cases. All existing tests are unchanged.
- Root requirements, verified dependency snapshot and historical documentation:
  preserved. Existing setup and entry points continue to work.

Migration is additive: new frontend and backend composition packages. The new
backend includes the legacy router, reusing analysis without copying the engine.
Install the root package before backend. No source moves, destructive migration,
history rewrite, commit or push. Later relocation requires an import compatibility
layer and the same regression suite; it is not part of this milestone.

## Boundaries

```text
frontend/src/app/          Next.js App Router, layout, landing page, Tailwind CSS
frontend/src/components/   site header
frontend/src/lib/          static presentation data
frontend/src/services/     reserved typed API clients (documented, not implemented)
frontend/src/types/        reserved API types (documented, not implemented)
frontend/public/           static assets boundary
backend/src/app/api/       health routes
backend/src/app/core/      configuration and JSON logging
backend/src/app/database/  reserved SQLAlchemy engine/session boundary
backend/src/app/models/    reserved SQLAlchemy models
backend/src/app/schemas/   platform response contracts
backend/src/app/services/  in-process risk engine readiness
backend/src/app/modules/   reserved future domain organization
backend/src/app/main.py    factory, lifespan, request IDs, legacy router composition
backend/tests/             unit, api and integration checks
src/contract_risk/         existing canonical engine, API, Streamlit UI
tests/                    existing regression suite
```

The static landing page makes no API requests and labels its sample illustration.
No login, upload or interactive assessment workflow is implemented. System fonts
avoid external font downloads. Tailwind v4 uses @tailwindcss/postcss; shadcn/ui
will be introduced when interactive components are needed.
Setup follows the [Next.js App Router guide](https://nextjs.org/docs/app/getting-started/installation)
and [Tailwind Next.js guide](https://tailwindcss.com/docs/installation/framework-guides/nextjs).

## Health, configuration and observability

Settings use Pydantic and process environment. APP_ENV allows development/test/
production (default development); LOG_LEVEL allows DEBUG/INFO/WARNING/ERROR/
CRITICAL (default INFO). Supplied invalid values stop app creation with field
names only. No required credential or external dependency exists yet. .env loading
is explicit via Uvicorn --env-file, not implicit.

GET /api/v1/health/live returns 200 when the running process handles the request,
independent of engine/database status. GET /api/v1/health/ready checks lifespan
startup completion and the risk engine with a known phrase. Both must pass for
200; otherwise 503/not_ready. Database is explicitly not_configured and is not a
required dependency yet. Future integration must add a required connectivity check.
Both return status, check, request_id and dependencies.

X-Request-ID is returned on all HTTP responses. Incoming IDs of 1-64 ASCII letters,
digits, underscore or hyphen are retained; other values become UUIDs. IDs provide
correlation, not identity. Existing analysis/validation JSON remains compatible.
Unexpected errors use a generic 500 response with request ID. JSON application
logs contain event, timestamp, method, route template, status, duration and request
ID, omitting bodies, query strings and arbitrary exception values. Uvicorn lifecycle
logs remain standard server logs. Setup commands disable its separate access log
to avoid duplicate query-bearing output.

## Later milestones

SQLAlchemy installation/session integration, Neon, Alembic, Clerk, authorization,
API clients, CORS integration and new Playwright tests remain deferred. Reserved
packages do not create tables, connections, migrations or claim database readiness.
No authentication broker exists. No Docker, Redis, Celery or Kubernetes.

Use one shared Python venv, one backend and one frontend. Do not run legacy
Streamlit alongside them unless testing it. The production build uses Webpack
and a single page-data worker to limit concurrency on an 8 GB laptop; memory
consumption was not benchmarked.
