import { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Image, ActivityIndicator, Dimensions } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { ArrowLeft, Star, Heart, Minus, Plus, Clock, ShoppingBag } from 'lucide-react-native';

// Sample product data
const productData = {
  'pizza-1': {
    id: 'pizza-1',
    name: 'Margherita Pizza',
    price: 12.99,
    rating: 4.8,
    reviews: 124,
    image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&h=500&fit=crop',
    description: 'Classic pizza with tomato sauce, mozzarella, and basil. Made with fresh ingredients and baked in a traditional wood-fired oven for that authentic taste.',
    category: 'Pizza',
    deliveryTime: '25-30 min',
    ingredients: ['Tomato Sauce', 'Mozzarella Cheese', 'Fresh Basil', 'Olive Oil', 'Salt'],
    sizes: ['Small', 'Medium', 'Large'],
    options: ['Thin Crust', 'Regular Crust', 'Thick Crust'],
  },
  'pizza-2': {
    id: 'pizza-2',
    name: 'Pepperoni Pizza',
    price: 14.99,
    rating: 4.6,
    reviews: 98,
    image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500&h=500&fit=crop',
    description: 'Pizza topped with pepperoni slices and cheese. Our pepperoni is carefully selected for the perfect spicy kick, complemented by our signature cheese blend.',
    category: 'Pizza',
    deliveryTime: '25-30 min',
    ingredients: ['Tomato Sauce', 'Mozzarella Cheese', 'Pepperoni', 'Oregano'],
    sizes: ['Small', 'Medium', 'Large'],
    options: ['Thin Crust', 'Regular Crust', 'Thick Crust'],
  },
  'burger-1': {
    id: 'burger-1',
    name: 'Classic Cheeseburger',
    price: 9.99,
    rating: 4.7,
    reviews: 156,
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&h=500&fit=crop',
    description: 'Beef patty with cheese, lettuce, tomato, and special sauce. Made with 100% Angus beef and served on a freshly baked brioche bun.',
    category: 'Burgers',
    deliveryTime: '20-25 min',
    ingredients: ['Beef Patty', 'Cheddar Cheese', 'Lettuce', 'Tomato', 'Onion', 'Special Sauce', 'Brioche Bun'],
    sizes: ['Single', 'Double'],
    options: ['With Fries', 'With Onion Rings', 'No Sides'],
  },
  'pasta-1': {
    id: 'pasta-1',
    name: 'Spaghetti Carbonara',
    price: 13.99,
    rating: 4.6,
    reviews: 87,
    image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=500&h=500&fit=crop',
    description: 'Spaghetti with creamy egg sauce, pancetta, and parmesan. A traditional Italian dish made with authentic ingredients imported from Italy.',
    category: 'Pasta',
    deliveryTime: '25-35 min',
    ingredients: ['Spaghetti', 'Eggs', 'Pancetta', 'Parmesan Cheese', 'Black Pepper', 'Salt'],
    sizes: ['Regular', 'Large'],
    options: ['With Garlic Bread', 'With Salad', 'No Sides'],
  },
  'sushi-1': {
    id: 'sushi-1',
    name: 'California Roll',
    price: 8.99,
    rating: 4.5,
    reviews: 112,
    image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&h=500&fit=crop',
    description: 'Sushi roll with crab, avocado, and cucumber. Made with premium ingredients and expertly rolled by our sushi chefs.',
    category: 'Sushi',
    deliveryTime: '30-40 min',
    ingredients: ['Sushi Rice', 'Nori', 'Crab Meat', 'Avocado', 'Cucumber', 'Sesame Seeds'],
    sizes: ['6 pieces', '8 pieces', '12 pieces'],
    options: ['With Soy Sauce', 'With Wasabi', 'With Ginger'],
  },
  'dessert-1': {
    id: 'dessert-1',
    name: 'Chocolate Cake',
    price: 6.99,
    rating: 4.9,
    reviews: 203,
    image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&h=500&fit=crop',
    description: 'Rich chocolate cake with chocolate ganache. Made with premium Belgian chocolate and baked fresh daily.',
    category: 'Desserts',
    deliveryTime: '20-30 min',
    ingredients: ['Flour', 'Sugar', 'Eggs', 'Belgian Chocolate', 'Butter', 'Vanilla Extract'],
    sizes: ['Slice', 'Small Cake', 'Large Cake'],
    options: ['With Ice Cream', 'With Whipped Cream', 'Plain'],
  },
  'drink-1': {
    id: 'drink-1',
    name: 'Iced Coffee',
    price: 4.99,
    rating: 4.6,
    reviews: 78,
    image: 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500&h=500&fit=crop',
    description: 'Cold brewed coffee served over ice. Made with premium coffee beans and brewed for 12 hours for a smooth, rich flavor.',
    category: 'Drinks',
    deliveryTime: '15-20 min',
    ingredients: ['Cold Brew Coffee', 'Ice', 'Optional: Milk', 'Optional: Sugar'],
    sizes: ['Small', 'Medium', 'Large'],
    options: ['Black', 'With Milk', 'With Sugar', 'With Milk and Sugar'],
  },
};

