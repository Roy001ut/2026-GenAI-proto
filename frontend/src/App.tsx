import { useEffect, useState } from 'react';
import { useAuthStore } from './store/auth.store';
import api from './services/api';
import Login from './pages/Login';
import Dashboard from './components/Dashboard/Dashboard';

export default function App() {
  const { token, user, setUser, logout } = useAuthStore();
  const [loading, setLoading] = useState(!!token && !user);

  // On hard refresh: token is in localStorage but user state is empty — re-fetch
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
      <div className="flex items-center justify-center min-h-screen text-gray-500">
        Loading…
      </div>
    );
  }

  return token && user ? <Dashboard /> : <Login />;
}
