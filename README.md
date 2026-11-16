# Contract Risk Assessment Bot

A Python automation-testing portfolio project with a deterministic phrase detector,
FastAPI API and Streamlit UI. Educational demo; not legal advice.

## Architecture and business rules

FastAPI and Streamlit both call `src/contract_risk/risk_engine.py`. The UI calls the
engine directly, not through the API. There is no database or external AI service.
High/Medium/Low findings contribute 3/2/1 points. Scores 0-3 are Low Risk, 4-6
Medium Risk, 7+ High Risk. Each phrase counts once, case-insensitively. The original
sample returns **4 findings, score 8, High Risk**. Application source is unchanged.

```text
src/contract_risk/       engine, API, Streamlit UI
tests/unit/             scoring and boundary tests
tests/api/              API contract and validation tests
tests/streamlit/        Streamlit AppTest widget interaction tests
tests/ui/               browser fixtures and POM plan; no browser tests
scripts/                developer tasks and live service verification
test-data/              original sample
docs/                   setup, acceptance and execution evidence
```

## Stack and installation

Verified: Windows 11, Python 3.14.6, FastAPI 0.163.1, Starlette 1.10.0,
Pydantic 2.14.3, Uvicorn 0.54.0, Streamlit 1.67.0, Pytest 8.4.2,
HTTPX 0.28.1, httpx2 2.16.2, Playwright 1.65.2, pytest-playwright 0.10.0.
Python >=3.10 is declared; other runtimes were not tested.

From repository root in PowerShell; activation is unnecessary:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m pip check
```

Keep an existing .venv rather than recreating it. For the recorded versions, add
`-c requirements-verified.txt` to the requirements installation command. That
snapshot is not a portable lock. Install requirements explicitly: dependencies
currently live in requirements.txt, not the package metadata.

## Startup

Run each in a separate terminal; stop with Ctrl+C:

```powershell
.\.venv\Scripts\python.exe -m uvicorn contract_risk.api:app --reload --app-dir src --host 127.0.0.1
.\.venv\Scripts\python.exe -m streamlit run src/contract_risk/streamlit_app.py --server.address 127.0.0.1
```

API docs: http://127.0.0.1:8000/docs ; UI: http://127.0.0.1:8501.
Use module commands instead of executable launchers. No security policy changes
are required. Optional scripts/dev.ps1 tasks: install, api, streamlit, test, unit,
api-tests, report, browsers. The helper selects active-venv Python or local .venv.
This machine blocks .ps1 execution, so use direct commands here.

## API documentation

GET `/health`: HTTP 200, `{"status":"ok"}`. OpenAPI: `/openapi.json`.
POST `/api/v1/analyze`: required non-empty string `contract_text`.

```json
{"contract_text":"termination without notice; unlimited liability; confidentiality; arbitration"}
```

HTTP 200 response:

```json
{"findings":[{"clause":"termination without notice","level":"High","points":3},{"clause":"unlimited liability","level":"High","points":3},{"clause":"confidentiality","level":"Low","points":1},{"clause":"arbitration","level":"Low","points":1}],"score":8,"overall_risk":"High Risk","detected_count":4}
```

No matches: empty findings, score/count zero, Low Risk. Empty, missing, non-string
input and malformed JSON return 422 with a `detail` array. Whitespace-only API
text remains accepted and scores zero; the UI rejects whitespace separately.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
$body = @{contract_text = Get-Content test-data/sample_contract.txt -Raw} | ConvertTo-Json
Invoke-RestMethod http://127.0.0.1:8000/api/v1/analyze -Method Post -ContentType 'application/json' -Body $body
```

## Verification commands

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m pytest tests/unit -v
.\.venv\Scripts\python.exe -m pytest tests/api -v
.\.venv\Scripts\python.exe -m pytest tests/streamlit -v
.\.venv\Scripts\python.exe -m pytest -v --html=reports/pytest-report.html --self-contained-html --junitxml=reports/pytest-results.xml
.\.venv\Scripts\python.exe -m compileall -q src tests scripts
.\.venv\Scripts\python.exe scripts/verify_services.py
```

The live check starts temporary loopback servers, checks HTTP responses, stops its
processes and writes startup logs under reports/.

Observed 2026-11-16: **35 passed in 3.92s, no warnings**: 16 unit, 13 API, six
Streamlit AppTest. All original 20 cases remain. Results describe this execution;
rerun for current evidence. See [execution report](docs/TEST_EXECUTION_REPORT.md).

## Limitations and roadmap

Literal substring detection does not understand negation, legal context, hyphens,
punctuation variants or equivalent wording. No uploads, persistence, authentication
or AI interpretation. Servers are for local development.

Phase 1 acceptance is verified with unit/API/AppTest and real service startup.
Browser rendering and end-to-end automation remain unverified. Playwright fixtures,
installation commands, failure screenshots/traces strategy and future POM planning
are in [tests/ui/README.md](tests/ui/README.md). No browser tests exist yet.
Next, after Phase 1 review: implement page objects and browser journeys, then CI.
No subsequent phase was started.

See [Phase 1](docs/PHASE_1.md) and [environment setup](docs/ENVIRONMENT_SETUP.md).
