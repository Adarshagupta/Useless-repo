import React, { useEffect, useRef } from 'react';
import { View, StyleSheet, Animated, Easing, Text } from 'react-native';
import { RefreshCw } from 'lucide-react-native';

interface RefreshAnimationProps {
  visible: boolean;
}

export const RefreshAnimation: React.FC<RefreshAnimationProps> = ({ visible }) => {
  const spinValue = useRef(new Animated.Value(0)).current;
  const scaleValue = useRef(new Animated.Value(0)).current;
  const opacityValue = useRef(new Animated.Value(0)).current;
  const moveValue = useRef(new Animated.Value(0)).current;
  const pulseValue = useRef(new Animated.Value(1)).current;

  useEffect(() => {
    if (visible) {
      // Sequence of animations
      Animated.sequence([
        // Fade in and move up
        Animated.parallel([
          Animated.timing(opacityValue, {
            toValue: 1,
            duration: 300,
            useNativeDriver: true,
          }),
          Animated.timing(moveValue, {
            toValue: 1,
            duration: 400,
            easing: Easing.out(Easing.cubic),
            useNativeDriver: true,
          }),
        ]),
        // Scale up with bounce effect
        Animated.timing(scaleValue, {
          toValue: 1,
          duration: 300,
          useNativeDriver: true,
          easing: Easing.out(Easing.back(1.5)),
        }),
      ]).start();

      // Continuous rotation animation
      Animated.loop(
        Animated.timing(spinValue, {
          toValue: 1,
          duration: 1500,
          easing: Easing.linear,
          useNativeDriver: true,
        })
      ).start();

      // Pulsing animation
      Animated.loop(
        Animated.sequence([
          Animated.timing(pulseValue, {
            toValue: 1.2,
            duration: 800,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: true,
          }),
          Animated.timing(pulseValue, {
            toValue: 1,
            duration: 800,
            easing: Easing.inOut(Easing.ease),
            useNativeDriver: true,
          })
        ])
      ).start();
    } else {
      // Fade out and scale down
      Animated.parallel([
        Animated.timing(opacityValue, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(scaleValue, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
        Animated.timing(moveValue, {
          toValue: 0,
          duration: 300,
          useNativeDriver: true,
        }),
      ]).start();

      // Stop all animations
      spinValue.stopAnimation();
      pulseValue.stopAnimation();
    }
  }, [visible, spinValue, scaleValue, pulseValue]);

  const spin = spinValue.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg'],
  });

  if (!visible) return null;

  // Calculate the movement from top
  const translateY = moveValue.interpolate({
    inputRange: [0, 1],
    outputRange: [-20, 0], // Move from -20 (above) to 0 (normal position)
  });

  return (
    <View style={styles.container}>
      <Animated.View
        style={[
          styles.iconContainer,
          {
            opacity: opacityValue,
            transform: [
              { translateY },
              { rotate: spin },
              { scale: Animated.multiply(scaleValue, pulseValue) }
            ],
          },
        ]}
      >
        <RefreshCw size={32} color="#007AFF" />
      </Animated.View>
      <Animated.Text
        style={[
          styles.refreshText,
          {
            opacity: opacityValue,
            transform: [{ translateY }]
          }
        ]}
      >
        Refreshing...
      </Animated.Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
  },
  iconContainer: {
    width: 70,
    height: 70,
    borderRadius: 35,
    backgroundColor: 'rgba(28, 28, 30, 0.9)',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.4,
    shadowRadius: 6,
    elevation: 8,
    borderWidth: 2,
    borderColor: 'rgba(0, 122, 255, 0.5)',
  },
  refreshText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
    backgroundColor: 'rgba(28, 28, 30, 0.9)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
    overflow: 'hidden',
    letterSpacing: 0.5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
    elevation: 4,
  },
});
