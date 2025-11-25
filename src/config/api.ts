// Client-side API configuration
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const isProduction = !isDevelopment;

// Use different API endpoints based on environment
// In development, use mock API server, in production use Vercel API routes
export const API_BASE_URL = isDevelopment ? 'http://localhost:3001/api' : '/api';

// API endpoints
export const API_ENDPOINTS = {
  // Health check
  health: `${API_BASE_URL}/health`,
  
  // Authentication endpoints
  auth: {
    registerPatient: `${API_BASE_URL}/auth/register/patient`,
    registerDoctor: `${API_BASE_URL}/auth/register/doctor`,
    registerHealthworker: `${API_BASE_URL}/auth/register/healthworker`,
    loginPatient: `${API_BASE_URL}/auth/login/patient`,
    loginDoctor: `${API_BASE_URL}/auth/login/doctor`,
    loginHealthworker: `${API_BASE_URL}/auth/login/healthworker`,
  },
  
  // Profile endpoints
  profile: {
    me: `${API_BASE_URL}/me`,
  }
};

// Default fetch options
export const defaultFetchOptions = {
  headers: {
    'Content-Type': 'application/json',
  },
};

// Helper function to get auth headers
export function getAuthHeaders(token?: string) {
  const authToken = token || localStorage.getItem('authToken');
  return {
    ...defaultFetchOptions.headers,
    ...(authToken && { Authorization: `Bearer ${authToken}` }),
  };
}

export default {
  API_BASE_URL,
  API_ENDPOINTS,
  defaultFetchOptions,
  getAuthHeaders,
  isDevelopment,
  isProduction,
};