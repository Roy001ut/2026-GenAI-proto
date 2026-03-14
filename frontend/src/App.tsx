import { useEffect, useState } from 'react';
import { useAuthStore } from './store/auth';
import api from './services/api';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

export default function App() {
  const { token, user, setUser, logout } = useAuthStore();
  const [loading, setLoading] = useState(!!token && !user);

  useEffect(() => {
    if (!token || user) {
      setLoading(false);
      return;
    }
    api.get('/auth/me')
      .then((r) => setUser(r.data))
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, []); // run once on mount

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-gray-500 text-lg">Loading…</div>
      </div>
    );
  }

  return token && user ? <Dashboard /> : <Login />;
}
