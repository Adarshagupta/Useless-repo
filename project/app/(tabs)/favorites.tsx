import { StyleSheet, Text, View, ScrollView, Image, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Heart, Star } from 'lucide-react-native';

const favoriteRestaurants = [
  {
    id: 1,
    name: 'Pizza Palace',
    image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?w=500&h=300&fit=crop',
    rating: 4.5,
    cuisine: 'Italian',
    priceRange: '$$',
    distance: '1.2 km',
    deliveryTime: '25-35 min',
  },
  {
    id: 2,
    name: 'Sushi Master',
    image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&h=300&fit=crop',
    rating: 4.8,
    cuisine: 'Japanese',
    priceRange: '$$$',
    distance: '0.8 km',
    deliveryTime: '30-40 min',
  },
  {
    id: 3,
    name: 'Burger House',
    image: 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=500&h=300&fit=crop',
    rating: 4.6,
    cuisine: 'American',
    priceRange: '$$',
    distance: '1.5 km',
    deliveryTime: '20-30 min',
  },
];

export default function FavoritesScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Favorites</Text>
      </View>

      <ScrollView 
        style={styles.content} 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {favoriteRestaurants.map((restaurant) => (
          <TouchableOpacity key={restaurant.id} style={styles.restaurantCard}>
            <Image source={{ uri: restaurant.image }} style={styles.restaurantImage} />
            <View style={styles.favoriteButton}>
              <Heart size={20} color="#FF2E56" fill="#FF2E56" />
            </View>
            <View style={styles.restaurantInfo}>
              <View style={styles.nameRow}>
                <Text style={styles.restaurantName}>{restaurant.name}</Text>
                <View style={styles.ratingContainer}>
                  <Star size={16} color="#F59E0B" fill="#F59E0B" />
                  <Text style={styles.rating}>{restaurant.rating}</Text>
                </View>
              </View>
              <View style={styles.detailsRow}>
                <Text style={styles.cuisine}>{restaurant.cuisine}</Text>
                <Text style={styles.dot}>•</Text>
                <Text style={styles.priceRange}>{restaurant.priceRange}</Text>
              </View>
              <View style={styles.deliveryInfo}>
                <Text style={styles.deliveryDetail}>{restaurant.distance}</Text>
                <Text style={styles.dot}>•</Text>
                <Text style={styles.deliveryDetail}>{restaurant.deliveryTime}</Text>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  header: {
    padding: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: '#111827',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  scrollContent: {
    paddingBottom: 80,
  },
  restaurantCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  restaurantImage: {
    width: '100%',
    height: 200,
    borderTopLeftRadius: 16,
    borderTopRightRadius: 16,
  },
  favoriteButton: {
    position: 'absolute',
    top: 12,
    right: 12,
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  restaurantInfo: {
    padding: 16,
  },
  nameRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  restaurantName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FEF3C7',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  rating: {
    marginLeft: 4,
    fontSize: 14,
    fontWeight: '600',
    color: '#D97706',
  },
  detailsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  cuisine: {
    fontSize: 14,
    color: '#4B5563',
  },
  dot: {
    marginHorizontal: 8,
    color: '#9CA3AF',
  },
  priceRange: {
    fontSize: 14,
    color: '#4B5563',
  },
  deliveryInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  deliveryDetail: {
    fontSize: 14,
    color: '#6B7280',
  },
});