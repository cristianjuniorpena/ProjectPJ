import { useState } from 'react';

import PostList from './PostList';
import CreatePost from './CreatePost';

import './Dashboard.css';

function Dashboard({ user, onLogout }) {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  function handlePostCreated() {
    setRefreshTrigger((prev) => prev + 1);
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <span className="brand">
          <span className="brand__mark" aria-hidden="true">PJ</span>
          Project PJ
        </span>

        <nav className="topbar__nav" aria-label="Navegação principal">
          <a href="#overview">Visão geral</a>
          <a href="#publications">Publicações</a>
          {user.role === 'contractor' && (
            <a href="#create-post">Nova publicação</a>
          )}
        </nav>

        <div className="topbar__user">
          <span className="avatar" aria-hidden="true">
            {user.name?.charAt(0)?.toUpperCase() ?? '?'}
          </span>
          <span className="topbar__identity">
            <strong>{user.name}</strong>
            <span className="role-badge">
              {user.role === 'contractor' ? 'Contratante' : 'Prestador'}
            </span>
          </span>
          <button
            className="button button--ghost button--small"
            onClick={onLogout}
          >
            Sair
          </button>
        </div>
      </header>

      <main className="dashboard">
        <div className="dashboard__intro" id="overview">
          <h1>Bem-vindo, {user.name}!</h1>
          <p>
            Gerencie suas publicações, acompanhe oportunidades e mantenha
            tudo organizado em um só lugar.
          </p>
        </div>

        <section className="card profile-card" aria-label="Dados do perfil">
          <div className="profile-card__item">
            <span className="profile-card__label">ID:</span>
            <p className="profile-card__value">{user.id}</p>
          </div>
          <div className="profile-card__item">
            <span className="profile-card__label">Email:</span>
            <p className="profile-card__value">{user.email}</p>
          </div>
          <div className="profile-card__item">
            <span className="profile-card__label">Perfil:</span>
            <p className="profile-card__value">{user.role}</p>
          </div>
          <div className="profile-card__item">
            <span className="profile-card__label">Cadastro:</span>
            <p className="profile-card__value">{user.created_at}</p>
          </div>
        </section>

        {user.role === 'contractor' && (
          <CreatePost onPostCreated={handlePostCreated} />
        )}

        <PostList refreshTrigger={refreshTrigger} user={user}/>
      </main>
    </div>
  );
}

export default Dashboard;