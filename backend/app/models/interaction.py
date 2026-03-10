from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from app.db.database import Base

class Interaction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)

    hcp_name = Column(String)
    interaction_type = Column(String)
    date = Column(String)
    time = Column(String)
    attendees = Column(ARRAY(String))
    topics_discussed = Column(String)
    materials_shared = Column(ARRAY(String))
    sentiment = Column(String)
    follow_up_date = Column(String)

    # NEW
    key_outcomes = Column(String)
    follow_up_actions = Column(String)
    ai_suggested_followups = Column(ARRAY(String))
