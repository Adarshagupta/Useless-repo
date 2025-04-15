import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Create axios instance
const api = axios.create({
  baseURL: 'http://10.1.42.77:8006',
  headers: {
    'Content-Type': 'application/json',
  },
});

// For development, disable mock data to use the real backend
const USE_MOCK_DATA = true;

// Mock credentials for development mode
const MOCK_CREDENTIALS = {
  username: 'johndoe',
  email: 'johndoe@example.com',
  password: 'secret',
  full_name: 'John Doe'
};

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Check if error.response exists before accessing its properties
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      // Clear the token and redirect to login
      await AsyncStorage.removeItem('token');
      // In a real app, you would redirect to login here
    }

    return Promise.reject(error);
  }
);

// Mock data
const mockChartData = [
  { date: '2023-01-01', price: 130.45 },
  { date: '2023-01-02', price: 132.64 },
  { date: '2023-01-03', price: 134.98 },
  { date: '2023-01-04', price: 133.75 },
  { date: '2023-01-05', price: 135.21 },
  { date: '2023-01-06', price: 138.45 },
  { date: '2023-01-07', price: 140.10 },
  { date: '2023-01-08', price: 139.85 },
  { date: '2023-01-09', price: 141.20 },
  { date: '2023-01-10', price: 143.75 },
  { date: '2023-01-11', price: 145.30 },
  { date: '2023-01-12', price: 146.87 },
  { date: '2023-01-13', price: 147.95 },
  { date: '2023-01-14', price: 148.97 },
];

const mockStockDetails = {
  id: 1,
  symbol: 'AAPL',
  name: 'Apple Inc.',
  current_price: 148.97,
  change_percent: 1.23,
  currency: 'USD',
  market_cap: 2450000000000,
  pe_ratio: 32.5,
  dividend_yield: 0.62,
  high_52w: 152.0,
  low_52w: 89.15,
  volume: 78543210,
  avg_volume: 85642310,
  historical_data: mockChartData
};

const mockStocks = [
  { id: 1, symbol: 'AAPL', name: 'Apple Inc.', current_price: 148.97, change_percent: 1.23, currency: 'USD' },
  { id: 2, symbol: 'MSFT', name: 'Microsoft Corporation', current_price: 234.51, change_percent: -0.45, currency: 'USD' },
  { id: 3, symbol: 'GOOGL', name: 'Alphabet Inc.', current_price: 2055.85, change_percent: 0.75, currency: 'USD' },
  { id: 4, symbol: 'AMZN', name: 'Amazon.com Inc.', current_price: 3304.20, change_percent: -1.05, currency: 'USD' },
  { id: 5, symbol: 'TSLA', name: 'Tesla, Inc.', current_price: 650.75, change_percent: 2.45, currency: 'USD' },
];

const mockTopGainers = [
  { id: 5, symbol: 'TSLA', name: 'Tesla, Inc.', current_price: 650.75, change_percent: 5.45, currency: 'USD' },
  { id: 6, symbol: 'NVDA', name: 'NVIDIA Corporation', current_price: 198.52, change_percent: 4.32, currency: 'USD' },
  { id: 7, symbol: 'AMD', name: 'Advanced Micro Devices, Inc.', current_price: 92.15, change_percent: 3.87, currency: 'USD' },
  { id: 8, symbol: 'PLTR', name: 'Palantir Technologies Inc.', current_price: 24.18, change_percent: 3.45, currency: 'USD' },
  { id: 9, symbol: 'COIN', name: 'Coinbase Global, Inc.', current_price: 248.30, change_percent: 3.21, currency: 'USD' },
];

const mockTopLosers = [
  { id: 10, symbol: 'GME', name: 'GameStop Corp.', current_price: 180.50, change_percent: -7.25, currency: 'USD' },
  { id: 11, symbol: 'AMC', name: 'AMC Entertainment Holdings', current_price: 46.20, change_percent: -5.84, currency: 'USD' },
  { id: 12, symbol: 'BABA', name: 'Alibaba Group Holding Ltd.', current_price: 212.75, change_percent: -4.92, currency: 'USD' },
  { id: 13, symbol: 'NIO', name: 'NIO Inc.', current_price: 38.45, change_percent: -4.15, currency: 'USD' },
  { id: 14, symbol: 'HOOD', name: 'Robinhood Markets, Inc.', current_price: 42.85, change_percent: -3.78, currency: 'USD' },
];

