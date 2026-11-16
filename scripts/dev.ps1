param(
    [ValidateSet('install', 'api', 'streamlit', 'test', 'unit', 'api-tests', 'report', 'browsers')]
    [string]$Task = 'test'
)
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
# Use an activated environment when present, otherwise the repository environment.
$Python = if ($env:VIRTUAL_ENV) { Join-Path $env:VIRTUAL_ENV 'Scripts\python.exe' } else { Join-Path $ProjectRoot '.venv\Scripts\python.exe' }
if (-not (Test-Path -LiteralPath $Python)) { throw 'Create .venv with python -m venv .venv first.' }
function Invoke-Python {
    & $Python @args
    if ($LASTEXITCODE -ne 0) { throw "Python command failed with exit code $LASTEXITCODE" }
}
Push-Location $ProjectRoot
try {
    switch ($Task) {
        'install' { Invoke-Python -m pip install -r requirements.txt; Invoke-Python -m pip install -e .; Invoke-Python -m pip check }
        'api' { Invoke-Python -m uvicorn contract_risk.api:app --reload --app-dir src --host 127.0.0.1 }
        'streamlit' { Invoke-Python -m streamlit run src/contract_risk/streamlit_app.py --server.address 127.0.0.1 }
        'test' { Invoke-Python -m pytest -v }
        'unit' { Invoke-Python -m pytest tests/unit -v }
        'api-tests' { Invoke-Python -m pytest tests/api -v }
        'report' { Invoke-Python -m pytest -v --html=reports/pytest-report.html --self-contained-html --junitxml=reports/pytest-results.xml }
        'browsers' { Invoke-Python -m playwright install chromium }
    }
} finally { Pop-Location }
