# 📄 Contract Analysis & Risk Assessment Bot

A Python-based application that analyzes contract text, identifies potentially risky clauses, calculates risk scores, and classifies contracts into Low, Medium, and High risk categories.

## 📌 Project Overview

Understanding legal contracts can be challenging, especially for small and medium-sized businesses.

This application provides a simple rule-based approach to identify predefined risky clauses in contract documents and generate an overall risk assessment.

## 🎯 Problem Statement

Contracts may contain clauses involving unlimited liability, termination conditions, penalties, indemnity, and automatic renewal.

Manually reviewing these clauses can be time-consuming.

This project aims to simplify the initial risk identification process through automated keyword-based analysis.

## ✨ Key Features

- Contract text input through a Streamlit interface.
- Automated keyword-based clause detection.
- High, Medium, and Low risk classification.
- Weighted risk score calculation.
- Overall contract risk assessment.
- User-friendly results display.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | User interface |
| Rule-based logic | Risk detection |
| Git & GitHub | Version control |

## 📂 Project Structure

```text
contract-risk-assessment-bot/
│
├── app.py
├── risk_rules.py
├── requirements.txt
├── sample_contract.txt
└── README.md
```

## ⚙️ Risk Assessment Logic

The application identifies predefined keywords under three risk categories.

### High Risk
- Termination without notice
- Unlimited liability
- Non-compete
- Exclusive agreement
- Penalty for breach

### Medium Risk
- Indemnity
- Auto renewal
- Late payment
- Service level agreement

### Low Risk
- Confidentiality
- Arbitration
- Governing law
- Jurisdiction

### Risk Scoring

| Risk Category | Weight |
|---|---:|
| High | 3 |
| Medium | 2 |
| Low | 1 |

### Overall Risk Classification

| Total Score | Classification |
|---|---|
| 0–3 | Low Risk |
| 4–6 | Medium Risk |
| 7 and above | High Risk |

## 🚀 Installation and Setup

### Prerequisites

- Python 3.x
- pip
- Git

### Step 1: Clone the repository

```bash
git clone https://github.com/sujithkumaar-png/contract-risk-assessment-bot.git
```

### Step 2: Navigate to the project

```bash
cd contract-risk-assessment-bot
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## 🧪 Application Workflow

1. Enter contract text in the input area.
2. Click the Analyze Contract button.
3. The application checks for predefined risk keywords.
4. Detected clauses are assigned risk weights.
5. The total risk score is calculated.
6. The overall risk classification is displayed.

## 🔍 Quality Assurance Scope

The following scenarios are identified for application validation:

- Empty contract submission.
- Valid contract analysis.
- High-risk keyword detection.
- Medium-risk keyword detection.
- Low-risk keyword detection.
- Uppercase and lowercase keyword handling.
- Multiple risk keyword combinations.
- Invalid and unexpected input handling.
- Risk score calculation validation.

## ⚠️ Current Limitations

- Uses predefined keyword matching rather than advanced legal-language understanding.
- Does not interpret the legal context of clauses.
- Does not provide professional legal advice.
- Risk results depend on the configured rules and scoring thresholds.

## 🔮 Future Enhancements

- Automated UI testing using Playwright.
- Unit testing using pytest.
- Improved keyword matching.
- Contract document upload support.
- Expanded test coverage and regression validation.
- Automated test reports and CI/CD integration.

## 👨‍💻 Author

**Sujith Kumaar K S**

QA Engineer | Aspiring QA Automation Engineer

- GitHub: https://github.com/sujithkumaar-png
- LinkedIn: https://www.linkedin.com/in/sujith-kumaar-8729b7311/

---

⭐ If you find this project interesting, feel free to explore the repository!
