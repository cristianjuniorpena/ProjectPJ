import { useState } from 'react';

import PostList from './PostList';
import CreatePost from './CreatePost';

function Dashboard({ user, onLogout }) {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  function handlePostCreated() {
    setRefreshTrigger((prev) => prev + 1);
  }

  return (
    <main>
      <h1>Bem-vindo, {user.name}!</h1>

      <p>ID: {user.id}</p>
      <p>Email: {user.email}</p>
      <p>Perfil: {user.role}</p>
      <p>Cadastro: {user.created_at}</p>

      <button onClick={onLogout}>
        Sair
      </button>

      {user.role === 'contractor' && (
        <CreatePost onPostCreated={handlePostCreated} />
      )}

      <PostList refreshTrigger={refreshTrigger} user={user}/>
    </main>
  );
}

export default Dashboard;