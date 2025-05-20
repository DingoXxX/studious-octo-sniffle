// src/api.js
// Centralized API service for connecting React UI to FastAPI backend

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function registerUser(name, email, password) {
  const response = await fetch(`${API_BASE_URL}/users/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password })
  });
  if (!response.ok) throw new Error('Registration failed');
  return response.json();
}

export async function login(username, password) {
  const response = await fetch(`${API_BASE_URL}/auth/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  if (!response.ok) throw new Error('Login failed');
  return response.json();
}

export async function fetchUserAccount(userId, token) {
  const response = await fetch(`${API_BASE_URL}/users/${userId}/account`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error('Failed to fetch account');
  return response.json();
}

export async function fetchTransactions(accountId, token) {
  const response = await fetch(`${API_BASE_URL}/accounts/${accountId}/transactions`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!response.ok) throw new Error('Failed to fetch transactions');
  return response.json();
}

// Add more functions for other endpoints as needed
