import { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Image, ActivityIndicator } from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { ArrowLeft, Filter, Star } from 'lucide-react-native';

// Sample category data
const categoryData = {
  pizza: {
    name: 'Pizza',
    description: 'Delicious pizzas with a variety of toppings',
    products: [
      {
        id: 'pizza-1',
        name: 'Margherita Pizza',
        price: 12.99,
        rating: 4.8,
        image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&h=500&fit=crop',
        description: 'Classic pizza with tomato sauce, mozzarella, and basil',
      },
      {
        id: 'pizza-2',
        name: 'Pepperoni Pizza',
        price: 14.99,
        rating: 4.6,
        image: 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=500&h=500&fit=crop',
        description: 'Pizza topped with pepperoni slices and cheese',
      },
      {
        id: 'pizza-3',
        name: 'Vegetarian Pizza',
        price: 13.99,
        rating: 4.5,
        image: 'https://images.unsplash.com/photo-1604917877934-07d8d248d396?w=500&h=500&fit=crop',
        description: 'Pizza loaded with fresh vegetables and cheese',
      },
      {
        id: 'pizza-4',
        name: 'Hawaiian Pizza',
        price: 15.99,
        rating: 4.3,
        image: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=500&h=500&fit=crop',
        description: 'Pizza with ham, pineapple, and cheese',
      },
    ],
  },
  burger: {
    name: 'Burgers',
    description: 'Juicy burgers with premium ingredients',
    products: [
      {
        id: 'burger-1',
        name: 'Classic Cheeseburger',
        price: 9.99,
        rating: 4.7,
        image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&h=500&fit=crop',
        description: 'Beef patty with cheese, lettuce, tomato, and special sauce',
      },
      {
        id: 'burger-2',
        name: 'Bacon Burger',
        price: 11.99,
        rating: 4.8,
        image: 'https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500&h=500&fit=crop',
        description: 'Beef patty with crispy bacon, cheese, and BBQ sauce',
      },
      {
        id: 'burger-3',
        name: 'Veggie Burger',
        price: 10.99,
        rating: 4.5,
        image: 'https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&h=500&fit=crop',
        description: 'Plant-based patty with fresh vegetables and vegan mayo',
      },
    ],
  },
  pasta: {
    name: 'Pasta',
    description: 'Authentic Italian pasta dishes',
    products: [
      {
        id: 'pasta-1',
        name: 'Spaghetti Carbonara',
        price: 13.99,
        rating: 4.6,
        image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=500&h=500&fit=crop',
        description: 'Spaghetti with creamy egg sauce, pancetta, and parmesan',
      },
      {
        id: 'pasta-2',
        name: 'Fettuccine Alfredo',
        price: 14.99,
        rating: 4.7,
        image: 'https://images.unsplash.com/photo-1645112411341-6c4fd023882c?w=500&h=500&fit=crop',
        description: 'Fettuccine pasta in a rich and creamy parmesan sauce',
      },
      {
        id: 'pasta-3',
        name: 'Penne Arrabbiata',
        price: 12.99,
        rating: 4.5,
        image: 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=500&h=500&fit=crop',
        description: 'Penne pasta with spicy tomato sauce and garlic',
      },
    ],
  },
  sushi: {
    name: 'Sushi',
    description: 'Fresh and delicious Japanese sushi',
    products: [
      {
        id: 'sushi-1',
        name: 'California Roll',
        price: 8.99,
        rating: 4.5,
        image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&h=500&fit=crop',
        description: 'Sushi roll with crab, avocado, and cucumber',
      },
      {
        id: 'sushi-2',
        name: 'Salmon Nigiri',
        price: 10.99,
        rating: 4.8,
        image: 'https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=500&h=500&fit=crop',
        description: 'Fresh salmon slices on top of seasoned rice',
      },
      {
        id: 'sushi-3',
        name: 'Dragon Roll',
        price: 14.99,
        rating: 4.7,
        image: 'https://images.unsplash.com/photo-1617196034183-421b4917c92d?w=500&h=500&fit=crop',
        description: 'Sushi roll with eel, avocado, and special sauce',
      },
    ],
  },
  dessert: {
    name: 'Desserts',
    description: 'Sweet treats to satisfy your cravings',
    products: [
      {
        id: 'dessert-1',
        name: 'Chocolate Cake',
        price: 6.99,
        rating: 4.9,
        image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&h=500&fit=crop',
        description: 'Rich chocolate cake with chocolate ganache',
      },
      {
        id: 'dessert-2',
        name: 'Cheesecake',
        price: 7.99,
        rating: 4.7,
        image: 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?w=500&h=500&fit=crop',
        description: 'Creamy cheesecake with berry compote',
      },
      {
        id: 'dessert-3',
        name: 'Tiramisu',
        price: 8.99,
        rating: 4.8,
        image: 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=500&h=500&fit=crop',
        description: 'Italian dessert with coffee-soaked ladyfingers and mascarpone',
      },
    ],
  },
  drinks: {
    name: 'Drinks',
    description: 'Refreshing beverages for any occasion',
    products: [
      {
        id: 'drink-1',
        name: 'Iced Coffee',
        price: 4.99,
        rating: 4.6,
        image: 'https://images.unsplash.com/photo-1517701604599-bb29b565090c?w=500&h=500&fit=crop',
        description: 'Cold brewed coffee served over ice',
      },
      {
        id: 'drink-2',
        name: 'Fruit Smoothie',
        price: 5.99,
        rating: 4.8,
        image: 'https://images.unsplash.com/photo-1505252585461-04db1eb84625?w=500&h=500&fit=crop',
        description: 'Blend of fresh fruits and yogurt',
      },
      {
        id: 'drink-3',
        name: 'Matcha Latte',
        price: 5.49,
        rating: 4.7,
        image: 'https://images.unsplash.com/photo-1536256263959-770b48d82b0a?w=500&h=500&fit=crop',
        description: 'Green tea latte with steamed milk',
      },
    ],
  },
};

