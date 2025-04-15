import { useState, useEffect } from 'react';
import { newsAPI } from '../api';

// Define the shape of news data
interface NewsData {
  latestNews: any[];
  featuredNews: any[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
  fetchNewsByCategory: (category: string) => Promise<any[]>;
  fetchNewsByTicker: (ticker: string) => Promise<any[]>;
}

export const useNewsData = (): NewsData => {
  const [latestNews, setLatestNews] = useState<any[]>([]);
  const [featuredNews, setFeaturedNews] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchNewsData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Fetch latest news
      const latest = await newsAPI.getLatestNews();
      setLatestNews(latest);

      // Fetch featured news
      const featured = await newsAPI.getFeaturedNews();
      setFeaturedNews(featured);
    } catch (err) {
      console.error('Error fetching news data:', err);
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchNewsByCategory = async (category: string): Promise<any[]> => {
    try {
      const news = await newsAPI.getNewsByCategory(category);
      return news;
    } catch (err) {
      console.error(`Error fetching news for category ${category}:`, err);
      setError(err as Error);
      return [];
    }
  };

  const fetchNewsByTicker = async (ticker: string): Promise<any[]> => {
    try {
      const news = await newsAPI.getNewsByTicker(ticker);
      return news;
    } catch (err) {
      console.error(`Error fetching news for ticker ${ticker}:`, err);
      setError(err as Error);
      return [];
    }
  };

  // Fetch data on mount
  useEffect(() => {
    fetchNewsData();
  }, []);

  return {
    latestNews,
    featuredNews,
    isLoading,
    error,
    refetch: fetchNewsData,
    fetchNewsByCategory,
    fetchNewsByTicker,
  };
};

export default useNewsData;
