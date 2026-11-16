"""FastAPI endpoints for contract risk analysis."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from contract_risk.risk_engine import analyze_contract

app = FastAPI(
    title="Contract Risk Assessment API",
    description="Rule-based contract keyword detection and weighted risk scoring.",
    version="1.0.0",
)

class AnalyzeRequest(BaseModel):
    contract_text: str = Field(..., min_length=1, description="Contract text to analyze")

class FindingResponse(BaseModel):
    clause: str
    level: str
    points: int

class AnalyzeResponse(BaseModel):
    findings: list[FindingResponse]
    score: int
    overall_risk: str
    detected_count: int

@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/api/v1/analyze", response_model=AnalyzeResponse, tags=["Contract Analysis"])
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    result = analyze_contract(request.contract_text)
    return AnalyzeResponse(
        findings=[FindingResponse(clause=f.clause, level=f.level, points=f.points) for f in result.findings],
        score=result.score,
        overall_risk=result.overall_risk,
        detected_count=result.detected_count,
    )
