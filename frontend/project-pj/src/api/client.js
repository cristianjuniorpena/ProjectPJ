const API_URL = import.meta.env.VITE_API_URL;

export async function apiRequest(
  endpoint,
  options = {},
  token = null
) {
  const headers = {
    ...options.headers,
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail || `Erro HTTP: ${response.status}`
    );
  }

  return data;
}