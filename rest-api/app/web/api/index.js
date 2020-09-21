import axios from 'axios';
import { API_URL } from '../utils/constants';

const instance = axios.create({
    baseURL: API_URL,
});

instance.interceptors.request.use(function handler(config) {
    const token = typeof window !== 'undefined' ? window.localStorage.getItem('token') : null;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default instance;
