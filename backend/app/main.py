import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.db.database import Base, engine
from app.routes import tools as legacy_tools
from app.agent.graph import compiled_graph
from app.routes.tools import extract_fields_from_prompt


app = FastAPI()

# Environment detection
ENV = os.getenv("ENV", "dev")

# CORS configuration
if ENV == "prod":
    origins = ["*"]
else:
    origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include existing tools routes
app.include_router(legacy_tools.router, prefix="/tools")


@app.get("/")
def health_check():
    return {"status": "AI CRM backend running"}


# Request schema
class ChatRequest(BaseModel):
    message: str


@app.post("/agent/chat")
async def agent_chat(body: ChatRequest):

    # Send message to LangGraph agent
    state = {
        "messages": [
            {"role": "user", "content": body.message}
        ]
    }

    result = compiled_graph.invoke(state)

    # Get assistant response
    assistant_msg = next(
        (m for m in reversed(result["messages"]) if m["role"] == "assistant"),
        None,
    )

    reply_text = assistant_msg["content"] if assistant_msg else "Interaction processed."

    # Extract structured form fields
    fields = extract_fields_from_prompt(body.message)

    return {
        "reply": reply_text,
        "fields": fields,
    }
