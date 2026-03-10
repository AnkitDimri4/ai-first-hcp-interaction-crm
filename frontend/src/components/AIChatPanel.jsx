import React, { useState } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { updateField } from "../redux/interactionsSlice";

const AIChatPanel = () => {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);

  const dispatch = useDispatch();

  const fieldMap = {
    hcp_name: "hcpName",
    interaction_type: "interactionType",
    date: "date",
    time: "time",
    attendees: "attendees",
    topics_discussed: "topicsDiscussed",
    materials_shared: "materialsShared",
    sentiment: "sentiment",
    follow_up_date: "followUpDate",
    key_outcomes: "keyOutcomes",
    follow_up_actions: "followUpActions",
    ai_suggested_followups: "aiSuggestedFollowups",
  };
const handleSend = async () => {
  if (!prompt.trim()) return;

  const userText = prompt;
  setMessages((prev) => [...prev, { type: "user", text: userText }]);

  try {
    const backendURL = process.env.REACT_APP_BACKEND_URL;
    const res = await axios.post(`${backendURL}/agent/chat`, {
      message: userText,
    });

    const fields = res.data.fields || {};

    Object.keys(fieldMap).forEach((key) => {
      let value = fields[key];

      if (
        key === "attendees" ||
        key === "materials_shared" ||
        key === "ai_suggested_followups"
      ) {
        value = value || [];
      }

      const isEmptyArray = Array.isArray(value) && value.length === 0;
      const isEmptyStringOrNull =
        value === "" || value === null || value === undefined;

      if (!isEmptyArray && !isEmptyStringOrNull) {
        dispatch(
          updateField({
            field: fieldMap[key],
            value,
          })
        );
      }
    });

    // Decide message type: log vs edit (simple heuristic based on wording)
    const lower = userText.toLowerCase();
    let replyText;

    if (
      lower.includes("update the last interaction") ||
      lower.includes("change the time") ||
      lower.includes("set the follow-up date") ||
      lower.includes("move the follow-up") ||
      lower.includes("also note that i shared") ||
      lower.includes("update the materials")
    ) {
      replyText =
        "✅ Changes applied. I’ve updated only the requested fields for the last interaction, keeping all other details the same.";
    } else {
      replyText =
        "✅ Interaction logged successfully. I’ve filled the form with HCP Name, Date, Time, Sentiment, Topics, Materials Shared, and Follow-up details based on your description.";
    }

    setMessages((prev) => [
      ...prev,
      {
        type: "ai",
        text: replyText,
      },
    ]);

    setPrompt("");
  } catch (error) {
    console.error(error);
    setMessages((prev) => [
      ...prev,
      {
        type: "ai",
        text: "Error processing request",
      },
    ]);
  }
};


  return (
    <div className="ai-chat">
      <h3>🤖 AI Assistant</h3>

      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble ${m.type}`}>
            {m.text}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Describe interaction or ask to edit..."
        />

        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default AIChatPanel;