import re
import sqlite3
import json
from datetime import datetime, timezone

DB_PATH = "raksha.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                risk TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                confidence REAL,
                red_flags TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

def redact(text: str) -> str:
    # Mask values that follow words like otp / pin / password / cvv
    text = re.sub(
        r"(?i)\b(otp|pin|password|passcode|cvv)\b(\s*(?:is|:|=|-)?\s*)\S+",
        r"\1\2[REDACTED]",
        text,
    )
    # Mask long digit runs (card numbers, account numbers)
    text = re.sub(r"\b\d{9,}\b", "[REDACTED]", text)
    return text

def save_analysis(text, risk, score, confidence, flags):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO analysis_history "
            "(input_text, risk, risk_score, confidence, red_flags, timestamp) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                redact(text),
                risk,
                score,
                confidence,
                json.dumps(flags),
                datetime.now(timezone.utc).isoformat(),
            ),
        )

def get_history(limit: int = 20):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM analysis_history ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [
        {**dict(r), "red_flags": json.loads(r["red_flags"])} for r in rows
    ]