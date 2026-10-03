import os
import re
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from database import init_db, save_analysis, get_history
from ai_service import predict

app = FastAPI(title="RakshaAI API", version="1.0.0")
init_db()

origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=5000)

    @field_validator("text")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 5:
            raise ValueError("Text must contain at least 5 characters")
        return v


RULES = [
    ("Guaranteed/unrealistic return", 30,
     r"double your money|guaranteed|assured return|100% (profit|return)|risk[- ]free"
     r"|paisa double|paise double|pakka munafa|100% munafa|dugna"),
    ("OTP/PIN request", 30,
     r"\botp\b|\bpin\b|password|cvv|otp (batao|bhejo|share)|pin (batao|bhejo)"),
    ("Third-party payment", 25,
     r"(send|transfer|pay).*(to this|account|upi)"),
    ("Suspicious link", 20, r"https?://|bit\.ly|t\.me/"),
    ("Urgency", 15,
     r"immediately|urgent|today only|hurry|limited slots|last chance"
     r"|turant|jaldi|abhi (pay|bhejo|transfer)|aakhri mauka"),
    ("Social-media solicitation", 10,
     r"whatsapp|telegram|join (our )?group"),
]

RECOMMENDATIONS = {
    "LOW": "No major warning signs found, but still verify the source before acting.",
    "VERIFY": "Some warning signs found. Verify the sender and platform on official sites before sending money.",
    "HIGH": "Do not pay or share OTP/PIN. Verify with SEBI/RBI official sources and report suspected fraud at cybercrime.gov.in or call 1930.",
}


def run_risk_engine(text: str, ml_prob=None):
    score, flags = 0, []
    for name, points, pattern in RULES:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            score += points
            flags.append(name)
    if ml_prob is not None and ml_prob > 0.5:
        score += round((ml_prob - 0.5) * 2 * 25)
        if ml_prob >= 0.75:
            flags.append("Similar to known scam messages (ML model)")
    score = min(score, 100)
    level = "LOW" if score < 30 else "VERIFY" if score < 60 else "HIGH"
    return level, score, flags


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        ml_prob = predict(req.text)
        level, score, flags = run_risk_engine(req.text, ml_prob)
        confidence = round(ml_prob, 2) if ml_prob is not None else None
    except Exception as e:
        print("Analyze error:", e)
        raise HTTPException(status_code=500, detail="Analysis failed. Please try again.")

    try:
        save_analysis(req.text, level, score, confidence, flags)
    except Exception as e:
        print("Database error (analysis still returned):", e)

    return {
        "success": True,
        "risk": level,
        "risk_score": score,
        "confidence": confidence,
        "reasons": flags,
        "red_flags": flags,
        "recommendation": RECOMMENDATIONS[level],
    }


@app.get("/history")
def history(limit: int = 20, x_admin_key: str = Header(None)):
    admin_key = os.getenv("ADMIN_KEY")
    if not admin_key or x_admin_key != admin_key:
        raise HTTPException(status_code=404)
    return get_history(min(limit, 100))