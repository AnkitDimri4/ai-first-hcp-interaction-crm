import { configureStore } from "@reduxjs/toolkit";
import interactionsReducer from "./interactionsSlice";

export default configureStore({
  reducer: { interactions: interactionsReducer }
});