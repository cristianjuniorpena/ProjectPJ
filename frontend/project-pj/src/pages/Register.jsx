
import { useState } from 'react';
import { apiRequest } from '../api/client';

import './Auth.css';

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
      <div className="auth-shell">
        <div className="card auth-success">
          <span className="auth-success__icon" aria-hidden="true">✓</span>
          <h1>Cadastro concluído</h1>
          <p>{message}</p>

          <button
            className="button button--primary"
            onClick={onBackToLogin}
          >
            Ir para login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-shell">
      <div className="auth-layout">
        <aside className="auth-aside">
          <span className="brand">
            <span className="brand__mark" aria-hidden="true">PJ</span>
            Project PJ
          </span>

          <div>
            <h2 className="auth-aside__title">Faça parte da plataforma.</h2>
            <p className="auth-aside__text">
              Crie sua conta para publicar serviços ou encontrar oportunidades
              de trabalho como profissional autônomo.
            </p>
          </div>

          <ul className="auth-benefits">
            <li>
              <span className="auth-benefits__icon" aria-hidden="true">1</span>
              <span>Escolha seu perfil: contratante ou prestador.</span>
            </li>
            <li>
              <span className="auth-benefits__icon" aria-hidden="true">2</span>
              <span>Organize publicações com título, categoria e orçamento.</span>
            </li>
            <li>
              <span className="auth-benefits__icon" aria-hidden="true">3</span>
              <span>Acompanhe oportunidades em um ambiente simples.</span>
            </li>
          </ul>

          <p className="auth-aside__footer">Plataforma de conexão profissional PJ.</p>
        </aside>

        <main className="auth-panel">
          <div className="auth-card">
            <header className="auth-card__header">
              <p className="auth-card__eyebrow">Crie sua conta</p>
              <h1>Cadastro</h1>
              <p className="auth-card__subtitle">
                Preencha os dados abaixo para começar.
              </p>
            </header>

            <form className="auth-form" onSubmit={handleRegister}>
              <div className="field">
                <label htmlFor="register-name">Nome completo</label>
                <input
                  id="register-name"
                  type="text"
                  placeholder="Seu nome"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  minLength={2}
                  maxLength={120}
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="register-email">Email</label>
                <input
                  id="register-email"
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="register-password">Senha</label>
                <input
                  id="register-password"
                  type="password"
                  placeholder="Mínimo de 8 caracteres"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  minLength={8}
                  maxLength={128}
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="register-role">Tipo de perfil</label>
                <select
                  id="register-role"
                  value={role}
                  onChange={(event) => setRole(event.target.value)}
                >
                  <option value="contractor">Contratante — publica serviços</option>
                  <option value="provider">Prestador — encontra oportunidades</option>
                </select>
                <p className="field__hint">
                  Contratantes criam publicações. Prestadores apenas consultam.
                </p>
              </div>

              <button
                className="button button--primary auth-form__submit"
                type="submit"
                disabled={loading}
              >
                {loading ? 'Cadastrando...' : 'Cadastrar'}
              </button>

              {message && (
                <p className={`alert ${success ? 'alert--success' : 'alert--error'}`}>
                  {message}
                </p>
              )}
            </form>

            <footer className="auth-card__footer">
              <span className="auth-card__footer-text">Já possui uma conta?</span>
              <button
                type="button"
                className="button button--secondary button--small"
                onClick={onBackToLogin}
              >
                Voltar para login
              </button>
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Register;
