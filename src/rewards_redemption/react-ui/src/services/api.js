import axios from 'axios';

const API_BASE = process.env.NODE_ENV === 'production' 
  ? 'http://localhost:8000' 
  : '';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const rewardsAPI = {
  // Categories
  getActiveCategories: () => api.get('/categories/active'),
  
  getSpendingInsights: (memberId, period = 'monthly') => 
    api.get(`/categories/${memberId}/insights?period=${period}`),
  
  getCategoryRecommendations: (memberId) => 
    api.get(`/categories/${memberId}/recommendations`),

  // Redemptions
  getRedemptionCatalog: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return api.get(`/redemptions/catalog${queryString ? '?' + queryString : ''}`);
  },
  
  processManualRedemption: (data) => 
    api.post('/redemptions/manual', data),
  
  getRedemptionHistory: (memberId, limit = 50) => 
    api.get(`/redemptions/${memberId}/history?limit=${limit}`),
  
  getValueAnalysis: (params = {}) => {
    const queryString = new URLSearchParams(params).toString();
    return api.get(`/redemptions/value-analysis${queryString ? '?' + queryString : ''}`);
  },

  // Health check
  healthCheck: () => api.get('/health'),
};

export default api;