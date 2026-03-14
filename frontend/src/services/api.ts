import axios from 'axios';

const api = axios.create({ baseURL: '/api' });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('[api] request:', config.method?.toUpperCase(), config.url, '| token present:', !!token);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => {
    console.log('[api] response OK:', res.config.url, res.status, res.data);
    return res;
  },
  (err) => {
    console.error('[api] response ERROR:', err.config?.url, '| status:', err.response?.status, '| detail:', err.response?.data);

    if (err.response?.status === 401) {
      // In demo mode this should never fire — log loudly if it does
      console.error('[api] 401 received — would normally trigger logout+reload. SUPPRESSED in demo mode.');
      return Promise.reject(err);
    }

    // Return stubs so pages don't crash without a backend
    const url: string = err.config?.url ?? '';
    if (url.includes('/documents'))    { console.warn('[api] stub: returning [] for', url); return Promise.resolve({ data: [] }); }
    if (url.includes('/health-wallet')){ console.warn('[api] stub: returning [] for', url); return Promise.resolve({ data: [] }); }
    if (url.includes('/consultations') ){ console.warn('[api] stub: returning [] for', url); return Promise.resolve({ data: [] }); }
    if (url.includes('/analysis'))     { console.warn('[api] stub: returning demo note for', url); return Promise.resolve({ data: { note: 'Demo mode — no backend connected.' } }); }

    console.error('[api] unhandled error, re-throwing');
    return Promise.reject(err);
  }
);

export default api;
