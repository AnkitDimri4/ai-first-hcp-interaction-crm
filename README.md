

---

# AI-First HCP Interaction CRM

An **intelligent CRM system** for Life Sciences field representatives to log and manage interactions with **Healthcare Professionals (HCPs)**. This **AI-First CRM** uses a **natural language AI assistant** to automatically extract structured information from user prompts, **eliminating manual form filling** and streamlining CRM workflows.


> #### **Live Demo:** [https://ai-first-hcp-interaction-crm.vercel.app/](https://ai-first-hcp-interaction-crm.vercel.app/)  

---

## Overview

- Users communicate with an **AI assistant** through natural language prompts.
- The **backend AI agent** (LangGraph + Groq LLM) extracts structured fields:
  - HCP Name, Date, Time, Topics, Materials Shared, Sentiment, Follow-up Actions, Key Outcomes
- Extracted data is automatically populated in the **React CRM form**.
- All interactions are saved in **PostgreSQL** via **SQLAlchemy**.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.10+, LangGraph, LangChain, Groq LLM |
| Database | PostgreSQL, SQLAlchemy |
| Frontend | React 18, Redux Toolkit, Axios, CSS |
| Hosting | Render (backend), Vercel (frontend) |

---

## Architecture

### Backend Flow

1. The **frontend** sends a `POST /agent/chat` request with the user’s message.
2. The **LangGraph AI agent** decides which tool to invoke:

   * `log_interaction` – create new interaction
   * `edit_interaction` – update specific fields
   * `get_interactions` – fetch recent interactions
   * `add_followup` – set or move follow-up dates
   * `update_materials` – update shared materials
3. Tools read/write data in the **PostgreSQL database**.
4. The backend returns **structured fields** that automatically populate the frontend form.

### Frontend Layout

* **Left Panel – AI Chat Assistant**

  * Accepts natural language prompts
  * Sends messages to the backend AI agent
  * Receives extracted structured fields

* **Right Panel – Interaction Form**

  * Auto-filled by the AI assistant
  * Displays HCP interaction details (e.g., name, date, topics, materials, sentiment, follow-ups) in real-time

---

## Project Structure & Separate READMEs

For detailed setup, architecture, and usage, see the separate README files in the repository:  

- **Backend:** [backend README](https://github.com/AnkitDimri4/ai-first-hcp-interaction-crm/blob/main/backend/README.md)  
- **Frontend:** [frontend README](https://github.com/AnkitDimri4/ai-first-hcp-interaction-crm/blob/main/frontend/README.md)  

> Each README contains installation instructions, environment variable setup, API documentation (backend), and running the development server (frontend).

---

## Key Features

- **AI-Driven Interaction Logging:** Automatically extracts HCP name, date, topics, materials shared, sentiment, follow-up actions, and outcomes from free-text input.
- **Editable Interactions:** Update only specified fields without overwriting the entire record.
- **Follow-Up Management:** Automatically suggest or adjust follow-up actions.
- **Material Updates:** Track and update materials shared during interactions.
- **Summary Retrieval:** Fetch and summarize recent interactions for quick review.

---

## Author

**Ankit Dimri**  
Full-Stack & AI Developer  
📍 Dehradun, India  

[![GitHub](https://img.shields.io/badge/GitHub-AnkitDimri4-black?logo=github)](https://github.com/AnkitDimri4)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankit%20Dimri-blue?logo=linkedin)](https://linkedin.com/in/ankit-dimri-a6ab98263)
[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-orange?logo=leetcode)](https://leetcode.com/u/user4612MW/)

### Technologies Used in This Project

### Backend
![Python](https://img.shields.io/badge/Language-Python-blue?logo=python)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue?logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)
![LangGraph](https://img.shields.io/badge/AI-LangGraph-purple)
![LangChain](https://img.shields.io/badge/AI-LangChain-black)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)
### Frontend
![React](https://img.shields.io/badge/Library-React-blue?logo=react)
![Redux](https://img.shields.io/badge/State-Redux_Toolkit-purple?logo=redux)
![React Redux](https://img.shields.io/badge/State_Management-React_Redux-purple)
![Axios](https://img.shields.io/badge/API-Axios-green)
![CSS](https://img.shields.io/badge/Style-CSS-blue?logo=css3)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

---

### Project Info

- **Project:** AI-First HCP Interaction CRM – Frontend  
- **Purpose:** Python Developer Internship Assessment  
- **Organization:** AIVOA  
- **Year:** 2026

---
---

<div align="center">
Built with ❤️ by <span>Ankit Dimri</span>
</div>

---
