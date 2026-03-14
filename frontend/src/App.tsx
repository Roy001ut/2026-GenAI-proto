import { useAuthStore } from './store/auth';
import Dashboard from './pages/Dashboard';

// DEMO MODE: inject user synchronously before first render — login page never shows
useAuthStore.getState().setAuth('demo-token', {
  id: 'demo-user-001',
  email: 'demo@medaudit.ai',
  full_name: 'Demo User',
  is_active: true,
});

export default function App() {
  return <Dashboard />;
}
