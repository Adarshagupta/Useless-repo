// Market data types
export interface MarketIndex {
  id: string;
  name: string;
  current_value: number;
  change_percent: number;
  change_amount: number;
  is_positive: boolean;
  is_global: boolean;
  region: string;
  chart_data?: ChartDataPoint[];
}

export interface ChartDataPoint {
  date: string;
  value: number;
}

// Stock types
export interface Stock {
  id?: string;
  symbol: string;
  name: string;
  current_price: number;
  change_percent: number;
  change_amount: number;
  is_positive: boolean;
}

export interface StockDetail extends Stock {
  market_cap?: number;
  volume?: number;
  pe_ratio?: number;
  eps?: number;
  high?: number;
  low?: number;
  open?: number;
  previous_close?: number;
  fifty_two_week_high?: number;
  fifty_two_week_low?: number;
  historical_data?: HistoricalDataPoint[];
  news?: NewsItem[];
  technical_indicators?: any;
}

export interface HistoricalDataPoint {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

// News types
export interface NewsItem {
  id: string;
  title: string;
  summary?: string;
  url: string;
  image_url?: string;
  source?: string;
  datetime?: number;
  related_symbols?: string;
}

// Authentication related types
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  token: string | null;
  isLoading: boolean;
}

export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  profile_image_url?: string;
}