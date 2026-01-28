# Contract Analysis & Risk Assessment Bot

## Problem Statement
Small and medium businesses often struggle to understand legal risks hidden inside complex contracts. This project provides a simplified risk assessment tool that highlights risky clauses and assigns an overall risk score.

## Solution Overview
This application analyzes contract text using rule-based logic to detect predefined risky clauses. Each detected clause contributes to a risk score which is used to classify the contract into Low, Medium, or High Risk.

## Key Features
- Clause detection using keyword matching
- Risk scoring system
- Overall contract risk classification
- Simple and intuitive UI built with Streamlit

## Tech Stack
- Python
- Streamlit

## How It Works
1. User pastes contract text
2. System detects risky clauses
3. Risk score is calculated
4. Overall risk level is displayed

## Assumptions
- Analysis is rule-based and explainable
- No external legal databases or APIs are used

## Future Enhancements
- NLP-based clause classification
- PDF/DOCX file upload
- LLM-powered explanation engine
