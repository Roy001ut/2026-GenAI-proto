import { useState, useEffect } from 'react';
import { useAuthStore } from './store/auth.store';
import api from './services/api';
import Login from './pages/Login';
import Dashboard from './components/Dashboard/Dashboard';

function App() {
  const { token, setUser, logout } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      fetchCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const fetchCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me');
      setUser(response.data);
    } catch (error) {
      logout();
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  return token ? <Dashboard /> : <Login />;
}

export default App;