const mockMostActive = [
  { id: 1, symbol: 'AAPL', name: 'Apple Inc.', current_price: 148.97, change_percent: 1.23, currency: 'USD', volume: 78543210 },
  { id: 2, symbol: 'MSFT', name: 'Microsoft Corporation', current_price: 234.51, change_percent: -0.45, currency: 'USD', volume: 65123478 },
  { id: 5, symbol: 'TSLA', name: 'Tesla, Inc.', current_price: 650.75, change_percent: 5.45, currency: 'USD', volume: 57123456 },
  { id: 4, symbol: 'AMZN', name: 'Amazon.com Inc.', current_price: 3304.20, change_percent: -1.05, currency: 'USD', volume: 45678912 },
  { id: 3, symbol: 'GOOGL', name: 'Alphabet Inc.', current_price: 2055.85, change_percent: 0.75, currency: 'USD', volume: 42123456 },
];

const mockMarketIndices = [
  { id: 1, symbol: 'SPX', name: 'S&P 500', current_value: 4204.11, change_percent: 0.58, is_positive: true },
  { id: 2, symbol: 'DJI', name: 'Dow Jones Industrial Average', current_value: 34393.75, change_percent: 0.25, is_positive: true },
  { id: 3, symbol: 'IXIC', name: 'NASDAQ Composite', current_value: 14174.14, change_percent: 0.74, is_positive: true },
  { id: 4, symbol: 'RUT', name: 'Russell 2000', current_value: 2304.40, change_percent: -0.33, is_positive: false },
  { id: 5, symbol: 'VIX', name: 'CBOE Volatility Index', current_value: 16.39, change_percent: -3.42, is_positive: false },
];

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    try {
      // For FastAPI's token endpoint, we need to use x-www-form-urlencoded format
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await api.post('/api/v1/auth/login/access-token', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      if (response.data.access_token) {
        await AsyncStorage.setItem('token', response.data.access_token);
      }

      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      if (USE_MOCK_DATA) {
        // In mock mode, validate against hardcoded credentials
        if (
          (email === MOCK_CREDENTIALS.email || email === MOCK_CREDENTIALS.username) && 
          password === MOCK_CREDENTIALS.password
        ) {
          // Store the email and name for later use
          await AsyncStorage.setItem('userEmail', MOCK_CREDENTIALS.email);
          await AsyncStorage.setItem('userName', MOCK_CREDENTIALS.full_name);
          
          const mockToken = 'mock_token_' + Date.now();
          await AsyncStorage.setItem('token', mockToken);
          return { access_token: mockToken, token_type: 'bearer' };
        } else {
          // Simulate a login error for wrong credentials
          throw new Error('Incorrect username or password');
        }
      }
      throw error;
    }
  },

  forgotPassword: async (email: string) => {
    try {
      const response = await api.post('/api/v1/auth/password-reset/request', { email });
      return response.data;
    } catch (error) {
      console.error('Forgot password error:', error);
      if (USE_MOCK_DATA) {
        // For development, just simulate a successful password reset request
        // In a real app, this would send an email with a reset link
        return { 
          success: true, 
          message: 'If your email exists in our system, you will receive a password reset link.'
        };
      }
      throw error;
    }
  },
  
  resetPassword: async (token: string, newPassword: string) => {
    try {
      const response = await api.post('/api/v1/auth/password-reset/confirm', { 
        token, 
        new_password: newPassword 
      });
      return response.data;
    } catch (error) {
      console.error('Reset password error:', error);
      if (USE_MOCK_DATA) {
        // For development, just simulate a successful password reset
        return { 
          success: true, 
          message: 'Password successfully reset.'
        };
      }
      throw error;
    }
  },

  logout: async () => {
    await AsyncStorage.removeItem('token');
    await AsyncStorage.removeItem('userEmail');
    await AsyncStorage.removeItem('userName');
  },

  register: async (email: string, password: string, fullName: string) => {
    try {
      // For the FastAPI backend, use a proper JSON body for registration
      const response = await api.post('/api/v1/auth/register', null, {
        params: {
          username: email.split('@')[0], // Create a username from email (can be changed later)
          email: email,
          password: password,
          full_name: fullName
        }
      });
      return response.data;
    } catch (error) {
      console.error('Register error:', error);
      if (USE_MOCK_DATA) {
        // Store the new user details
        await AsyncStorage.setItem('userEmail', email);
        await AsyncStorage.setItem('userName', fullName);
        
        // Return mock data for development
        return {
          username: email.split('@')[0],
          email,
          full_name: fullName,
          disabled: false
        };
      }
      throw error;
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await api.get('/api/v1/users/me');
      return response.data;
    } catch (error) {
      console.error('Get current user error:', error);
      if (USE_MOCK_DATA) {
        // Check if we have a token first
        const token = await AsyncStorage.getItem('token');
        if (!token) {
          throw new Error('Not authenticated');
        }
        
        // Get email from storage to simulate logged in user
        const userEmail = await AsyncStorage.getItem('userEmail') || MOCK_CREDENTIALS.email;
        const userName = await AsyncStorage.getItem('userName') || MOCK_CREDENTIALS.full_name;
        
        // Return mock data for development
        return {
          username: userEmail.split('@')[0],
          email: userEmail,
          full_name: userName,
          disabled: false
        };
      }
      throw error;
    }
  },
};

