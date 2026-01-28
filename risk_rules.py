RISK_RULES = {
    "High": [
        "termination without notice",
        "unlimited liability",
        "non compete",
        "exclusive agreement",
        "penalty for breach"
    ],
    "Medium": [
        "indemnity",
        "auto renewal",
        "late payment",
        "service level agreement"
    ],
    "Low": [
        "confidentiality",
        "arbitration",
        "governing law",
        "jurisdiction"
    ]
}

WEIGHTS = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

def analyze_contract(text):
    text = text.lower()
    findings = []
    score = 0

    for level, keywords in RISK_RULES.items():
        for keyword in keywords:
            if keyword in text:
                findings.append((keyword, level))
                score += WEIGHTS[level]

    if score <= 3:
        overall_risk = "Low Risk"
    elif score <= 6:
        overall_risk = "Medium Risk"
    else:
        overall_risk = "High Risk"

    return findings, score, overall_risk
