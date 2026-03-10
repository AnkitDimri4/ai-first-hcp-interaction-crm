
---

> # AI-First HCP Interaction CRM – Frontend

This repository contains the **React frontend** for the **AI-First HCP Interaction CRM**, an intelligent Customer Relationship Management system designed for **Life Sciences field representatives** to log and manage interactions with **Healthcare Professionals (HCPs)**.

> - ### The frontend provides a **split-screen interface** where:
>   * #### The **left panel** contains an **AI chat assistant**.
>   * #### The **right panel** displays the **interaction form**.

Instead of manually filling the CRM form, users interact with the **AI assistant using natural language**, and the system automatically extracts and fills structured fields in the form.

This frontend communicates with the **FastAPI backend**, which runs the **LangGraph AI agent** responsible for extracting structured CRM data.

> This project was developed as part of the **Python Developer Internship assessment at AIVOA**.

<img width="450" height="500" alt="image" src="https://github.com/user-attachments/assets/73aec764-dd83-4069-8c5a-97d778c86ac7" />
<img width="450" height="500" alt="image" src="https://github.com/user-attachments/assets/b44b259c-7a2d-4683-8bd3-12a77f658ecb" />


---

## UI Layout

The interface follows a **split-screen CRM design**:

* **AI Chat Panel**

  * User enters natural language prompts.
  * Messages are sent to the backend AI agent.
  * AI processes the request and extracts structured fields.

* **Interaction Form**

  * Automatically populated by the AI response.
  * Displays extracted interaction data such as:

    * HCP Name
    * Interaction Date
    * Interaction Time
    * Discussion Topics
    * Materials Shared
    * Sentiment
    * Follow-up Actions
    * Key Outcomes

---

## Tech Stack

Frontend technologies used:

* **React 18**
* **Redux Toolkit** (state management)
* **React Redux**
* **Axios** (API communication)
* **CSS** for styling

Testing utilities included:

* React Testing Library
* Jest DOM

---

## Frontend Architecture

Main project structure:

```
frontend/
├── package.json
├── src/
│ ├── App.jsx
│ ├── index.js
│ ├── redux/
│ │ ├── store.js
│ │ └── interactionsSlice.js
│ ├── components/
│ │ ├── InteractionForm.jsx
│ │ └── AIChatPanel.jsx
│ └── App.css
```

### Core Components

**AIChatPanel.jsx**

* Chat interface for communicating with the AI assistant
* Sends prompts to:

```
POST /agent/chat
```

* Receives structured data from backend and updates Redux state

---

**InteractionForm.jsx**

Displays the **CRM interaction form**.

Fields are automatically populated from AI extracted data including:

* HCP Name
* Date
* Time
* Topics Discussed
* Materials Shared
* Sentiment
* Follow-up Actions

The form reflects the **latest AI-generated interaction state** stored in Redux.

---

**Redux Store**

Redux manages global state for the interaction form.

```
redux/
 ├── store.js
 └── interactionsSlice.js
```

Responsibilities:

* Store extracted interaction fields
* Update form fields when AI response arrives
* Maintain consistent application state

---

## Backend Communication

The frontend communicates with the backend AI agent using **Axios**.

Example request flow:

1. User enters message in **AIChatPanel**.

Example prompt:

> I met Dr Smith today at 3 PM to discuss Product X efficiency. I shared brochures and the response was positive. We will follow up on 25 March.

2. Frontend sends request to backend:

```
POST http://localhost:8000/agent/chat
```

3. Backend AI agent:

* Extracts structured fields
* Saves interaction to database
* Returns extracted data

4. Redux updates form fields automatically.

---

## Setup

### 1 Install Dependencies

Navigate to the frontend folder:

```
cd frontend
```

Install packages:

```
npm install
```

---

### 2 Run the Development Server

```
npm start
```

Application runs at:

```
http://localhost:3000
```

---

### 3 Backend Requirement

The frontend requires the backend API to be running.

Start backend:

```
uvicorn app.main:app --reload
```

Backend URL:

```
http://localhost:8000
```

---

## Author

**Ankit Dimri**  
Full-Stack & AI Developer  
📍 Dehradun, India  

[![GitHub](https://img.shields.io/badge/GitHub-AnkitDimri4-black?logo=github)](https://github.com/AnkitDimri4)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ankit%20Dimri-blue?logo=linkedin)](https://linkedin.com/in/ankit-dimri-a6ab98263)
[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-orange?logo=leetcode)](https://leetcode.com/u/user4612MW/)

### Technologies Used in This Project

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

<div align="center">
Built with ❤️ by <b>Ankit Dimri</b>
</div>

---
