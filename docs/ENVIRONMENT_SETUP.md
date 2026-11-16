# Environment setup

Follow README.md for exact installation, startup and test commands. Use an
organization-approved Python installation. Verified here: Python 3.14.6 / Windows 11.
Activation is optional; explicit .venv Python commands avoid activation scripts.
An activated environment can instead use `python -m ...`.

Normal `python -m pip install -e .` uses the declared setuptools/wheel build tools
in an isolated build environment and succeeded. A trial with --no-build-isolation
failed because runtime setuptools was absent; do not use that option here.
Requirements were installed successfully in the existing venv. A fresh empty-venv
installation and other Python/OS combinations were not tested.

For recorded versions:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -c requirements-verified.txt
```

The snapshot is an observed environment, not a cross-platform lock.

## Application Control and PowerShell

The reported uvicorn.exe denial is an OS policy restriction, not an application
traceback. Its precise rule/signature decision requires IT policy/event logs and
was not established. Python module execution, including Uvicorn --reload, worked.
No launcher renaming, Defender changes or execution-policy changes were used.

The optional scripts/dev.ps1 selects active-venv Python or repository .venv and
propagates Python failures. Its execution is blocked by this machine's existing
PowerShell policy, so dynamic helper execution remains unverified. Use README's
direct interpreter commands. Do not use policy bypass flags.

If Python module execution is also prohibited, stop and ask IT to approve the
interpreter/dependencies or provide an approved development VM/container/runner.
No approval for an alternative environment is claimed. If package downloads are
blocked, request an approved package mirror or IT-provided wheels.

## Dependency compatibility

Verified: FastAPI 0.163.1, Starlette 1.10.0, Pydantic 2.14.3, Uvicorn 0.54.0,
Streamlit 1.67.0, HTTPX 0.28.1, httpx2 2.16.2, Pytest 8.4.2.
`pip check` found no broken requirements. Existing ranges were preserved.

Installed starlette/testclient.py prefers httpx2 and warns on fallback to httpx.
Adding httpx2 2.16.2 (httpcore2 2.16.2, truststore 0.10.5) removed that warning.
HTTPX remains used by live service checks. No warning filter was added.
References: [Starlette TestClient](https://starlette.dev/testclient/) and
[release notes](https://www.starlette.io/release-notes/).

## Browser preparation

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
```

Run on an approved machine with download access. Browser installation was not
executed in this task. See tests/ui/README.md for fixture setup, future page objects
and screenshot/trace commands. No browser test cases currently exist.
