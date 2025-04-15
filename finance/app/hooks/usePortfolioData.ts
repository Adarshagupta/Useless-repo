import { useState, useEffect } from 'react';
import { portfolioAPI } from '../api';
import { useAuth } from '../context/AuthContext';

// Define the shape of portfolio data
interface PortfolioData {
  portfolios: any[];
  selectedPortfolio: any | null;
  portfolioItems: any[];
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
  selectPortfolio: (portfolioId: string) => Promise<void>;
  createPortfolio: (name: string) => Promise<any>;
  updatePortfolio: (portfolioId: string, name: string) => Promise<any>;
  deletePortfolio: (portfolioId: string) => Promise<void>;
  addPortfolioItem: (stockId: string, quantity: number, purchasePrice: number, purchaseDate?: string) => Promise<any>;
  updatePortfolioItem: (itemId: string, quantity?: number, purchasePrice?: number, purchaseDate?: string) => Promise<any>;
  deletePortfolioItem: (itemId: string) => Promise<void>;
}

export const usePortfolioData = (): PortfolioData => {
  const { isSignedIn } = useAuth();
  const [portfolios, setPortfolios] = useState<any[]>([]);
  const [selectedPortfolio, setSelectedPortfolio] = useState<any | null>(null);
  const [portfolioItems, setPortfolioItems] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchPortfolios = async () => {
    if (!isSignedIn) return;
    
    try {
      setIsLoading(true);
      setError(null);

      // Fetch portfolios
      const data = await portfolioAPI.getPortfolios();
      setPortfolios(data);

      // If we have portfolios and no selected portfolio, select the first one
      if (data.length > 0 && !selectedPortfolio) {
        await selectPortfolio(data[0].id);
      }
    } catch (err) {
      console.error('Error fetching portfolios:', err);
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  };

  const selectPortfolio = async (portfolioId: string) => {
    try {
      setIsLoading(true);
      setError(null);

      // Fetch portfolio details
      const portfolio = await portfolioAPI.getPortfolio(portfolioId);
      setSelectedPortfolio(portfolio);

      // Fetch portfolio items
      const items = await portfolioAPI.getPortfolioItems(portfolioId);
      setPortfolioItems(items);
    } catch (err) {
      console.error(`Error selecting portfolio ${portfolioId}:`, err);
      setError(err as Error);
    } finally {
      setIsLoading(false);
    }
  };

  const createPortfolio = async (name: string) => {
    try {
      setIsLoading(true);
      setError(null);

      // Create portfolio
      const portfolio = await portfolioAPI.createPortfolio(name);
      
      // Refresh portfolios
      await fetchPortfolios();
      
      return portfolio;
    } catch (err) {
      console.error('Error creating portfolio:', err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const updatePortfolio = async (portfolioId: string, name: string) => {
    try {
      setIsLoading(true);
      setError(null);

      // Update portfolio
      const portfolio = await portfolioAPI.updatePortfolio(portfolioId, name);
      
      // Refresh portfolios
      await fetchPortfolios();
      
      // If this is the selected portfolio, update it
      if (selectedPortfolio && selectedPortfolio.id === portfolioId) {
        setSelectedPortfolio(portfolio);
      }
      
      return portfolio;
    } catch (err) {
      console.error(`Error updating portfolio ${portfolioId}:`, err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const deletePortfolio = async (portfolioId: string) => {
    try {
      setIsLoading(true);
      setError(null);

      // Delete portfolio
      await portfolioAPI.deletePortfolio(portfolioId);
      
      // Refresh portfolios
      await fetchPortfolios();
      
      // If this was the selected portfolio, clear it
      if (selectedPortfolio && selectedPortfolio.id === portfolioId) {
        setSelectedPortfolio(null);
        setPortfolioItems([]);
      }
    } catch (err) {
      console.error(`Error deleting portfolio ${portfolioId}:`, err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const addPortfolioItem = async (stockId: string, quantity: number, purchasePrice: number, purchaseDate?: string) => {
    if (!selectedPortfolio) {
      throw new Error('No portfolio selected');
    }
    
    try {
      setIsLoading(true);
      setError(null);

      // Add portfolio item
      const item = await portfolioAPI.addPortfolioItem(
        selectedPortfolio.id,
        stockId,
        quantity,
        purchasePrice,
        purchaseDate
      );
      
      // Refresh portfolio items
      await selectPortfolio(selectedPortfolio.id);
      
      return item;
    } catch (err) {
      console.error('Error adding portfolio item:', err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const updatePortfolioItem = async (itemId: string, quantity?: number, purchasePrice?: number, purchaseDate?: string) => {
    if (!selectedPortfolio) {
      throw new Error('No portfolio selected');
    }
    
    try {
      setIsLoading(true);
      setError(null);

      // Update portfolio item
      const item = await portfolioAPI.updatePortfolioItem(
        selectedPortfolio.id,
        itemId,
        quantity,
        purchasePrice,
        purchaseDate
      );
      
      // Refresh portfolio items
      await selectPortfolio(selectedPortfolio.id);
      
      return item;
    } catch (err) {
      console.error(`Error updating portfolio item ${itemId}:`, err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  const deletePortfolioItem = async (itemId: string) => {
    if (!selectedPortfolio) {
      throw new Error('No portfolio selected');
    }
    
    try {
      setIsLoading(true);
      setError(null);

      // Delete portfolio item
      await portfolioAPI.deletePortfolioItem(selectedPortfolio.id, itemId);
      
      // Refresh portfolio items
      await selectPortfolio(selectedPortfolio.id);
    } catch (err) {
      console.error(`Error deleting portfolio item ${itemId}:`, err);
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  };

  // Fetch data on mount and when auth state changes
  useEffect(() => {
    if (isSignedIn) {
      fetchPortfolios();
    } else {
      setPortfolios([]);
      setSelectedPortfolio(null);
      setPortfolioItems([]);
    }
  }, [isSignedIn]);

  return {
    portfolios,
    selectedPortfolio,
    portfolioItems,
    isLoading,
    error,
    refetch: fetchPortfolios,
    selectPortfolio,
    createPortfolio,
    updatePortfolio,
    deletePortfolio,
    addPortfolioItem,
    updatePortfolioItem,
    deletePortfolioItem,
  };
};

export default usePortfolioData;
