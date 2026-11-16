# Browser automation foundation (not executed)

pytest-playwright provides `browser`, isolated `context`, and `page` fixtures.
The local conftest supplies the viewport and UI_BASE_URL, defaulting to localhost:8501.
Start Streamlit separately before running browser tests.

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe -m pytest tests/ui --browser chromium --screenshot only-on-failure --tracing retain-on-failure --output test-results
```

There are no browser test cases yet; this directory currently collects zero tests
(pytest returns exit code 5). Browser installation and browser execution are deferred.
The screenshot/trace strategy above uses the plugin's built-in failure artifacts.
Future tests must use its `page` fixture to receive those artifacts.

Planned Page Object Model: `tests/ui/pages/contract_page.py` will expose open,
enter_contract, analyze, findings, score, and classification operations. Prefer
get_by_role/get_by_label locators and Playwright web-first assertions; avoid sleeps
and generated Streamlit CSS classes. Planned journeys cover empty text, sample
analysis, no matches, and replacing previously analyzed text. Add and execute
these only in the browser-automation phase after Phase 1 approval.