// Stocks API
export const stocksAPI = {
  getStocks: async (skip = 0, limit = 100) => {
    if (USE_MOCK_DATA) {
      return mockStocks;
    }
    const response = await api.get(`/stocks/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getStock: async (symbol: string) => {
    if (USE_MOCK_DATA) {
      return mockStockDetails;
    }
    const response = await api.get(`/stocks/${symbol}`);
    return response.data;
  },

  getStockChart: async (symbol: string, period = '1y', interval = '1d') => {
    if (USE_MOCK_DATA) {
      return mockChartData;
    }
    const response = await api.get(`/stocks/${symbol}/chart?period=${period}&interval=${interval}`);
    return response.data;
  },

  searchStocks: async (query: string, limit = 10) => {
    if (USE_MOCK_DATA) {
      return mockStocks.slice(0, limit);
    }
    const response = await api.get(`/stocks/search?query=${query}&limit=${limit}`);
    return response.data;
  },

  getTopGainers: async (limit = 5) => {
    if (USE_MOCK_DATA) {
      return mockTopGainers;
    }
    const response = await api.get(`/stocks/top-gainers?limit=${limit}`);
    return response.data;
  },

  getTopLosers: async (limit = 5) => {
    if (USE_MOCK_DATA) {
      return mockTopLosers;
    }
    const response = await api.get(`/stocks/top-losers?limit=${limit}`);
    return response.data;
  },

  getMostActive: async (limit = 5) => {
    if (USE_MOCK_DATA) {
      return mockMostActive;
    }
    const response = await api.get(`/stocks/most-active?limit=${limit}`);
    return response.data;
  },
};

// Market Indices API
export const marketIndicesAPI = {
  getIndices: async (skip = 0, limit = 100) => {
    if (USE_MOCK_DATA) {
      return mockMarketIndices;
    }
    const response = await api.get(`/market-indices/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getIndex: async (symbol: string) => {
    const response = await api.get(`/market-indices/${symbol}`);
    return response.data;
  },

  getIndexChart: async (symbol: string, period = '1y', interval = '1d') => {
    const response = await api.get(`/market-indices/${symbol}/chart?period=${period}&interval=${interval}`);
    return response.data;
  },

  getUSIndices: async (limit = 10) => {
    const response = await api.get(`/market-indices/us?limit=${limit}`);
    return response.data;
  },

  getGlobalIndices: async (limit = 10) => {
    const response = await api.get(`/market-indices/global?limit=${limit}`);
    return response.data;
  },

  getIndicesByRegion: async (region: string, limit = 10) => {
    const response = await api.get(`/market-indices/region/${region}?limit=${limit}`);
    return response.data;
  },
};

// News API
export const newsAPI = {
  getNews: async (skip = 0, limit = 10) => {
    const response = await api.get(`/news/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getLatestNews: async (limit = 10) => {
    const response = await api.get(`/news/latest?limit=${limit}`);
    return response.data;
  },

  getFeaturedNews: async (limit = 5) => {
    const response = await api.get(`/news/featured?limit=${limit}`);
    return response.data;
  },

  getNewsByCategory: async (category: string, limit = 10) => {
    const response = await api.get(`/news/category/${category}?limit=${limit}`);
    return response.data;
  },

  getNewsByTicker: async (ticker: string, limit = 10) => {
    const response = await api.get(`/news/ticker/${ticker}?limit=${limit}`);
    return response.data;
  },

  getNewsItem: async (newsId: string) => {
    const response = await api.get(`/news/${newsId}`);
    return response.data;
  },
};

// Portfolio API
export const portfolioAPI = {
  getPortfolios: async (skip = 0, limit = 100) => {
    const response = await api.get(`/portfolio/?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  getPortfolio: async (portfolioId: string) => {
    const response = await api.get(`/portfolio/${portfolioId}`);
    return response.data;
  },

  createPortfolio: async (name: string) => {
    const response = await api.post('/portfolio/', { name });
    return response.data;
  },

  updatePortfolio: async (portfolioId: string, name: string) => {
    const response = await api.put(`/portfolio/${portfolioId}`, { name });
    return response.data;
  },

  deletePortfolio: async (portfolioId: string) => {
    const response = await api.delete(`/portfolio/${portfolioId}`);
    return response.data;
  },

  getPortfolioItems: async (portfolioId: string, skip = 0, limit = 100) => {
    const response = await api.get(`/portfolio/${portfolioId}/items?skip=${skip}&limit=${limit}`);
    return response.data;
  },

  addPortfolioItem: async (portfolioId: string, stockId: string, quantity: number, purchasePrice: number, purchaseDate?: string) => {
    const response = await api.post(`/portfolio/${portfolioId}/items`, {
      stock_id: stockId,
      quantity,
      purchase_price: purchasePrice,
      purchase_date: purchaseDate,
    });
    return response.data;
  },

  updatePortfolioItem: async (portfolioId: string, itemId: string, quantity?: number, purchasePrice?: number, purchaseDate?: string) => {
    const response = await api.put(`/portfolio/${portfolioId}/items/${itemId}`, {
      quantity,
      purchase_price: purchasePrice,
      purchase_date: purchaseDate,
    });
    return response.data;
  },

  deletePortfolioItem: async (portfolioId: string, itemId: string) => {
    const response = await api.delete(`/portfolio/${portfolioId}/items/${itemId}`);
    return response.data;
  },
};

// User API
export const userAPI = {
  getMe: async () => {
    try {
      const response = await api.get('/api/v1/users/me');
      return response.data;
    } catch (error) {
      console.error('Get user error:', error);
      if (USE_MOCK_DATA) {
        // Return mock data for development
        return {
          username: 'johndoe',
          email: 'johndoe@example.com',
          full_name: 'John Doe',
          disabled: false
        };
      }
      throw error;
    }
  },

  updateProfile: async (data: { full_name?: string; email?: string; password?: string }) => {
    try {
      const response = await api.put('/api/v1/users/me', data);
      return response.data;
    } catch (error) {
      console.error('Update profile error:', error);
      if (USE_MOCK_DATA) {
        // Return mock data for development
        return {
          username: 'johndoe',
          email: data.email || 'johndoe@example.com',
          full_name: data.full_name || 'John Doe',
          disabled: false
        };
      }
      throw error;
    }
  },
};

export default {
  auth: authAPI,
  stocks: stocksAPI,
  marketIndices: marketIndicesAPI,
  news: newsAPI,
  portfolio: portfolioAPI,
  user: userAPI,
};
