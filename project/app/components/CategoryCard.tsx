import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import { colors, typography, spacing, shadows, borderRadius } from '../theme';

interface CategoryCardProps {
  id: string;
  name: string;
  image: string;
  count?: number;
  style?: any;
  size?: 'small' | 'medium' | 'large';
}

const CategoryCard = ({
  id,
  name,
  image,
  count,
  style,
  size = 'medium',
}: CategoryCardProps) => {
  const router = useRouter();

  const handlePress = () => {
    router.push(`/category/${id}`);
  };

  const getCardSize = () => {
    switch (size) {
      case 'small':
        return {
          container: { width: 100, height: 100 },
          image: { height: 70 },
        };
      case 'large':
        return {
          container: { width: '100%', height: 150 },
          image: { height: 100 },
        };
      case 'medium':
      default:
        return {
          container: { width: 140, height: 140 },
          image: { height: 90 },
        };
    }
  };

  const sizeStyles = getCardSize();

  return (
    <TouchableOpacity
      style={[styles.container, sizeStyles.container, style]}
      onPress={handlePress}
      activeOpacity={0.9}
    >
      <Image 
        source={{ uri: image }} 
        style={[styles.image, sizeStyles.image]} 
      />
      
      <View style={styles.content}>
        <Text style={styles.name} numberOfLines={1}>{name}</Text>
        {count !== undefined && (
          <Text style={styles.count}>{count} items</Text>
        )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: colors.white,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    ...shadows.md,
    marginRight: spacing['3'],
    marginBottom: spacing['3'],
  },
  image: {
    width: '100%',
    resizeMode: 'cover',
  },
  content: {
    padding: spacing['3'],
  },
  name: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.semibold,
    color: colors.dark,
    marginBottom: spacing['1'],
  },
  count: {
    fontSize: typography.fontSize.sm,
    color: colors.gray,
  },
});

export default CategoryCard;
