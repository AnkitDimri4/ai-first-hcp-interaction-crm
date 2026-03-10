import React from "react";
import { useSelector } from "react-redux";

const InteractionForm = () => {
  const interaction = useSelector((state) => state.interactions);

  return (
    <div className="interaction-form">
      <h2 className="page-title">Log HCP Interaction</h2>

      <div className="form-section">
        {/* Existing top fields - keep as is */}
        <div className="form-row">
          <div className="form-group">
            <label>HCP Name</label>
            <input
              value={interaction.hcpName || ""}
              readOnly
              className={interaction.hcpNameUpdated ? "highlight" : ""}
            />
          </div>

          <div className="form-group">
            <label>Interaction Type</label>
            <select value={interaction.interactionType || ""} disabled>
              <option>Meeting</option>
              <option>Call</option>
              <option>Email</option>
              <option>Conference</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Date</label>
            <div className="input-with-icon">
              <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <input type="date" value={interaction.date || ""} readOnly />
            </div>
          </div>

          <div className="form-group">
            <label>Time</label>
            <div className="input-with-icon">
              <svg className="input-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12,6 12,12 16,14"></polyline>
              </svg>
              <input type="time" value={interaction.time || ""} readOnly />
            </div>
          </div>
        </div>

        <div className="form-group">
          <label>Attendees</label>
          <input value={(interaction.attendees || []).join(", ")} readOnly />
        </div>

        <div className="form-group">
          <label>Topics Discussed</label>
          <textarea rows="3" value={interaction.topicsDiscussed || ""} readOnly />
        </div>

        <div className="form-group">
          <label>Materials Shared</label>
          <input value={(interaction.materialsShared || []).join(", ")} readOnly />
        </div>

        <div className="form-group">
          <label>Sentiment</label>
          <div className="sentiment-group">
            <label>
              <input type="radio" checked={interaction.sentiment === "Positive"} readOnly />
              😊 Positive
            </label>
            <label>
              <input type="radio" checked={interaction.sentiment === "Neutral"} readOnly />
              😐 Neutral
            </label>
            <label>
              <input type="radio" checked={interaction.sentiment === "Negative"} readOnly />
              😞 Negative
            </label>
          </div>
        </div>

        {/* NEW REQUIRED SECTIONS */}
        <div className="form-group">
          <label>Key Outcomes/Agreements</label>
          <textarea 
            rows="3" 
            value={interaction.keyOutcomes || ""} 
            readOnly 
            placeholder="Key outcomes or agreements..."
          />
        </div>

        <div className="form-group">
          <label>Follow-up Actions</label>
          <textarea 
            rows="3" 
            value={interaction.followUpActions || ""} 
            readOnly 
            placeholder="Enter next steps or tasks..."
          />
        </div>

        <div className="form-group">
          <label>AI Suggested Follow-ups</label>
          <div className="ai-suggestions">
            {(interaction.aiSuggestedFollowups || []).map((suggestion, index) => (
              <div key={index} className="suggestion-item">
                <svg className="suggestion-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9 21l3-7 3 7h-6zM3 5v14h18V5H3z"/>
                </svg>
                {suggestion}
              </div>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>Follow-up Date</label>
          <input type="date" value={interaction.followUpDate || ""} readOnly />
        </div>
      </div>
    </div>
  );
};


export default InteractionForm;
