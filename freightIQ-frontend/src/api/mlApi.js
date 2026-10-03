import axios from "axios";

const ML_BASE = import.meta.env.VITE_ML_SERVICE_URL || "http://localhost:8000";

export const getMLRecommendations = (shipmentId) =>
  axios.post(`${ML_BASE}/api/recommend`, { shipmentId });
