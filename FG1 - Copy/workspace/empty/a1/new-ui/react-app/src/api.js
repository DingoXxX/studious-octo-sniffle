const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Handle API responses
const handleResponse = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }
  return response.json();
};

// Authentication API
export const auth = {
  login: async (username, password) => {
    const response = await fetch(`${API_BASE}/auth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ username, password }),
      credentials: 'include',
    });
    return handleResponse(response);
  },
  
  register: async (userData) => {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  logout: async () => {
    localStorage.removeItem('token');
  }
};

// Protected API calls
const authFetch = async (url, options = {}) => {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const response = await fetch(url, { ...options, headers });
  return handleResponse(response);
};

// Account API
export const accounts = {
  getAll: () => authFetch(`${API_BASE}/accounts`),
  getDetails: (id) => authFetch(`${API_BASE}/accounts/${id}`),
  getTransactions: (id) => authFetch(`${API_BASE}/accounts/${id}/transactions`),
  deposit: (id, amount) => authFetch(`${API_BASE}/accounts/${id}/deposit`, {
    method: 'POST',
    body: JSON.stringify({ amount }),
  }),
  withdraw: (id, amount) => authFetch(`${API_BASE}/accounts/${id}/withdraw`, {
    method: 'POST',
    body: JSON.stringify({ amount }),
  }),
};

// User API
export const users = {
  getProfile: () => authFetch(`${API_BASE}/users/me`),
  updateProfile: (data) => authFetch(`${API_BASE}/users/me`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
};