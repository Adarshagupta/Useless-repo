import { useState, useEffect } from 'react';
import { MarketIndex } from '../types';
import api from '../api';
import { useAuth } from '../context/AuthContext';

export function useMarketData() {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<MarketIndex[]>([]);
  const { isAuthenticated, token } = useAuth();

  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      if (!isAuthenticated || !token) {
        return;
      }

      try {
        setLoading(true);
        const response = await api.marketIndices.getMarketIndices();
        if (isMounted) {
          setData(response.data || []);
          setError(null);
        }
      } catch (err) {
        console.error('Error fetching market data:', err);
        if (isMounted) {
          setError('Failed to load market data. Please try again later.');
          // Fallback to mock data in case of error
          setData([
            {
              id: "^DJI",
              name: "Dow Jones Industrial Average",
              current_value: 38627.96,
              change_percent: 0.35,
              is_positive: true,
              change_amount: 134.25,
              is_global: false,
              region: "US",
              chart_data: []
            },
            {
              id: "^GSPC",
              name: "S&P 500",
              current_value: 5069.53,
              change_percent: 0.38,
              is_positive: true,
              change_amount: 40.81,
              is_global: false,
              region: "US",
              chart_data: []
            },
            {
              id: "^IXIC",
              name: "NASDAQ Composite",
              current_value: 15966.84,
              change_percent: 0.35,
              is_positive: true,
              change_amount: 183.05,
              is_global: false,
              region: "US",
              chart_data: []
            }
          ]);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    fetchData();

    // Set up auto-refresh every 60 seconds
    const intervalId = setInterval(() => {
      fetchData();
    }, 60000);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, [isAuthenticated, token]);

  return { data, loading, error, refetch: () => setLoading(true) };
}

export default useMarketData; 