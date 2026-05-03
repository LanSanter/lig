// src/api/client.js
const BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const apiClient = {
  async post(endpoint, data) {
    const url = `${BASE_URL}/api${endpoint}`; // 自動轉換為完整網址
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
  },

  async get(endpoint) {
    const url = `${BASE_URL}/api${endpoint}`;
    const response = await fetch(url);
    return response.json();
  }
};