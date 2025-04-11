import React, { createContext, useState, useContext, useCallback } from 'react';
import { useRouter } from 'expo-router';
import NavigationTransition from '../components/NavigationTransition';

interface NavigationContextType {
  navigateWithTransition: (
    route: string,
    options?: {
      type?: 'fade' | 'slide' | 'zoom' | 'flip';
      duration?: number;
      color?: string;
    }
  ) => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (!context) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
};

export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [transitionVisible, setTransitionVisible] = useState(false);
  const [transitionType, setTransitionType] = useState<'fade' | 'slide' | 'zoom' | 'flip'>('fade');
  const [transitionDuration, setTransitionDuration] = useState(300);
  const [transitionColor, setTransitionColor] = useState('#ffffff');
  const [pendingRoute, setPendingRoute] = useState<string | null>(null);
  
  const router = useRouter();

  const navigateWithTransition = useCallback(
    (
      route: string,
      options?: {
        type?: 'fade' | 'slide' | 'zoom' | 'flip';
        duration?: number;
        color?: string;
      }
    ) => {
      // Set transition options
      setTransitionType(options?.type || 'fade');
      setTransitionDuration(options?.duration || 300);
      setTransitionColor(options?.color || '#ffffff');
      
      // Store the route we want to navigate to
      setPendingRoute(route);
      
      // Show transition
      setTransitionVisible(true);
    },
    []
  );

  const handleTransitionComplete = useCallback(() => {
    if (pendingRoute) {
      // Navigate to the pending route
      router.push(pendingRoute);
      
      // Reset transition state
      setTimeout(() => {
        setTransitionVisible(false);
        setPendingRoute(null);
      }, 50);
    }
  }, [pendingRoute, router]);

  return (
    <NavigationContext.Provider value={{ navigateWithTransition }}>
      {children}
      <NavigationTransition
        isVisible={transitionVisible}
        onAnimationComplete={handleTransitionComplete}
        type={transitionType}
        duration={transitionDuration}
        color={transitionColor}
      />
    </NavigationContext.Provider>
  );
};
