import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import { Heart, Star, Plus } from 'lucide-react-native';
import { colors, typography, spacing, shadows, borderRadius } from '../theme';

interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  rating: number;
  image: string;
  restaurant?: string;
  discount?: string;
  isNew?: boolean;
  isFavorite?: boolean;
  onFavoritePress?: () => void;
  style?: any;
}

const { width } = Dimensions.get('window');
const CARD_WIDTH = (width - spacing['4'] * 2 - spacing['3']) / 2;

const ProductCard = ({
  id,
  name,
  price,
  rating,
  image,
  restaurant,
  discount,
  isNew = false,
  isFavorite = false,
  onFavoritePress,
  style,
}: ProductCardProps) => {
  const router = useRouter();

  const handlePress = () => {
    router.push(`/product/${id}`);
  };

  return (
    <TouchableOpacity
      style={[styles.container, style]}
      onPress={handlePress}
      activeOpacity={0.9}
    >
      <View style={styles.imageContainer}>
        <Image source={{ uri: image }} style={styles.image} />
        
        {discount && (
          <View style={styles.discountBadge}>
            <Text style={styles.discountText}>{discount}</Text>
          </View>
        )}
        
        {isNew && (
          <View style={styles.newBadge}>
            <Text style={styles.newText}>NEW</Text>
          </View>
        )}
        
        <TouchableOpacity 
          style={styles.favoriteButton}
          onPress={onFavoritePress}
          hitSlop={{ top: 10, right: 10, bottom: 10, left: 10 }}
        >
          <Heart 
            size={18} 
            color={colors.white} 
            fill={isFavorite ? colors.primary : 'transparent'} 
          />
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.addButton}>
          <Plus size={16} color={colors.white} />
        </TouchableOpacity>
      </View>
      
      <View style={styles.content}>
        <Text style={styles.name} numberOfLines={1}>{name}</Text>
        
        {restaurant && (
          <Text style={styles.restaurant} numberOfLines={1}>{restaurant}</Text>
        )}
        
        <View style={styles.footer}>
          <View style={styles.ratingContainer}>
            <Star size={12} color={colors.warning} fill={colors.warning} />
            <Text style={styles.rating}>{rating}</Text>
          </View>
          
          <Text style={styles.price}>${price.toFixed(2)}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    width: CARD_WIDTH,
    backgroundColor: colors.white,
    borderRadius: borderRadius.lg,
    overflow: 'hidden',
    ...shadows.md,
    marginBottom: spacing['4'],
  },
  imageContainer: {
    position: 'relative',
    height: CARD_WIDTH,
  },
  image: {
    width: '100%',
    height: '100%',
    borderTopLeftRadius: borderRadius.lg,
    borderTopRightRadius: borderRadius.lg,
  },
  discountBadge: {
    position: 'absolute',
    top: spacing['2'],
    left: spacing['2'],
    backgroundColor: colors.primary,
    paddingHorizontal: spacing['2'],
    paddingVertical: spacing['1'],
    borderRadius: borderRadius.md,
  },
  discountText: {
    color: colors.white,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
  },
  newBadge: {
    position: 'absolute',
    top: spacing['2'],
    left: spacing['2'],
    backgroundColor: colors.secondary,
    paddingHorizontal: spacing['2'],
    paddingVertical: spacing['1'],
    borderRadius: borderRadius.md,
  },
  newText: {
    color: colors.white,
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
  },
  favoriteButton: {
    position: 'absolute',
    top: spacing['2'],
    right: spacing['2'],
    backgroundColor: 'rgba(0,0,0,0.3)',
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  addButton: {
    position: 'absolute',
    bottom: spacing['2'],
    right: spacing['2'],
    backgroundColor: colors.primary,
    width: 28,
    height: 28,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
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
  restaurant: {
    fontSize: typography.fontSize.sm,
    color: colors.gray,
    marginBottom: spacing['2'],
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rating: {
    fontSize: typography.fontSize.sm,
    color: colors.gray,
    marginLeft: spacing['1'],
  },
  price: {
    fontSize: typography.fontSize.base,
    fontWeight: typography.fontWeight.bold,
    color: colors.primary,
  },
});

export default ProductCard;
