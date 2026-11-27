
const API_URL = import.meta.env.VITE_API_URL?.replace(/\/+$/, '');

export async function apiRequest(endpoint, options = {}, token = null) {
  const headers = {
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(
    `${API_URL}/${endpoint.replace(/^\/+/, '')}`,
    {
      ...options,
      headers,
    }
  );

  const responseText = await response.text();

  let data = null;

  if (responseText) {
    try {
      data = JSON.parse(responseText);
    } catch {
      throw new Error('A API retornou uma resposta que não é JSON.');
    }
  }

  if (!response.ok) {
    const error = new Error(
      data?.detail || `Erro HTTP: ${response.status}`
    );
  
    error.status = response.status;
  
    throw error;
  }
  return data;
}
