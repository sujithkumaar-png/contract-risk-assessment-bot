import pytest
from contract_risk.risk_engine import analyze_contract, classify_risk

pytestmark = pytest.mark.unit

def test_original_sample_contract_returns_score_eight():
    text = (
        "This agreement includes a termination without notice clause. "
        "The party agrees to unlimited liability for damages. "
        "Confidentiality must be maintained. "
        "All disputes will be resolved by arbitration under Indian law."
    )
    result = analyze_contract(text)
    assert result.score == 8
    assert result.overall_risk == "High Risk"
    assert [(f.clause, f.level) for f in result.findings] == [
        ("termination without notice", "High"),
        ("unlimited liability", "High"),
        ("confidentiality", "Low"),
        ("arbitration", "Low"),
    ]

@pytest.mark.parametrize(("text", "score", "risk"), [
    ("", 0, "Low Risk"),
    ("CONFIDENTIALITY", 1, "Low Risk"),
    ("indemnity", 2, "Low Risk"),
    ("termination without notice", 3, "Low Risk"),
    ("indemnity late payment", 4, "Medium Risk"),
    ("indemnity auto renewal late payment", 6, "Medium Risk"),
    ("unlimited liability termination without notice penalty for breach", 9, "High Risk"),
])
def test_scoring_and_classification(text, score, risk):
    result = analyze_contract(text)
    assert result.score == score
    assert result.overall_risk == risk


def test_same_phrase_is_counted_once():
    result = analyze_contract("unlimited liability; unlimited liability")
    assert result.score == 3
    assert result.detected_count == 1


def test_non_string_input_is_rejected():
    with pytest.raises(TypeError):
        analyze_contract(None)

@pytest.mark.parametrize(("score", "expected"), [
    (0, "Low Risk"), (3, "Low Risk"), (4, "Medium Risk"),
    (6, "Medium Risk"), (7, "High Risk"),
])
def test_classification_boundaries(score, expected):
    assert classify_risk(score) == expected


def test_negative_score_is_rejected():
    with pytest.raises(ValueError):
        classify_risk(-1)