const { width } = Dimensions.get('window');

export default function ProductScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [product, setProduct] = useState<any>(null);
  const [quantity, setQuantity] = useState(1);
  const [selectedSize, setSelectedSize] = useState('');
  const [selectedOption, setSelectedOption] = useState('');
  const [isFavorite, setIsFavorite] = useState(false);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      if (typeof id === 'string' && productData[id as keyof typeof productData]) {
        const productInfo = productData[id as keyof typeof productData];
        setProduct(productInfo);
        setSelectedSize(productInfo.sizes[0]);
        setSelectedOption(productInfo.options[0]);
      }
      setLoading(false);
    }, 500);
  }, [id]);

  const increaseQuantity = () => {
    setQuantity(prev => prev + 1);
  };

  const decreaseQuantity = () => {
    if (quantity > 1) {
      setQuantity(prev => prev - 1);
    }
  };

  const toggleFavorite = () => {
    setIsFavorite(prev => !prev);
  };

  const addToCart = () => {
    // In a real app, this would add the product to the cart
    // For now, we'll just show an alert
    alert(`Added ${quantity} ${product.name} to cart!`);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF2E56" />
      </View>
    );
  }

  if (!product) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Product not found</Text>
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <Text style={styles.backButtonText}>Go Back</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: '',
          headerShown: true,
          headerTransparent: true,
          headerLeft: () => (
            <TouchableOpacity 
              onPress={() => router.back()} 
              style={styles.headerButton}
            >
              <ArrowLeft size={24} color="#FFFFFF" />
            </TouchableOpacity>
          ),
          headerRight: () => (
            <TouchableOpacity 
              onPress={toggleFavorite} 
              style={styles.headerButton}
            >
              <Heart 
                size={24} 
                color="#FFFFFF" 
                fill={isFavorite ? "#FF2E56" : "transparent"} 
              />
            </TouchableOpacity>
          ),
        }}
      />
      <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
        <Image source={{ uri: product.image }} style={styles.productImage} />
        
        <View style={styles.content}>
          <View style={styles.header}>
            <View>
              <Text style={styles.category}>{product.category}</Text>
              <Text style={styles.title}>{product.name}</Text>
            </View>
            <View style={styles.priceContainer}>
              <Text style={styles.price}>${product.price.toFixed(2)}</Text>
            </View>
          </View>
          
          <View style={styles.ratingContainer}>
            <View style={styles.ratingStars}>
              <Star size={16} color="#F59E0B" fill="#F59E0B" />
              <Text style={styles.ratingText}>{product.rating}</Text>
              <Text style={styles.reviewsText}>({product.reviews} reviews)</Text>
            </View>
            <View style={styles.deliveryTime}>
              <Clock size={16} color="#6B7280" />
              <Text style={styles.deliveryTimeText}>{product.deliveryTime}</Text>
            </View>
          </View>
          
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Description</Text>
            <Text style={styles.description}>{product.description}</Text>
          </View>
          
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Ingredients</Text>
            <View style={styles.ingredientsContainer}>
              {product.ingredients.map((ingredient: string, index: number) => (
                <View key={index} style={styles.ingredientTag}>
                  <Text style={styles.ingredientText}>{ingredient}</Text>
                </View>
              ))}
            </View>
          </View>
          
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Size</Text>
            <View style={styles.optionsContainer}>
              {product.sizes.map((size: string, index: number) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.optionButton,
                    selectedSize === size && styles.optionButtonSelected,
                  ]}
                  onPress={() => setSelectedSize(size)}
                >
                  <Text
                    style={[
                      styles.optionText,
                      selectedSize === size && styles.optionTextSelected,
                    ]}
                  >
                    {size}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
          
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Options</Text>
            <View style={styles.optionsContainer}>
              {product.options.map((option: string, index: number) => (
                <TouchableOpacity
                  key={index}
                  style={[
                    styles.optionButton,
                    selectedOption === option && styles.optionButtonSelected,
                  ]}
                  onPress={() => setSelectedOption(option)}
                >
                  <Text
                    style={[
                      styles.optionText,
                      selectedOption === option && styles.optionTextSelected,
                    ]}
                  >
                    {option}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>
          
          <View style={styles.quantitySection}>
            <Text style={styles.sectionTitle}>Quantity</Text>
            <View style={styles.quantityControls}>
              <TouchableOpacity
                style={[styles.quantityButton, quantity <= 1 && styles.quantityButtonDisabled]}
                onPress={decreaseQuantity}
                disabled={quantity <= 1}
              >
                <Minus size={20} color={quantity <= 1 ? "#D1D5DB" : "#111827"} />
              </TouchableOpacity>
              <Text style={styles.quantityText}>{quantity}</Text>
              <TouchableOpacity style={styles.quantityButton} onPress={increaseQuantity}>
                <Plus size={20} color="#111827" />
              </TouchableOpacity>
            </View>
          </View>
          
          <View style={styles.totalSection}>
            <View>
              <Text style={styles.totalLabel}>Total Price</Text>
              <Text style={styles.totalPrice}>${(product.price * quantity).toFixed(2)}</Text>
            </View>
            <TouchableOpacity style={styles.addToCartButton} onPress={addToCart}>
              <ShoppingBag size={20} color="#FFFFFF" />
              <Text style={styles.addToCartText}>Add to Cart</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F9FAFB',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F9FAFB',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    color: '#111827',
    marginBottom: 20,
  },
  backButton: {
    backgroundColor: '#FF2E56',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
  },
  backButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  headerButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    justifyContent: 'center',
    alignItems: 'center',
    marginHorizontal: 16,
  },
  productImage: {
    width: width,
    height: width * 0.8,
    resizeMode: 'cover',
  },
  content: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 24,
    borderTopRightRadius: 24,
    marginTop: -24,
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: 40,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  category: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#111827',
    maxWidth: width * 0.6,
  },
  priceContainer: {
    backgroundColor: '#F3F4F6',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
  },
  price: {
    fontSize: 18,
    fontWeight: '700',
    color: '#FF2E56',
  },
  ratingContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  ratingStars: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingText: {
    fontSize: 14,
    color: '#111827',
    fontWeight: '600',
    marginLeft: 4,
  },
  reviewsText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
  },
  deliveryTime: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  deliveryTimeText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
  },
  section: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 12,
  },
  description: {
    fontSize: 16,
    lineHeight: 24,
    color: '#4B5563',
  },
  ingredientsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  ingredientTag: {
    backgroundColor: '#F3F4F6',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 16,
    marginRight: 8,
    marginBottom: 8,
  },
  ingredientText: {
    fontSize: 14,
    color: '#4B5563',
  },
  optionsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  optionButton: {
    backgroundColor: '#F3F4F6',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
    marginRight: 12,
    marginBottom: 8,
  },
  optionButtonSelected: {
    backgroundColor: '#FF2E56',
  },
  optionText: {
    fontSize: 14,
    color: '#4B5563',
  },
  optionTextSelected: {
    color: '#FFFFFF',
    fontWeight: '500',
  },
  quantitySection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
  },
  quantityControls: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  quantityButton: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#F3F4F6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  quantityButtonDisabled: {
    backgroundColor: '#F9FAFB',
  },
  quantityText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginHorizontal: 16,
  },
  totalSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 16,
    borderTopWidth: 1,
    borderTopColor: '#E5E7EB',
  },
  totalLabel: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 4,
  },
  totalPrice: {
    fontSize: 24,
    fontWeight: '700',
    color: '#111827',
  },
  addToCartButton: {
    backgroundColor: '#FF2E56',
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 12,
  },
  addToCartText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 8,
  },
});
