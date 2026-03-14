import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// DEMO MODE: intercept responses so the UI works without a backend
api.interceptors.response.use(
  (res) => res,
  (err) => {
    // Suppress 401 redirects in demo mode (no real auth)
    if (err.response?.status === 401) return Promise.reject(err);

    // Return sensible empty stubs so pages don't hard-crash
    const url: string = err.config?.url ?? '';
    if (url.includes('/documents')) return Promise.resolve({ data: [] });
    if (url.includes('/health-wallet')) return Promise.resolve({ data: [] });
    if (url.includes('/consultations')) return Promise.resolve({ data: [] });
    if (url.includes('/analysis')) return Promise.resolve({ data: { note: 'Demo mode — no backend connected.' } });

    return Promise.reject(err);
  }
);

export default api;
