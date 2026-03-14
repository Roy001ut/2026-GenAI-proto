import { useEffect } from 'react';
import { useAuthStore } from './store/auth';
import Dashboard from './pages/Dashboard';

// DEMO MODE: bypass login and env config — show the feature directly
const DEMO_USER = {
  id: 'demo-user-001',
  email: 'demo@medaudit.ai',
  full_name: 'Demo User',
  is_active: true,
};

export default function App() {
  const { user, setAuth } = useAuthStore();

  useEffect(() => {
    if (!user) {
      setAuth('demo-token', DEMO_USER);
    }
  }, []);

  if (!user) return null;

  return <Dashboard />;
}
