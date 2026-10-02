
from fastapi import FastAPI
from pydantic import BaseModel, Field

from analyzer import analyze_message

app = FastAPI(
    title="Investment Scam Detection API",
    description="AI-assisted investment risk analysis",
    version="1.0"
)


class MessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000
    )


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Investment Scam Detection API is ready"
    }


@app.post("/analyze")
def analyze(request: MessageRequest):
    if not request.message.strip():
        return {
            "risk": "UNKNOWN",
            "confidence": None,
            "reasons": ["Empty message"],
            "recommendation": "Enter an investment-related message."
        }

    result = analyze_message(request.message)
    return result