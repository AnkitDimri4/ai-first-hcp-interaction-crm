import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcpName: "",
  interactionType: "Meeting",
  date: "",
  time: "",
  attendees: [],
  topicsDiscussed: "",
  materialsShared: [],
  sentiment: "",
  followUpDate: "",
  keyOutcomes: "",
  followUpActions: "",
  aiSuggestedFollowups: [],
};

const interactionsSlice = createSlice({
  name: "interactions",
  initialState,
  reducers: {
    setInteraction: (state, action) => ({ ...state, ...action.payload }),
    updateField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
      state[field + "Updated"] = true; // for UI highlight
    },
  },
});

export const { setInteraction, updateField } = interactionsSlice.actions;
export default interactionsSlice.reducer;
