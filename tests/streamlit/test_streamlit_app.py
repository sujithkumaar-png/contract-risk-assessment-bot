from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

pytestmark = pytest.mark.streamlit
APP = Path(__file__).resolve().parents[2] / "src" / "contract_risk" / "streamlit_app.py"


@pytest.fixture
def ui():
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    return app


def test_homepage_loads(ui):
    assert "Contract Analysis" in ui.title[0].value
    assert ui.text_area[0].label == "Paste Contract Text Below"


@pytest.mark.parametrize("text", ["", "   "])
def test_empty_input_shows_validation(ui, text):
    ui.text_area[0].input(text)
    ui.button[0].click().run()
    assert not ui.exception
    assert ui.warning[0].value == "Please paste contract text to analyze."
    assert not ui.info


def test_sample_analysis_displays_findings_score_and_classification(ui, sample_contract):
    ui.text_area[0].input(sample_contract)
    ui.button[0].click().run()
    assert not ui.exception
    assert ui.info[0].value == "Total Risk Score: **8**"
    assert ui.error[0].value == "High Risk"
    findings = [item.value for item in ui.markdown if "point(s)" in item.value]
    assert len(findings) == 4
    for phrase in ["termination without notice", "unlimited liability", "confidentiality", "arbitration"]:
        assert any(phrase in finding for finding in findings)


@pytest.mark.parametrize(("text", "score", "risk"), [
    ("Ordinary delivery terms.", 0, "Low Risk"),
    ("indemnity late payment", 4, "Medium Risk"),
])
def test_other_risk_results(ui, text, score, risk):
    ui.text_area[0].input(text)
    ui.button[0].click().run()
    assert not ui.exception
    assert ui.info[0].value == f"Total Risk Score: **{score}**"
    assert (ui.success if risk == "Low Risk" else ui.warning)[0].value == risk
    if score == 0:
        assert any(item.value == "No risky clauses detected." for item in ui.markdown)
