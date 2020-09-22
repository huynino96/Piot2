import axios from 'axios';
import { API_URL } from '../utils/constants';

const instance = axios.create({
    baseURL: API_URL,
});

instance.interceptors.request.use(function handler(config) {
    const token = typeof window !== 'undefined' ? window.localStorage.getItem('access_token') : null;
    if (token) {
        config.headers.Authorization = token;
    }
    return config;
});

export default instance;
