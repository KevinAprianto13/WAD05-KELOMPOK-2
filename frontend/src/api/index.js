import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' }
})

// Attach JWT token to every request
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Handle 401 globally
api.interceptors.response.use(
  res => res,
  err => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

// ── Auth ──────────────────────────────────────────────────────────────────────
export const authApi = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
}

// ── Products ──────────────────────────────────────────────────────────────────
export const productsApi = {
  list: (params) => api.get('/products', { params }),
  get: (id) => api.get(`/products/${id}`),
  create: (data) => api.post('/products', data),
  update: (id, data) => api.put(`/products/${id}`, data),
  uploadImage: (id, data) => api.post(`/products/${id}/image`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  uploadImages: (id, data) => api.post(`/products/${id}/images`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteImage: (productId, imageId) => api.delete(`/products/${productId}/images/${imageId}`),
  delete: (id) => api.delete(`/products/${id}`),
}

// ── Categories ────────────────────────────────────────────────────────────────
export const categoriesApi = {
  list: () => api.get('/categories'),
  create: (data) => api.post('/categories', data),
  delete: (id) => api.delete(`/categories/${id}`),
}

// ── Cart ──────────────────────────────────────────────────────────────────────
export const cartApi = {
  get: () => api.get('/cart'),
  addItem: (data) => api.post('/cart/items', data),
  updateItem: (id, data) => api.put(`/cart/items/${id}`, data),
  removeItem: (id) => api.delete(`/cart/items/${id}`),
  clear: () => api.delete('/cart'),
}

// ── Orders ────────────────────────────────────────────────────────────────────
export const ordersApi = {
  checkout: (data) => api.post('/orders/checkout', data),
  myOrders: () => api.get('/orders/me'),
  allOrders: () => api.get('/orders'),
  updateStatus: (id, status) => api.put(`/orders/${id}/status`, { status }),
}

// ── Admin Dashboard ───────────────────────────────────────────────────────────
export const dashboardApi = {
  stats: () => api.get('/admin/dashboard/stats'),
  sales: () => api.get('/admin/dashboard/sales'),
}

export const bannersApi = {
  list: () => api.get('/banners'),
  save: (position, data) => api.post(`/banners/${position}`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  delete: (position) => api.delete(`/banners/${position}`),
}

// ── Chat ──────────────────────────────────────────────────────────────────────
export const chatApi = {
  getSessions: () => api.get('/chat/sessions'),
  getMessages: (userId) => api.get(`/chat/${userId}`),
  sendMessage: (data) => api.post('/chat/', data),
}

// ── Notifications ─────────────────────────────────────────────────────────────
export const notificationApi = {
  getNotifications: () => api.get('/notifications/'),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
  markAllAsRead: () => api.put('/notifications/read-all'),
}
