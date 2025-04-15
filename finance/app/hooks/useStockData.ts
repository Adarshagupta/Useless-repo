import { useState } from 'react';
import { stocksAPI } from '../api';

// Define the shape of stock data
interface StockData {
  searchStocks: (query: string) => Promise<any[]>;
  getStockDetails: (symbol: string) => Promise<any>;
  getStockChart: (symbol: string, period?: string, interval?: string) => Promise<any>;
  isLoading: boolean;
  error: Error | null;
}

export const useStockData = (): StockData => {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  const searchStocks = async (query: string): Promise<any[]> => {
    try {
      setIsLoading(true);
      setError(null);

      const results = await stocksAPI.searchStocks(query);
      return results;
    } catch (err) {
      console.error(`Error searching stocks for "${query}":`, err);
      setError(err as Error);
      return [];
    } finally {
      setIsLoading(false);
    }
  };

  const getStockDetails = async (symbol: string): Promise<any> => {
    try {
      setIsLoading(true);
      setError(null);

      const stock = await stocksAPI.getStock(symbol);
      return stock;
    } catch (err) {
      console.error(`Error fetching stock details for ${symbol}:`, err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const getStockChart = async (symbol: string, period = '1y', interval = '1d'): Promise<any> => {
    try {
      setIsLoading(true);
      setError(null);

      const chartData = await stocksAPI.getStockChart(symbol, period, interval);
      return chartData;
    } catch (err) {
      console.error(`Error fetching chart data for ${symbol}:`, err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  return {
    searchStocks,
    getStockDetails,
    getStockChart,
    isLoading,
    error,
  };
};

export default useStockData;
