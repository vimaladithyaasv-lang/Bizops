import axios from 'axios';
const baseURL =
  process.env.NODE_ENV === 'production'
    ? 'https://api.production.com/'
    : 'https://bizops-hackathon.onrender.com';

const apiClient = axios.create({
  baseURL,
});

export default apiClient;