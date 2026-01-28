import streamlit as st
from risk_rules import analyze_contract

st.set_page_config(page_title="Contract Risk Assessment Bot", layout="centered")

st.title("📄 Contract Analysis & Risk Assessment Bot")
st.write("Analyze contracts and identify potential legal risks using rule-based logic.")

contract_text = st.text_area(
    "Paste Contract Text Below 👇",
    height=250,
    placeholder="Paste your contract content here..."
)

if st.button("Analyze Contract"):
    if contract_text.strip() == "":
        st.warning("Please paste contract text to analyze.")
    else:
        findings, score, risk = analyze_contract(contract_text)

        st.subheader("🔍 Detected Risky Clauses")
        if findings:
            for clause, level in findings:
                st.write(f"- **{clause}** → {level}")
        else:
            st.write("No risky clauses detected.")

        st.subheader("📊 Risk Score")
        st.info(f"Total Risk Score: **{score}**")

        st.subheader("⚠️ Overall Risk Level")
        if risk == "High Risk":
            st.error(risk)
        elif risk == "Medium Risk":
            st.warning(risk)
        else:
            st.success(risk)

st.markdown("---")
st.caption("Built for GUVI Career Carnival Hackathon 2026")
