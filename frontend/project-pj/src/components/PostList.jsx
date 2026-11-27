
import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';

function PostList({ refreshTrigger, user }) {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [editingPostId, setEditingPostId] = useState(null);
  const [editData, setEditData] = useState({
    title: '',
    description: '',
    category: '',
    budget: '',
    status: 'open'
  });

  const [saving, setSaving] = useState(false);
  const [editError, setEditError] = useState('');

  useEffect(() => {
    async function loadPosts() {
      setLoading(true);
      setError('');

      try {
        const data = await apiRequest('/posts/');
        setPosts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadPosts();
  }, [refreshTrigger]);

  function startEditing(post) {
    setEditingPostId(post.id);

    setEditData({
      title: post.title,
      description: post.description,
      category: post.category,
      budget: post.budget ?? '',
      status: post.status
    });

    setEditError('');
  }

  async function handleDelete(postId) {
    const confirmed = window.confirm(
      'Tem certeza de que deseja excluir esta publicação?'
    );
  
    if (!confirmed) return;
  
    try {
      const token = sessionStorage.getItem('access_token');
  
      await apiRequest(
        `/posts/${postId}`,
        {
          method: 'DELETE'
        },
        token
      );
  
      setPosts((currentPosts) =>
        currentPosts.filter((post) => post.id !== postId)
      );
  
    } catch (err) {
      setError(err.message);
    }
  }

  function cancelEditing() {
    setEditingPostId(null);
    setEditError('');
  }

  async function handleUpdate(event) {
    event.preventDefault();

    setSaving(true);
    setEditError('');

    const postData = {
      title: editData.title,
      description: editData.description,
      category: editData.category,
      budget:
        editData.budget === ''
          ? null
          : Number(editData.budget),
      status: editData.status
    };

    try {
      const token = sessionStorage.getItem('access_token');

      const updatedPost = await apiRequest(
        `/posts/${editingPostId}`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(postData)
        },
        token
      );

      setPosts((currentPosts) =>
        currentPosts.map((post) =>
          post.id === updatedPost.id ? updatedPost : post
        )
      );

      setEditingPostId(null);

    } catch (err) {
      setEditError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return <p>Carregando publicações...</p>;
  }

  if (error) {
    return <p>Erro: {error}</p>;
  }

  return (
    <section>
      <h2>Publicações disponíveis</h2>

      {posts.length === 0 ? (
        <p>Nenhuma publicação encontrada.</p>
      ) : (
        posts.map((post) => (
          <article key={post.id}>
            {editingPostId === post.id ? (
              <form onSubmit={handleUpdate}>
                <h3>Editar publicação</h3>

                <div>
                  <label>Título</label>
                  <input
                    value={editData.title}
                    onChange={(event) =>
                      setEditData({
                        ...editData,
                        title: event.target.value
                      })
                    }
                    minLength={3}
                    maxLength={150}
                    required
                  />
                </div>

                <div>
                  <label>Descrição</label>
                  <textarea
                    value={editData.description}
                    onChange={(event) =>
                      setEditData({
                        ...editData,
                        description: event.target.value
                      })
                    }
                    minLength={10}
                    required
                  />
                </div>

                <div>
                  <label>Categoria</label>
                  <input
                    value={editData.category}
                    onChange={(event) =>
                      setEditData({
                        ...editData,
                        category: event.target.value
                      })
                    }
                    minLength={2}
                    maxLength={100}
                    required
                  />
                </div>

                <div>
                  <label>Orçamento</label>
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    value={editData.budget}
                    onChange={(event) =>
                      setEditData({
                        ...editData,
                        budget: event.target.value
                      })
                    }
                  />
                </div>

                <div>
                  <label>Status</label>
                  <select
                    value={editData.status}
                    onChange={(event) =>
                      setEditData({
                        ...editData,
                        status: event.target.value
                      })
                    }
                  >
                    <option value="open">Aberto</option>
                    <option value="closed">Fechado</option>
                  </select>
                </div>

                <button type="submit" disabled={saving}>
                  {saving ? 'Salvando...' : 'Salvar alterações'}
                </button>

                <button
                  type="button"
                  onClick={cancelEditing}
                  disabled={saving}
                >
                  Cancelar
                </button>

                {editError && <p>Erro: {editError}</p>}
              </form>
            ) : (
              <>
                <h3>{post.title}</h3>

                <p>{post.description}</p>
                <p>Categoria: {post.category}</p>

                <p>
                  Orçamento:{' '}
                  {post.budget !== null
                    ? `R$ ${post.budget}`
                    : 'Não informado'}
                </p>

                <p>Status: {post.status}</p>
                <p>Contratante ID: {post.user_id}</p>

                {user?.role === 'contractor' &&
                user.id === post.user_id && (
                    <>
                    <button onClick={() => startEditing(post)}>
                        Editar
                    </button>

                    <button onClick={() => handleDelete(post.id)}>
                        Excluir
                    </button>   
                    </>
                )}
              </>
            )}
          </article>
        ))
      )}
    </section>
  );
}

export default PostList;
