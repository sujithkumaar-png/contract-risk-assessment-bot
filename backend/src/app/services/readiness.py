"""Check the only required runtime service: the existing in-process risk engine."""
from contract_risk.risk_engine import analyze_contract


def check_risk_engine() -> bool:
    try:
        result = analyze_contract("confidentiality")
        return result.score == 1 and result.detected_count == 1 and result.overall_risk == "Low Risk"
    except Exception:
        return False
