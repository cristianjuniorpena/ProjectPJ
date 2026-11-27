
import { useEffect, useState } from 'react';
import { apiRequest } from '../api/client';

import './PostList.css';

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

  const PAGE_SIZE = 20;

  const [page, setPage] = useState(0);

  const [filters, setFilters] = useState({
    category: '',
    status: '',
    search: '',
    min_budget: '',
    max_budget: ''
  });
  
  const [appliedFilters, setAppliedFilters] = useState({
    category: '',
    status: '',
    search: '',
    min_budget: '',
    max_budget: ''
  });
  
  const [filterError, setFilterError] = useState('');

  useEffect(() => {
    async function loadPosts() {
      setLoading(true);
      setError('');
  
      try {
        const token = sessionStorage.getItem('access_token');
  
        const params = new URLSearchParams({
          limit: PAGE_SIZE,
          offset: page * PAGE_SIZE
        });
  
        Object.entries(appliedFilters).forEach(([key, value]) => {
          if (value.trim() !== '') {
            params.append(key, value.trim());
          }
        });
  
        const data = await apiRequest(
          `/posts/?${params.toString()}`,
          {},
          token
        );
  
        setPosts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
  
    loadPosts();
  }, [refreshTrigger, page, appliedFilters]);

  function handleApplyFilters(event) {
    event.preventDefault();
  
    const min = filters.min_budget;
    const max = filters.max_budget;
  
    if (
      min !== '' &&
      max !== '' &&
      Number(min) > Number(max)
    ) {
      setFilterError(
        'O orçamento mínimo não pode ser maior que o máximo.'
      );
      return;
    }
  
    setFilterError('');
    setPage(0);
    setAppliedFilters({ ...filters });
  }
  
  function handleClearFilters() {
    const emptyFilters = {
      category: '',
      status: '',
      search: '',
      min_budget: '',
      max_budget: ''
    };
  
    setFilters(emptyFilters);
    setAppliedFilters(emptyFilters);
    setFilterError('');
    setPage(0);
  }

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
      
      if (posts.length === 1 && page > 0) {
        setPage(current => current - 1);
      }
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
    return (
      <section className="posts-section">
        <div className="state-message" role="status">
          Carregando publicações...
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="posts-section">
        <div className="alert alert--error">Erro: {error}</div>
      </section>
    );
  }

  return (
    <section className="posts-section" id="publications">
      <header className="section-header">
        <div>
          <h2>Publicações disponíveis</h2>
          <p>Use os filtros para encontrar as oportunidades certas.</p>
        </div>
      </header>

      <form className="card filters" onSubmit={handleApplyFilters}>
        <div className="filters__grid">
          <div className="field field--search">
            <label htmlFor="filter-search">Buscar por título ou descrição</label>
            <input
              id="filter-search"
              type="text"
              value={filters.search}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  search: event.target.value
                })
              }
              placeholder="Digite o que procura"
            />
          </div>

          <div className="field">
            <label htmlFor="filter-category">Categoria</label>
            <input
              id="filter-category"
              type="text"
              value={filters.category}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  category: event.target.value
                })
              }
              placeholder="Ex.: Tecnologia"
              minLength={2}
            />
          </div>

          <div className="field">
            <label htmlFor="filter-status">Status</label>
            <select
              id="filter-status"
              value={filters.status}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  status: event.target.value
                })
              }
            >
              <option value="">Todos</option>
              <option value="open">Aberto</option>
              <option value="closed">Fechado</option>
            </select>
          </div>

          <div className="field">
            <label htmlFor="filter-min-budget">Orçamento mínimo</label>
            <input
              id="filter-min-budget"
              type="number"
              min="0"
              step="0.01"
              value={filters.min_budget}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  min_budget: event.target.value
                })
              }
            />
          </div>

          <div className="field">
            <label htmlFor="filter-max-budget">Orçamento máximo</label>
            <input
              id="filter-max-budget"
              type="number"
              min="0"
              step="0.01"
              value={filters.max_budget}
              onChange={(event) =>
                setFilters({
                  ...filters,
                  max_budget: event.target.value
                })
              }
            />
          </div>
        </div>

        <div className="filters__actions">
          <button className="button button--primary" type="submit">
            Aplicar filtros
          </button>

          <button
            className="button button--secondary"
            type="button"
            onClick={handleClearFilters}
          >
            Limpar filtros
          </button>

          {filterError && <p className="alert alert--error">{filterError}</p>}
        </div>
      </form>

      {posts.length === 0 ? (
        <div className="empty-state">
          <strong>Nenhuma publicação encontrada.</strong>
          <span>Ajuste os filtros ou tente outra busca.</span>
        </div>
      ) : (
        <div className="post-grid">
          {posts.map((post) => (
            <article className="post-card" key={post.id}>
              {editingPostId === post.id ? (
                <form className="form-grid edit-form" onSubmit={handleUpdate}>
                  <h3 className="edit-form__title">Editar publicação</h3>

                  <div className="field">
                    <label>
                      Título{' '}
                      <span className="field__required" aria-hidden="true">*</span>
                    </label>
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

                  <div className="field field--full">
                    <label>
                      Descrição{' '}
                      <span className="field__required" aria-hidden="true">*</span>
                    </label>
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

                  <div className="field">
                    <label>
                      Categoria{' '}
                      <span className="field__required" aria-hidden="true">*</span>
                    </label>
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

                  <div className="field">
                    <label>
                      Orçamento
                      <span className="field__optional">(opcional)</span>
                    </label>
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

                  <div className="field field--full">
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

                  <div className="form-actions">
                    <button
                      className="button button--primary"
                      type="submit"
                      disabled={saving}
                    >
                      {saving ? 'Salvando...' : 'Salvar alterações'}
                    </button>

                    <button
                      className="button button--secondary"
                      type="button"
                      onClick={cancelEditing}
                      disabled={saving}
                    >
                      Cancelar
                    </button>
                  </div>

                  {editError && (
                    <p className="alert alert--error">Erro: {editError}</p>
                  )}
                </form>
              ) : (
                <>
                  <div className="post-card__header">
                    <span className="post-card__category">{post.category}</span>
                    <span className={`status-badge status-badge--${post.status}`}>
                      {post.status === 'open' ? 'Aberto' : 'Fechado'}
                    </span>
                  </div>

                  <h3 className="post-card__title">{post.title}</h3>

                  <p className="post-card__description">{post.description}</p>

                  {post.contractor?.name && (
                    <p className="post-card__contractor">
                      Contratante: {post.contractor.name}
                    </p>
                  )}

                  <div className="post-card__footer">
                    <div className="post-card__meta">
                      <span className="post-card__budget">
                        Orçamento:{' '}
                        {post.budget !== null
                          ? `R$ ${post.budget}`
                          : 'Não informado'}
                      </span>
                      <span>Contratante ID: {post.user_id}</span>
                    </div>

                    {user?.role === 'contractor' &&
                      user.id === post.user_id && (
                        <div className="post-card__actions">
                          <button
                            className="button button--secondary button--small"
                            onClick={() => startEditing(post)}
                          >
                            Editar
                          </button>

                          <button
                            className="button button--danger button--small"
                            onClick={() => handleDelete(post.id)}
                          >
                            Excluir
                          </button>
                        </div>
                      )}
                  </div>
                </>
              )}
            </article>
          ))}
        </div>
      )}
      <nav className="pagination" aria-label="Paginação de publicações">
        <button
          className="button button--secondary button--small"
          onClick={() => setPage(current => current - 1)}
          disabled={page === 0 || loading}
        >
          Anterior
        </button>

        <span className="pagination__label">
          Página {page + 1}
        </span>

        <button
          className="button button--secondary button--small"
          onClick={() => setPage(current => current + 1)}
          disabled={posts.length < PAGE_SIZE || loading}
        >
          Próxima
        </button>
      </nav>
    </section>
  );
}

export default PostList;
