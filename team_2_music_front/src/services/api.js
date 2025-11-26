import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth_token');
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
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Track APIs
export const trackAPI = {
    getAll: (params) => api.get('/api/v1/tracks', { params }),
    getById: (id) => api.get(`/api/v1/tracks/${id}`),
    initiateUpload: (data) => api.post('/api/v1/tracks/upload/initiate', data),
    finalizeUpload: (data) => api.post('/api/v1/tracks/upload/finalize', data),
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
