import { useEffect, useState } from 'react';

import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './components/Dashboard';

import { apiRequest } from './api/client';

import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState('login');

  async function loadUser() {
    const token = sessionStorage.getItem('access_token');

    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }

    try {
      const data = await apiRequest('/user/me', {}, token);
      setUser(data);
    } catch (error) {
      if (error.status === 401) {
        sessionStorage.removeItem('access_token');
        setUser(null);
      } else {
        console.error('Erro ao verificar sessão:', error);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadUser();
  }, []);

  function handleLogin() {
    setLoading(true);
    loadUser();
  }

  function handleLogout() {
    sessionStorage.removeItem('access_token');
    setUser(null);
    setPage('login');
  }

  if (loading) {
    return (
      <div className="app-loading">
        <div className="app-loading__card" role="status">
          <span className="app-loading__spinner" aria-hidden="true" />
          Verificando sessão...
        </div>
      </div>
    );
  }

  if (user) {
    return (
      <Dashboard
        user={user}
        onLogout={handleLogout}
      />
    );
  }

  if (page === 'register') {
    return (
      <Register
        onBackToLogin={() => setPage('login')}
      />
    );
  }

  return (
    <Login
      onLogin={handleLogin}
      onRegister={() => setPage('register')}
    />
  );
}

export default App;
