import axios from "axios";

const ML_BASE = import.meta.env.VITE_ML_SERVICE_URL || "http://localhost:8000";

export const predictDeliveryDelay = (history, sample) =>
  axios.post(`${ML_BASE}/api/predict-delay`, { history, sample });

export const predictDemand = (history, horizonDays = 7) =>
  axios.post(`${ML_BASE}/api/predict-demand`, { history, horizonDays });

export const optimizeRoutes = (payload) =>
  axios.post(`${ML_BASE}/api/optimize-route`, payload);
