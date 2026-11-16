# Phase 1 acceptance

Verified 2026-11-16 on Windows 11 / Python 3.14.6.

| Criterion | Evidence | Status |
| --- | --- | --- |
| Original scoring/sample | Original tests plus live HTTP: 4 findings, 8, High Risk | Pass |
| Health, valid analysis and response structure | TestClient and live server requests | Pass |
| Empty/missing/invalid API inputs | 422 assertions including malformed JSON | Pass |
| Multiple clauses/no matches | Exact response assertions and live checks | Pass |
| Streamlit startup/homepage | Health and homepage shell HTTP 200 | Pass |
| Widget input, validation, findings, score, classification | Six AppTest cases covering all risk classes | Pass |
| Preserve original tests | All original 20 retained; full suite 35 passed, no warnings | Pass |
| Compile/dependencies | compileall, requirements install, editable build, pip check | Pass |
| Module-based Uvicorn reload | Reloader/worker started; health 200 | Pass |
| Playwright foundation | Fixtures, POM and artifact plan | Prepared only |

Recommendation: ready to close Phase 1 for these acceptance criteria. AppTest
is not real-browser automation. Browser rendering, screenshots/traces and browser
journeys are deferred. Phase 2 has not started.

Significant changes: TestClient now closes through a fixture; added meaningful
negative/exact-JSON tests and shared sample-driven Streamlit tests. Unit/API markers
now work. Cache moved to reports/ because the supplied cache was unwritable.
Added Starlette's documented httpx2 dependency without downgrades or warning
suppression; retained HTTPX for live verification. Added developer scripts,
version snapshot and documentation. Application source and scoring are unchanged.

Environmental limitations: .ps1 scripts are blocked; direct interpreter commands
work. The precise reported uvicorn.exe blocking policy is unknown. No security
controls were modified. No Git metadata exists in this directory, so no commit
or Git diff was possible.

Suggested commits in a Git checkout:

- fix: add documented Starlette TestClient dependency
- test: extend API validation and Streamlit interaction coverage
- chore: add Windows commands and Playwright foundation
- docs: record Phase 1 verification and environment constraints