export default function CategoryScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState<any>(null);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      if (typeof id === 'string' && categoryData[id as keyof typeof categoryData]) {
        setCategory(categoryData[id as keyof typeof categoryData]);
      }
      setLoading(false);
    }, 500);
  }, [id]);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#FF2E56" />
      </View>
    );
  }

  if (!category) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Category not found</Text>
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
          title: category.name,
          headerShown: true,
          headerLeft: () => (
            <TouchableOpacity onPress={() => router.back()} style={{ marginRight: 16 }}>
              <ArrowLeft size={24} color="#111827" />
            </TouchableOpacity>
          ),
        }}
      />
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>{category.name}</Text>
          <Text style={styles.subtitle}>{category.description}</Text>
          
          <View style={styles.filterContainer}>
            <TouchableOpacity style={styles.filterButton}>
              <Filter size={16} color="#6B7280" />
              <Text style={styles.filterText}>Filter</Text>
            </TouchableOpacity>
            
            <View style={styles.sortContainer}>
              <TouchableOpacity style={[styles.sortButton, styles.sortButtonActive]}>
                <Text style={styles.sortButtonTextActive}>All</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.sortButton}>
                <Text style={styles.sortButtonText}>Popular</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.sortButton}>
                <Text style={styles.sortButtonText}>Recent</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>

        <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
          <View style={styles.productsContainer}>
            {category.products.map((product: any) => (
              <TouchableOpacity
                key={product.id}
                style={styles.productCard}
                onPress={() => router.push(`/product/${product.id}`)}
              >
                <Image source={{ uri: product.image }} style={styles.productImage} />
                <View style={styles.productInfo}>
                  <Text style={styles.productName}>{product.name}</Text>
                  <View style={styles.productMeta}>
                    <View style={styles.ratingContainer}>
                      <Star size={14} color="#F59E0B" fill="#F59E0B" />
                      <Text style={styles.ratingText}>{product.rating}</Text>
                    </View>
                    <Text style={styles.productPrice}>${product.price.toFixed(2)}</Text>
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </ScrollView>
      </View>
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
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 4,
    marginBottom: 16,
  },
  filterContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 8,
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F3F4F6',
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
  },
  filterText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
  },
  sortContainer: {
    flexDirection: 'row',
  },
  sortButton: {
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginLeft: 8,
    borderRadius: 8,
  },
  sortButtonActive: {
    backgroundColor: '#FF2E56',
  },
  sortButtonText: {
    fontSize: 14,
    color: '#6B7280',
  },
  sortButtonTextActive: {
    fontSize: 14,
    color: '#FFFFFF',
    fontWeight: '500',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  productsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  productCard: {
    width: '48%',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    overflow: 'hidden',
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  productImage: {
    width: '100%',
    height: 150,
    resizeMode: 'cover',
  },
  productInfo: {
    padding: 12,
  },
  productName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 8,
  },
  productMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
  },
  productPrice: {
    fontSize: 16,
    fontWeight: '700',
    color: '#FF2E56',
  },
});
