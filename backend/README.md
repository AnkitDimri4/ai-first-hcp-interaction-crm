
---

> # AI-First HCP Interaction CRM – Backend

This repository contains the **FastAPI** backend for the **AI-First HCP Interaction CRM**, an intelligent Customer Relationship Management system designed for Life Sciences field representatives to log and manage interactions with Healthcare Professionals (HCPs).

The system follows an **AI-First workflow**, where the user does **not manually fill the interaction form**. Instead, the user communicates with an **AI assistant**, which extracts information from natural language and automatically populates the CRM form fields.

> This project was developed as part of the Python Developer Internship assessment at **AIVOA**.
<img width="403" height="461" alt="image" src="https://github.com/user-attachments/assets/dc1d6967-39ae-4dd2-a7a7-5dcf718f35a4" />


## Tech Stack

- FastAPI (API)
- LangGraph + LangChain (AI agent + tools)
- Groq LLM – `llama-3.3-70b-versatile`
- PostgreSQL + SQLAlchemy
- Python 3.10+

> Note: `gemma2-9b-it` from the assignment was decommissioned by Groq, so `llama-3.3-70b-versatile` is used for reliable structured extraction of outcomes, follow-ups, and suggested actions.

> Additionally, during testing the smaller models did not reliably extract the required structured CRM fields such as: Key Outcomes / Agreements, Follow-up Actions, AI Suggested Follow-ups

## Architecture

High-level flow:

1. Frontend sends user message to `POST /agent/chat`.
2. LangGraph agent (Groq LLM + tools) decides which tool to call:
   - `log_interaction`
   - `edit_interaction`
   - `get_interactions`
   - `add_followup`
   - `update_materials`
3. Tools read/write the `hcp_interactions` table in PostgreSQL.
4. Backend returns structured `fields` so the React form auto-fills and updates.

Main backend layout:

```bash
backend/
├── app/
│   ├── agent/        # LangGraph agent (graph.py)
│   ├── db/           # DB engine/session (database.py)
│   ├── models/       # SQLAlchemy models (interaction.py)
│   ├── routes/       # Tool helpers (tools.py)
│   └── main.py       # FastAPI app + /agent/chat
├── requirements.txt
└── README.md
```

## Key Features (Tools)

- **log_interaction** – Create a new interaction from a free-text prompt (extracts HCP, date, time, topics, materials, sentiment, follow-up).
- **edit_interaction** – Update only the fields mentioned (e.g. “Change HCP name to Dr John and sentiment to negative”).
- **get_interactions** – Fetch recent interactions and return a text summary for the assistant response.
- **add_followup** – Set or move follow-up dates (supports “latest” interaction).
- **update_materials** – Replace `materials_shared` for a given interaction.

Example prompt:

> I met Dr Smith today at 3 PM to discuss Product X efficiency. John from marketing also attended, I shared brochures, the response was positive, and we will follow up on 25 March.

The backend + agent extract all fields and store a complete `hcp_interactions` row; the form is filled automatically.

## Setup

### 1. Virtualenv & Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

`requirements.txt` (minimal):

```txt
fastapi
uvicorn
sqlalchemy
psycopg2-binary
pydantic
python-dotenv
requests
langgraph
langchain
langchain-core
langchain-groq
```

Do **not** commit `venv/`; only commit `requirements.txt`.

### 2. Environment Variables

Create `backend/.env` (not committed):

```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=postgresql://user:password@localhost:5432/hcp_crm
```

You can add a safe `backend/.env.example` with placeholder values.

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

Main endpoints:

- `POST /agent/chat` – AI assistant entrypoint (used by frontend)
- Tool routes (internal use by agent, optional to call directly):
  - `POST /tools/log-interaction`
  - `PUT  /tools/edit-interaction`
  - `GET  /tools/interactions`
  - `PUT  /tools/add-followup`
  - `PUT  /tools/update-materials`


---


---

## Author

**Ankit Dimri**  
Full-Stack & AI Developer 
📍 Dehradun, India  

[![GitHub](https://img.shields.io/badge/GitHub-AnkitDimri4-black?logo=github)](https://github.com/AnkitDimri4)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankit%20Dimri-blue?logo=linkedin)](https://linkedin.com/in/ankit-dimri-a6ab98263)
[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-orange?logo=leetcode)](https://leetcode.com/u/user4612MW/)

### Technologies Used in This Project

![Python](https://img.shields.io/badge/Language-Python-blue?logo=python)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-purple)
![LangChain](https://img.shields.io/badge/AI-LangChain-black)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

---

### Project Info

- **Project:** AI-First HCP Interaction CRM – Backend  
- **Purpose:** Python Developer Internship Assessment  
- **Organization:** AIVOA  
- **Year:** 2026

---

<div align="center">
Built with ❤️ by <b>Ankit Dimri</b>
</div>

---
