"""Deterministic, rule-based contract risk analysis.

This engine intentionally preserves the original project's configured keywords,
weights, and score thresholds. It is a keyword detector, not a legal interpreter.
"""
from dataclasses import dataclass
from typing import Literal

RiskLevel = Literal["High", "Medium", "Low"]

RISK_RULES: dict[RiskLevel, tuple[str, ...]] = {
    "High": (
        "termination without notice",
        "unlimited liability",
        "non compete",
        "exclusive agreement",
        "penalty for breach",
    ),
    "Medium": (
        "indemnity",
        "auto renewal",
        "late payment",
        "service level agreement",
    ),
    "Low": (
        "confidentiality",
        "arbitration",
        "governing law",
        "jurisdiction",
    ),
}
WEIGHTS: dict[RiskLevel, int] = {"High": 3, "Medium": 2, "Low": 1}

@dataclass(frozen=True)
class Finding:
    clause: str
    level: RiskLevel
    points: int

@dataclass(frozen=True)
class AnalysisResult:
    findings: tuple[Finding, ...]
    score: int
    overall_risk: str

    @property
    def detected_count(self) -> int:
        return len(self.findings)


def classify_risk(score: int) -> str:
    """Classify a non-negative score using the original thresholds."""
    if score < 0:
        raise ValueError("score must be non-negative")
    if score <= 3:
        return "Low Risk"
    if score <= 6:
        return "Medium Risk"
    return "High Risk"


def analyze_contract(text: str) -> AnalysisResult:
    """Find configured phrases (case-insensitive) and calculate weighted score.

    Each configured phrase contributes at most once, matching the original
    implementation. Punctuation and hyphen variants are not normalized yet.
    """
    if not isinstance(text, str):
        raise TypeError("contract text must be a string")
    normalized = text.lower()
    findings: list[Finding] = []
    score = 0
    for level, phrases in RISK_RULES.items():
        for phrase in phrases:
            if phrase in normalized:
                points = WEIGHTS[level]
                findings.append(Finding(clause=phrase, level=level, points=points))
                score += points
    return AnalysisResult(
        findings=tuple(findings),
        score=score,
        overall_risk=classify_risk(score),
    )
