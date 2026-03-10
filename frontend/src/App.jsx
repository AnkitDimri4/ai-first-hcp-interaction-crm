import React from "react";
import InteractionForm from "./components/InteractionForm";
import AIChatPanel from "./components/AIChatPanel";
import "./App.css";

function App() {
  return (
    <div className="crm-container">
      <div className="left-panel">
        <InteractionForm />
      </div>
      <div className="right-panel">
        <AIChatPanel />
      </div>
    </div>
  );
}

export default App;