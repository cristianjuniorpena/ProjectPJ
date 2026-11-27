import { useState } from 'react';
import { apiRequest } from '../api/client';

function Login({ onLogin, onRegister }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function handleLogin(event) {
    event.preventDefault();
    setMessage('Autenticando...');

    try {
      const formData = new URLSearchParams();

      formData.append('username', email);
      formData.append('password', password);

      const data = await apiRequest('/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      sessionStorage.setItem('access_token', data.access_token);

      onLogin();

      setMessage('Login realizado com sucesso!');
    } catch (error) {
      setMessage(error.message);
    }
  }

  return (
    <main>
      <h1>Login - Project PJ</h1>

      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Senha"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          required
        />

        <button type="submit">Entrar</button>
      </form>

      <button type="button" onClick={onRegister}>
        Criar uma conta
      </button>

      <p>{message}</p>
    </main>
  );
}

export default Login;