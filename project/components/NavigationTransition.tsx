import React, { useEffect, useRef } from 'react';
import { Animated, StyleSheet, Dimensions, View } from 'react-native';

const { width, height } = Dimensions.get('window');

interface NavigationTransitionProps {
  isVisible: boolean;
  onAnimationComplete?: () => void;
  type?: 'fade' | 'slide' | 'zoom' | 'flip';
  duration?: number;
  color?: string;
}

const NavigationTransition: React.FC<NavigationTransitionProps> = ({
  isVisible,
  onAnimationComplete,
  type = 'fade',
  duration = 300,
  color = '#ffffff',
}) => {
  const animValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    if (isVisible) {
      // Start animation
      Animated.timing(animValue, {
        toValue: 1,
        duration,
        useNativeDriver: true,
      }).start(() => {
        // Animation completed
        if (onAnimationComplete) {
          onAnimationComplete();
        }
      });
    } else {
      // Reset animation
      animValue.setValue(0);
    }
  }, [isVisible, duration, animValue, onAnimationComplete]);

  // Different animation styles based on type
  const getAnimatedStyle = () => {
    switch (type) {
      case 'fade':
        return {
          opacity: animValue,
        };
      case 'slide':
        return {
          opacity: animValue,
          transform: [
            {
              translateX: animValue.interpolate({
                inputRange: [0, 1],
                outputRange: [width, 0],
              }),
            },
          ],
        };
      case 'zoom':
        return {
          opacity: animValue,
          transform: [
            {
              scale: animValue.interpolate({
                inputRange: [0, 1],
                outputRange: [0.8, 1],
              }),
            },
          ],
        };
      case 'flip':
        return {
          opacity: animValue,
          transform: [
            {
              rotateY: animValue.interpolate({
                inputRange: [0, 1],
                outputRange: ['90deg', '0deg'],
              }),
            },
          ],
        };
      default:
        return {
          opacity: animValue,
        };
    }
  };

  if (!isVisible && animValue._value === 0) {
    return null;
  }

  return (
    <Animated.View
      style={[
        styles.container,
        { backgroundColor: color },
        getAnimatedStyle(),
      ]}
    />
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    width,
    height,
    zIndex: 999,
  },
});

export default NavigationTransition;
