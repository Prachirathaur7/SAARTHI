import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from database import init_db, save_analysis, get_history

app = FastAPI(title="RakshaAI API")
init_db()

# Tighten this to your Lovable URL before deploying
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=5, max_length=5000)

# (red flag, score contribution, regex pattern)
RULES = [
    ("Guaranteed/unrealistic return", 30,
     r"double your money|guaranteed|assured return|100% (profit|return)|risk[- ]free"),
    ("OTP/PIN request", 30, r"\botp\b|\bpin\b|password|cvv"),
    ("Third-party payment", 25, r"(send|transfer|pay).*(to this|account|upi)"),
    ("Suspicious link", 20, r"https?://|bit\.ly|t\.me/"),
    ("Urgency", 15, r"immediately|urgent|today only|hurry|limited slots|last chance"),
    ("Social-media solicitation", 10, r"whatsapp|telegram|join (our )?group"),
]

def run_risk_engine(text: str):
    score, flags = 0, []
    for name, points, pattern in RULES:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            score += points
            flags.append(name)
    score = min(score, 100)
    level = "LOW" if score < 30 else "VERIFY" if score < 60 else "HIGH"
    return level, score, flags

@app.get("/health")
def health():
    return {"status": "ok"}
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    level, score, flags = run_risk_engine(req.text)
    save_analysis(req.text, level, score, None, flags)
    return {
        "success": True,
        "risk": level,
        "risk_score": score,
        "confidence": None,  # filled in once Member 1's ML model is connected
        "red_flags": flags,
    }

@app.get("/history")
def history(limit: int = 20):
    return get_history(min(limit, 100))
    