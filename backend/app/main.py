from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.db.database import Base, engine
from app.routes import tools as legacy_tools
from app.agent.graph import compiled_graph
from app.routes.tools import extract_fields_from_prompt  # IMPORTANT

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(legacy_tools.router, prefix="/tools")


class ChatRequest(BaseModel):
    message: str


@app.post("/agent/chat")
async def agent_chat(body: ChatRequest):

    state = {"messages": [{"role": "user", "content": body.message}]}
    result = compiled_graph.invoke(state)
    assistant_msg = next(
        (m for m in reversed(result["messages"]) if m["role"] == "assistant"),
        None,
    )
    reply_text = assistant_msg["content"] if assistant_msg else "Interaction processed."

    fields = extract_fields_from_prompt(body.message)

    return {
        "reply": reply_text,
        "fields": fields,
    }
