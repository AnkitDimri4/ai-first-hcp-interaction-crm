from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.interaction import Interaction
import requests
import os
import json
import re
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter()

# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Request Models
# -------------------------
class Prompt(BaseModel):
    prompt: str


class InteractionUpdate(BaseModel):
    id: int
    hcp_name: str | None = None
    interaction_type: str | None = None
    date: str | None = None
    time: str | None = None
    attendees: list[str] | None = None
    topics_discussed: str | None = None
    materials_shared: list[str] | None = None
    sentiment: str | None = None
    follow_up_date: str | None = None
    key_outcomes: str | None = None
    follow_up_actions: str | None = None
    ai_suggested_followups: list[str] | None = None


# -------------------------
# Groq Config
# -------------------------
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("GROQ_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


# -------------------------
# Helper: Extract JSON
# -------------------------
def extract_fields_from_prompt(prompt: str):
    today = datetime.now().strftime("%Y-%m-%d")

    system_prompt = f"""
Today is {today}.
Extract CRM interaction information and return ONLY valid JSON.

Fields:
{{
  "hcp_name": "",
  "interaction_type": "",
  "date": "",
  "time": "",
  "attendees": [],
  "topics_discussed": "",
  "materials_shared": [],
  "sentiment": "",
  "follow_up_date": "",
  "key_outcomes": "",
  "follow_up_actions": "",
  "ai_suggested_followups": []
}}

Rules:
- interaction_type must be: Meeting, Call, Email, Conference
- sentiment must be: Positive, Neutral, Negative
- Convert natural language dates:
  - "today" -> today's date in YYYY-MM-DD
  - "tomorrow" -> tomorrow's date
  - "25 March" -> YYYY-MM-DD in the correct year
- Convert time like:
  - "3 PM" -> 15:00
- attendees should be a list of names
- materials_shared should be a list
- key_outcomes: brief summary of key outcomes or agreements
- follow_up_actions: concrete next steps as one string
- ai_suggested_followups: array of 2–5 follow-up suggestions
- Return ONLY JSON with no extra text
"""

    payload = {
        "model": "llama-3.3-70b-versatile",
        # "model": "llama-3.1-8b-instant",
        # "model": "gemma2-9b-it",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
    data = response.json()

    if "choices" not in data:
        raise Exception(f"Groq API Error: {data}")

    content = data["choices"][0]["message"]["content"]

    try:
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        parsed = json.loads(json_match.group()) if json_match else {}
    except Exception:
        parsed = {}

    parsed.setdefault("hcp_name", "")
    parsed.setdefault("interaction_type", "")
    parsed.setdefault("date", None)
    parsed.setdefault("time", None)
    parsed.setdefault("topics_discussed", "")
    parsed.setdefault("sentiment", "")
    parsed.setdefault("follow_up_date", None)
    parsed.setdefault("key_outcomes", "")
    parsed.setdefault("follow_up_actions", "")
    parsed.setdefault("ai_suggested_followups", [])

    parsed["attendees"] = parsed.get("attendees") or []
    parsed["materials_shared"] = parsed.get("materials_shared") or []
    parsed["ai_suggested_followups"] = parsed.get("ai_suggested_followups") or []

    return parsed


# -------------------------
# Tool 1: Log Interaction
# -------------------------
@router.post("/log-interaction")
def log_interaction(prompt: Prompt, db: Session = Depends(get_db)):
    extracted = extract_fields_from_prompt(prompt.prompt)

    interaction = Interaction(
        hcp_name=extracted["hcp_name"],
        interaction_type=extracted["interaction_type"],
        date=extracted["date"],
        time=extracted["time"],
        attendees=extracted["attendees"],
        topics_discussed=extracted["topics_discussed"],
        materials_shared=extracted["materials_shared"],
        sentiment=extracted["sentiment"],
        follow_up_date=extracted["follow_up_date"],
        key_outcomes=extracted["key_outcomes"],
        follow_up_actions=extracted["follow_up_actions"],
        ai_suggested_followups=extracted["ai_suggested_followups"],
    )

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


# -------------------------
# Tool 2: Get Interactions
# -------------------------
@router.get("/interactions")
def get_interactions(db: Session = Depends(get_db)):
    return db.query(Interaction).all()


# -------------------------
# Tool 3: Edit Interaction
# -------------------------
@router.put("/edit-interaction")
def edit_interaction(update: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(
        Interaction.id == update.id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    for field, value in update.dict(exclude_unset=True).items():
        setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)

    return interaction


# -------------------------
# Tool 4: Add Followup
# -------------------------
@router.put("/add-followup")
def add_followup(update: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(
        Interaction.id == update.id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    interaction.follow_up_date = update.follow_up_date

    db.commit()
    db.refresh(interaction)

    return {"follow_up_date": interaction.follow_up_date}


# -------------------------
# Tool 5: Update Materials
# -------------------------
@router.put("/update-materials")
def update_materials(update: InteractionUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(
        Interaction.id == update.id
    ).first()

    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    interaction.materials_shared = update.materials_shared or []

    db.commit()
    db.refresh(interaction)

    return {"materials_shared": interaction.materials_shared}
