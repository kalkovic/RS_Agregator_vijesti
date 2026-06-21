import axios from 'axios';

export const analyticsApi = axios.create({
  baseURL: import.meta.env.VITE_ANALYTICS_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const newsApi = axios.create({
  baseURL: import.meta.env.VITE_NEWS_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authApi = axios.create({
  baseURL: import.meta.env.VITE_AUTH_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});