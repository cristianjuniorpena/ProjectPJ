
import { useState } from 'react';
import { apiRequest } from '../api/client';

function Register({ onBackToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('contractor');

  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  async function handleRegister(event) {
    event.preventDefault();

    setLoading(true);
    setMessage('');

    try {
      const data = await apiRequest('/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          password,
          role,
        }),
      });

      setMessage(`Usuário ${data.name} cadastrado com sucesso!`);
      setSuccess(true);

    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <main>
        <h1>Cadastro concluído</h1>
        <p>{message}</p>

        <button onClick={onBackToLogin}>
          Ir para login
        </button>
      </main>
    );
  }

  return (
    <main>
      <h1>Cadastro - Project PJ</h1>

      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Nome"
          value={name}
          onChange={(event) => setName(event.target.value)}
          minLength={2}
          maxLength={120}
          required
        />

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
          minLength={8}
          maxLength={128}
          required
        />

        <select
          value={role}
          onChange={(event) => setRole(event.target.value)}
        >
          <option value="contractor">Contratante</option>
          <option value="provider">Contratado</option>
        </select>

        <button type="submit" disabled={loading}>
          {loading ? 'Cadastrando...' : 'Cadastrar'}
        </button>
      </form>

      {message && <p>{message}</p>}

      <button onClick={onBackToLogin}>
        Voltar para login
      </button>
    </main>
  );
}

export default Register;
