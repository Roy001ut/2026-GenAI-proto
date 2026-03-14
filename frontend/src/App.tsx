import { useAuthStore } from './store/auth';
import Dashboard from './pages/Dashboard';

// DEMO MODE — runs once at module load, before any React render
console.log('[App] module loading — calling setAuth with demo user');
useAuthStore.getState().setAuth('demo-token', {
  id: 'demo-user-001',
  email: 'demo@medaudit.ai',
  full_name: 'Demo User',
  is_active: true,
});
console.log('[App] setAuth done — store state:', useAuthStore.getState());

export default function App() {
  const { user, token } = useAuthStore();
  console.log('[App] render — token:', token, '| user:', user);
  return <Dashboard />;
}
