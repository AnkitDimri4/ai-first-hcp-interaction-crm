
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_groq import ChatGroq

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.interaction import Interaction

import os
from typing import TypedDict, List, Optional


# ---------------- LLM ----------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.2,
)


# ---------------- SYSTEM PROMPT ----------------

system_instructions = """
You are an AI CRM assistant for HCP interactions.

You have these tools:
- log_interaction: when the user describes a new meeting/call/email, extract fields and log a new interaction.
- edit_interaction: when the user corrects or changes details of an existing interaction.
- get_interactions: when the user asks to see or summarize past interactions.
- add_followup: when the user changes or adds a follow-up date.
- update_materials: when the user says they shared additional materials.

When you call get_interactions, read the `summary` returned by the tool
and include that summary in your answer to the user.

When you edit the most recent interaction, call edit_interaction with interaction_id="latest".

Always choose the most appropriate tool based on the user's message.
"""


# ---------------- DB HELPERS ----------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_last_interaction_id() -> Optional[int]:
    db = next(get_db())
    last = db.query(Interaction).order_by(Interaction.id.desc()).first()
    return last.id if last else None


# ---------------- TOOLS ----------------

@tool("log_interaction")
def log_interaction_tool(user_text: str) -> dict:
    """Extract interaction details and create a new interaction."""

    from app.routes.tools import extract_fields_from_prompt

    db = next(get_db())

    extracted = extract_fields_from_prompt(user_text)

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

    return {
        "message": "Interaction logged",
        "interaction_id": interaction.id,
        "data": extracted,
    }


@tool("edit_interaction")
def edit_interaction_tool(instruction: str, interaction_id: int | str) -> dict:
    """Edit an existing interaction."""

    if isinstance(interaction_id, str):

        if interaction_id.lower() == "latest":
            interaction_id = get_last_interaction_id()

            if interaction_id is None:
                return {"error": "No interactions found"}

        else:
            try:
                interaction_id = int(interaction_id)
            except ValueError:
                return {"error": "Invalid interaction_id"}

    db = next(get_db())

    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    from app.routes.tools import extract_fields_from_prompt

    extracted = extract_fields_from_prompt(instruction)

    updatable_fields = [
        "hcp_name",
        "interaction_type",
        "date",
        "time",
        "attendees",
        "topics_discussed",
        "materials_shared",
        "sentiment",
        "follow_up_date",
        "key_outcomes",
        "follow_up_actions",
        "ai_suggested_followups",
    ]

    for field in updatable_fields:
        value = extracted.get(field)

        if value not in (None, "", []):
            setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)

    return {
        "message": "Interaction updated",
        "interaction_id": interaction.id,
    }


@tool("get_interactions")
def get_interactions_tool(limit: int | str = 5) -> dict:
    """Return recent interactions."""

    try:
        if isinstance(limit, str):
            limit = int(limit)
    except ValueError:
        limit = 5

    db = next(get_db())

    rows = (
        db.query(Interaction)
        .order_by(Interaction.id.desc())
        .limit(limit)
        .all()
    )

    interactions = []

    for r in rows:
        interactions.append(
            {
                "id": r.id,
                "hcp_name": r.hcp_name,
                "date": r.date,
                "topics_discussed": r.topics_discussed,
                "sentiment": r.sentiment,
            }
        )

    if not interactions:
        summary = "No recent interactions found."

    else:
        lines = []

        for r in interactions:
            lines.append(
                f"- {r['date']}: {r['hcp_name']} ({r['sentiment']}) – {r['topics_discussed']}"
            )

        summary = "Here are your recent interactions:\n" + "\n".join(lines)

    return {
        "interactions": interactions,
        "summary": summary,
    }


@tool("add_followup")
def add_followup_tool(interaction_id: int | str, follow_up_date: str) -> dict:
    """Update follow-up date."""

    if isinstance(interaction_id, str):

        if interaction_id.lower() == "latest":
            interaction_id = get_last_interaction_id()

            if interaction_id is None:
                return {"error": "No interactions found"}

        else:
            interaction_id = int(interaction_id)

    db = next(get_db())

    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    interaction.follow_up_date = follow_up_date

    db.commit()
    db.refresh(interaction)

    return {
        "message": "Follow-up updated",
        "follow_up_date": interaction.follow_up_date,
    }


@tool("update_materials")
def update_materials_tool(interaction_id: int | str, materials: list[str]) -> dict:
    """Update materials shared."""

    if isinstance(interaction_id, str):

        if interaction_id.lower() == "latest":
            interaction_id = get_last_interaction_id()

            if interaction_id is None:
                return {"error": "No interactions found"}

        else:
            interaction_id = int(interaction_id)

    db = next(get_db())

    interaction = db.query(Interaction).filter(
        Interaction.id == interaction_id
    ).first()

    if not interaction:
        return {"error": "Interaction not found"}

    interaction.materials_shared = materials

    db.commit()
    db.refresh(interaction)

    return {
        "message": "Materials updated",
        "materials_shared": interaction.materials_shared,
    }


# ---------------- TOOL LIST ----------------

tools = [
    log_interaction_tool,
    edit_interaction_tool,
    get_interactions_tool,
    add_followup_tool,
    update_materials_tool,
]

tool_node = ToolNode(tools)

llm_with_tools = llm.bind_tools(tools)


# ---------------- AGENT STATE ----------------

class AgentState(TypedDict):
    messages: List[dict]


# ---------------- AGENT NODE ----------------

def agent_node(state: AgentState, config: RunnableConfig):

    messages = [
        {"role": "system", "content": system_instructions},
        *state["messages"],
    ]

    response = llm_with_tools.invoke(messages, config=config)

    # Convert AIMessage → dict
    message = {
        "role": "assistant",
        "content": response.content
    }

    # If the LLM requested a tool
    if response.tool_calls:
        message["tool_calls"] = response.tool_calls

    state["messages"].append(message)

    return state


# ---------------- GRAPH ----------------

graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent")


def route_tools(state: AgentState):

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


graph.add_conditional_edges(
    "agent",
    route_tools,
)

graph.add_edge("tools", "agent")

compiled_graph = graph.compile()