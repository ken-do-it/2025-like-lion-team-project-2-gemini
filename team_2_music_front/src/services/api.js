import axios from 'axios';

// Force port 8002 for now
// const API_BASE_URL = 'http://localhost:8002';

// const API_BASE_URL = 'http://15.165.200.236:8000/api/v1';
// 아래있는걸로 변경이 되어야 배포되고 문제가 확인이 가능
// const API_BASE_URL = 'http://15.165.200.236:8000';
const API_BASE_URL = 'http://3.35.45.78:8000';
console.log('API_BASE_URL:', API_BASE_URL);

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
    (config) => {
        let token = localStorage.getItem('auth_token');

        // Development: Use mock token if not present
        if (!token && import.meta.env.DEV) {
            token = 'dev-token-2025';
            console.log('Using developer token for development');
        }

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor for handling errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('auth_token');
            // Redirect to home page instead of login (login page doesn't exist yet)
            window.location.href = '/';
        }
        return Promise.reject(error);
    }
);

// Track APIs
export const trackAPI = {
    getAll: (params) => api.get('/api/v1/tracks', { params }),
    getById: (id) => api.get(`/api/v1/tracks/${id}`),
    search: (query, params) => api.get('/api/v1/tracks/search', { params: { q: query, ...params } }),
    initiateUpload: (data) => api.post('/api/v1/tracks/upload/initiate', data),
    finalizeUpload: (data) => api.post('/api/v1/tracks/upload/finalize', data),
    update: (id, data) => api.patch(`/api/v1/tracks/${id}`, data),
    stream: (id) => `${API_BASE_URL}/api/v1/tracks/${id}/stream`,
};

// User APIs
export const userAPI = {
    me: () => api.get('/api/v1/users/me'),
    updateProfile: (data) => api.patch('/api/v1/users/me', data),
};

// Like APIs
export const likeAPI = {
    toggle: (trackId) => api.post('/api/v1/likes', { track_id: trackId }),
    getByTrack: (trackId) => api.get(`/api/v1/likes/track/${trackId}`),
};

// Comment APIs
export const commentAPI = {
    create: (data) => api.post('/api/v1/comments', data),
    getByTrack: (trackId) => api.get(`/api/v1/comments/track/${trackId}`),
    delete: (id) => api.delete(`/api/v1/comments/${id}`),
};

// Follow APIs
export const followAPI = {
    toggle: (userId) => api.post('/api/v1/follows', { followed_user_id: userId }),
    getFollowers: (userId) => api.get(`/api/v1/follows/${userId}/followers`),
    getFollowing: (userId) => api.get(`/api/v1/follows/${userId}/following`),
};

// Playlist APIs
export const playlistAPI = {
    getAll: () => api.get('/api/v1/playlists'),
    getById: (id) => api.get(`/api/v1/playlists/${id}`),
    create: (data) => api.post('/api/v1/playlists', data),
    update: (id, data) => api.patch(`/api/v1/playlists/${id}`, data),
    delete: (id) => api.delete(`/api/v1/playlists/${id}`),
    addTrack: (id, trackId) => api.post(`/api/v1/playlists/${id}/tracks/${trackId}`),
    removeTrack: (id, trackId) => api.delete(`/api/v1/playlists/${id}/tracks/${trackId}`),
};

export default api;
