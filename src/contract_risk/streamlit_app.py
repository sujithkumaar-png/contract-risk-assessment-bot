"""Streamlit user interface for the contract risk engine."""
import streamlit as st
from contract_risk.risk_engine import analyze_contract

st.set_page_config(page_title="Contract Risk Assessment Bot", layout="centered")
st.title("📄 Contract Analysis & Risk Assessment Bot")
st.write("Identify configured risk-related phrases and calculate a weighted score.")
contract_text = st.text_area(
    "Paste Contract Text Below", height=250,
    placeholder="Paste your contract content here..."
)
if st.button("Analyze Contract", type="primary"):
    if not contract_text.strip():
        st.warning("Please paste contract text to analyze.")
    else:
        result = analyze_contract(contract_text)
        st.subheader("🔍 Detected Risky Clauses")
        if result.findings:
            for finding in result.findings:
                st.write(f"- **{finding.clause}** → {finding.level} ({finding.points} point(s))")
        else:
            st.write("No risky clauses detected.")
        st.subheader("📊 Risk Score")
        st.info(f"Total Risk Score: **{result.score}**")
        st.subheader("⚠️ Overall Risk Level")
        if result.overall_risk == "High Risk":
            st.error(result.overall_risk)
        elif result.overall_risk == "Medium Risk":
            st.warning(result.overall_risk)
        else:
            st.success(result.overall_risk)
st.markdown("---")
st.caption("Automation Testing Portfolio Project | Rule-based demo — not legal advice.")
