import { useState } from 'react';
import { apiRequest } from '../api/client';

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
    <section>
      <h2>Criar publicação</h2>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Título</label>
          <input
            type="text"
            value={title}
            onChange={(event) => setTitle(event.target.value)}
            required
            minLength={3}
            maxLength={150}
          />
        </div>

        <div>
          <label>Descrição</label>
          <textarea
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            required
            minLength={10}
          />
        </div>

        <div>
          <label>Categoria</label>
          <input
            type="text"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
            required
            minLength={2}
            maxLength={100}
          />
        </div>

        <div>
          <label>Orçamento (opcional)</label>
          <input
            type="number"
            value={budget}
            onChange={(event) => setBudget(event.target.value)}
            min="0"
            step="0.01"
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Publicando...' : 'Criar publicação'}
        </button>
      </form>

      {message && <p>{message}</p>}
    </section>
  );
}

export default CreatePost;
