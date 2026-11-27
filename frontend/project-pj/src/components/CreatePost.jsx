import { useState } from 'react';
import { apiRequest } from '../api/client';

import './CreatePost.css';

function CreatePost({ onPostCreated }) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState('');
  const [budget, setBudget] = useState('');

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setMessage('');

    const postData = {
      title,
      description,
      category,
      budget: budget.trim() === '' ? null : Number(budget)
    };

    try {
      const token = sessionStorage.getItem('access_token');

      await apiRequest(
        '/posts/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(postData)
        },
        token
      );

      setTitle('');
      setDescription('');
      setCategory('');
      setBudget('');

      setMessage('Publicação criada com sucesso!');
      onPostCreated();

    } catch (error) {
      setMessage(`Erro: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="create-post" id="create-post">
      <header className="section-header">
        <div>
          <h2>Criar publicação</h2>
          <p>Campos marcados com * são obrigatórios.</p>
        </div>
      </header>

      <form className="card form-card form-grid" onSubmit={handleSubmit}>
        <div className="field field--full">
          <label>
            Título <span className="field__required" aria-hidden="true">*</span>
          </label>
          <input
            type="text"
            placeholder="Ex.: Desenvolvimento de site institucional"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            required
            minLength={3}
            maxLength={150}
          />
        </div>

        <div className="field field--full">
          <label>
            Descrição <span className="field__required" aria-hidden="true">*</span>
          </label>
          <textarea
            placeholder="Descreva o serviço, os requisitos e o resultado esperado."
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            required
            minLength={10}
          />
          <p className="field__hint">Mínimo de 10 caracteres.</p>
        </div>

        <div className="field">
          <label>
            Categoria <span className="field__required" aria-hidden="true">*</span>
          </label>
          <input
            type="text"
            placeholder="Ex.: Tecnologia"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
            required
            minLength={2}
            maxLength={100}
          />
        </div>

        <div className="field">
          <label>
            Orçamento
            <span className="field__optional">(opcional)</span>
          </label>
          <input
            type="number"
            placeholder="0,00"
            value={budget}
            onChange={(event) => setBudget(event.target.value)}
            min="0"
            step="0.01"
          />
        </div>

        <div className="form-actions">
          <button
            className="button button--primary"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Publicando...' : 'Criar publicação'}
          </button>
          <span className="form-note">Você pode editar ou excluir depois.</span>
        </div>
      </form>

      {message && (
        <p
          className={`alert create-post__message ${
            message.startsWith('Erro') ? 'alert--error' : 'alert--success'
          }`}
        >
          {message}
        </p>
      )}
    </section>
  );
}

export default CreatePost;
