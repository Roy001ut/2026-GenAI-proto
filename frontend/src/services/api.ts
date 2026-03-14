import axios from 'axios';

const DEMO_USER = {
  id: 'demo-user-001',
  email: 'demo@medaudit.ai',
  full_name: 'Demo User',
  is_active: true,
};

const api = axios.create({ baseURL: '/api' });

// Intercept requests — mock auth & data endpoints so no backend is needed
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('[api] request:', config.method?.toUpperCase(), config.url, '| token present:', !!token);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (res) => {
    console.log('[api] response OK:', res.config.url, res.status);
    return res;
  },
  (err) => {
    const url: string = err.config?.url ?? '';
    console.error('[api] response ERROR:', url, '| status:', err.response?.status ?? 'NETWORK', '| detail:', err.response?.data ?? err.message);

    // --- AUTH stubs (login/register fail because backend is down) ---
    if (url.includes('/auth/login') || url.includes('/auth/register')) {
      console.warn('[api] stub: returning demo auth success for', url);
      return Promise.resolve({
        data: { access_token: 'demo-token', user: DEMO_USER },
      });
    }
    if (url.includes('/auth/me')) {
      console.warn('[api] stub: returning demo user for /auth/me');
      return Promise.resolve({ data: DEMO_USER });
    }

    // Suppress 401 → no reload in demo mode
    if (err.response?.status === 401) {
      console.error('[api] 401 — SUPPRESSED in demo mode (no reload)');
      return Promise.reject(err);
    }

    // --- Data stubs ---
    if (url.includes('/documents'))     { console.warn('[api] stub []', url); return Promise.resolve({ data: [] }); }
    if (url.includes('/health-wallet')) { console.warn('[api] stub []', url); return Promise.resolve({ data: [] }); }
    if (url.includes('/consultations')) { console.warn('[api] stub []', url); return Promise.resolve({ data: [] }); }
    if (url.includes('/analysis'))      { console.warn('[api] stub demo note', url); return Promise.resolve({ data: { note: 'Demo mode — no backend connected.' } }); }

    console.error('[api] unhandled error, re-throwing');
    return Promise.reject(err);
  }
);

export default api;
