import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Configuration axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour gérer les erreurs globalement
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erreur API:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// === DUERP ===
export const getDUERPs = () => api.get('/duerp/');
export const getDUERP = (id) => api.get(`/duerp/${id}`);
export const createDUERP = (data) => api.post('/duerp/', data);
export const updateDUERP = (id, data) => api.put(`/duerp/${id}`, data);
export const deleteDUERP = (id) => api.delete(`/duerp/${id}`);
export const validateDUERP = (id, data) => api.post(`/duerp/${id}/validate`, data);
export const getDUERPStats = (id) => api.get(`/duerp/${id}/stats`);
export const getDUERPHistory = (id) => api.get(`/duerp/${id}/history`);
export const generateDUERPDocument = (id, format = 'pdf') =>
  api.post(`/duerp/${id}/generate`, { format }, { responseType: 'blob' });

// === Unités de travail ===
export const createUnite = (data) => api.post('/unite/', data);
export const getUnite = (id) => api.get(`/unite/${id}`);
export const updateUnite = (id, data) => api.put(`/unite/${id}`, data);
export const deleteUnite = (id) => api.delete(`/unite/${id}`);

// === Risques ===
export const createRisque = (data) => api.post('/risque/', data);
export const getRisque = (id) => api.get(`/risque/${id}`);
export const updateRisque = (id, data) => api.put(`/risque/${id}`, data);
export const deleteRisque = (id) => api.delete(`/risque/${id}`);
export const getRisqueCategories = () => api.get('/risque/categories');

// === Mesures de prévention ===
export const createMesure = (data) => api.post('/mesure/', data);
export const getMesure = (id) => api.get(`/mesure/${id}`);
export const updateMesure = (id, data) => api.put(`/mesure/${id}`, data);
export const deleteMesure = (id) => api.delete(`/mesure/${id}`);
export const getMesureTypes = () => api.get('/mesure/types');

export default api;
