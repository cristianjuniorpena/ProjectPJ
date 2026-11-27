import { useState } from 'react';
import { apiRequest } from '../api/client';

import './Auth.css';

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
    <div className="auth-shell">
      <div className="auth-layout">
        <aside className="auth-aside">
          <span className="brand">
            <span className="brand__mark" aria-hidden="true">PJ</span>
            Project PJ
          </span>

          <div>
            <h2 className="auth-aside__title">Contrate bem. Trabalhe melhor.</h2>
            <p className="auth-aside__text">
              Um espaço direto para contratantes e prestadores de serviços
              encontrarem oportunidades e organizarem suas publicações.
            </p>
          </div>

          <ul className="auth-benefits">
            <li>
              <span className="auth-benefits__icon" aria-hidden="true">1</span>
              <span>Publique serviços com informações claras e objetivas.</span>
            </li>
            <li>
              <span className="auth-benefits__icon" aria-hidden="true">2</span>
              <span>Encontre oportunidades de acordo com o seu perfil.</span>
            </li>
            <li>
              <span className="auth-benefits__icon" aria-hidden="true">3</span>
              <span>Gerencie suas publicações em um só lugar.</span>
            </li>
          </ul>

          <p className="auth-aside__footer">Plataforma de conexão profissional PJ.</p>
        </aside>

        <main className="auth-panel">
          <div className="auth-card">
            <header className="auth-card__header">
              <p className="auth-card__eyebrow">Acesse sua conta</p>
              <h1>Bem-vindo de volta</h1>
              <p className="auth-card__subtitle">
                Informe seus dados para continuar.
              </p>
            </header>

            <form className="auth-form" onSubmit={handleLogin}>
              <div className="field">
                <label htmlFor="login-email">Email</label>
                <input
                  id="login-email"
                  type="email"
                  placeholder="seu@email.com"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  required
                />
              </div>

              <div className="field">
                <label htmlFor="login-password">Senha</label>
                <input
                  id="login-password"
                  type="password"
                  placeholder="Sua senha"
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  required
                />
              </div>

              <button
                className="button button--primary auth-form__submit"
                type="submit"
              >
                Entrar
              </button>

              {message && (
                <p
                  className={`alert ${
                    message.startsWith('Erro')
                      ? 'alert--error'
                      : message.includes('sucesso')
                        ? 'alert--success'
                        : 'alert--info'
                  }`}
                >
                  {message}
                </p>
              )}
            </form>

            <footer className="auth-card__footer">
              <span className="auth-card__footer-text">
                Ainda não tem uma conta?
              </span>
              <button
                type="button"
                className="button button--secondary button--small"
                onClick={onRegister}
              >
                Criar uma conta
              </button>
            </footer>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Login;