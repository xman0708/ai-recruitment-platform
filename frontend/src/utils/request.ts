import axios from 'axios';

// Create axios instance
const request = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Request interceptor
request.interceptors.request.use(
    (config) => {
        // We could add token logic here in the future
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
request.interceptors.response.use(
    (response) => {
        return response.data;
    },
    (error) => {
        if (error.response && error.response.status === 401) {
            // Future: Handle unauthorized, maybe redirect to login
            localStorage.removeItem('token');
        }
        return Promise.reject(error);
    }
);

export default request;
