# Test execution report

Recorded 2026-11-16, Asia/Calcutta, Windows 11, Python 3.14.6.
These are actual observations; rerun README commands for current evidence.

| Check | Result |
| --- | --- |
| Original baseline | 20 passed in 0.79s; Starlette and cache-write warnings |
| Requirements installation | Success in existing .venv, including httpx2 |
| Editable installation | Normal isolated build/install succeeded |
| pip check | No broken requirements found |
| compileall src tests scripts | Exit 0 |
| Unit tests separately | 16 passed in 0.06s |
| API tests separately | 13 passed in 0.68s |
| Full suite, HTML and JUnit | 35 passed in 3.92s, no warnings |
| Uvicorn module startup | Success and real HTTP requests verified |
| Uvicorn --reload | Reloader/worker started; /health 200 and expected JSON |
| Streamlit startup | Health and homepage shell HTTP 200 |
| Streamlit behavior | Six AppTest cases passed within full suite |
| PowerShell helper execution | Blocked by existing script execution policy |
| Browser installation/E2E | Not executed; no browser tests implemented |

## API evidence

Temporary loopback servers were used by scripts/verify_services.py. GET /health
returned 200 and {"status":"ok"}; Swagger /docs returned 200. Analysis requests:

- Sample/multiple clauses: 200, four findings, score 8, High Risk.
- Empty string: 422, string_too_short at body.contract_text.
- Missing field: 422, missing at body.contract_text.
- Numeric text: 422, string_type at body.contract_text.
- No matches: 200, empty findings, score/count zero, Low Risk.

In-process API tests additionally checked null, boolean, list, object, malformed
JSON, case-insensitivity, repeated phrases, exact response structure and existing
whitespace acceptance. Original boundary tests at 0, 3, 4, 6, 7 and negative-score
rejection remain intact.

## Streamlit evidence

AppTest verified title/input, empty and whitespace validation, text entry and
Analyze button interaction, all four sample findings, score 8/High Risk,
no matches with score 0/Low Risk and score 4/Medium Risk. No AppTest exceptions.
HTTP verifies the homepage shell; AppTest verifies the Python widget tree.
Neither proves browser rendering or end-to-end browser behavior.

## Artifacts

- reports/pytest-report.html: generated self-contained HTML report.
- reports/pytest-results.xml: generated JUnit results.
- reports/api-startup.log and streamlit-startup.log: real-server logs.
- requirements-verified.txt: recorded installed dependency versions.

Reports/logs are generated artifacts ignored by Git. No screenshots or browser
traces were generated.

## Resolved issues and remaining limitations

Starlette warning resolved through documented httpx2 dependency; cache warning
resolved by relocating cache. Initial sandbox pip network access failed; approved
elevated pip succeeded. A --no-build-isolation editable attempt failed because
runtime setuptools was absent; normal isolated editable installation succeeded.

No test warnings remain in the recorded full suite. PowerShell scripts remain
policy-blocked; direct Python commands work. Exact uvicorn.exe blocking rule is
unconfirmed. No fresh-venv, cross-platform or browser execution was performed.
No .git metadata was supplied, and no commit was created.
