import { ScrollView, StyleSheet, Text, View, Image, TouchableOpacity, TextInput, Platform, StatusBar, FlatList, Animated, Easing, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { MapPin, Search, Star, Clock, TrendingUp, Percent, Award, ChevronRight, Zap, Gift, Utensils, Flame, Heart, Share2, Bell, Filter } from 'lucide-react-native';
import { colors, typography, spacing, shadows, borderRadius } from '../theme';
import { LinearGradient } from 'expo-linear-gradient';
import { useRef, useEffect, useState, useCallback } from 'react';
import { useNavigation } from '../../context/NavigationContext';

// Utility function to darken or lighten a color
const shadeColor = (color: string, percent: number): string => {
  let R = parseInt(color.substring(1, 3), 16);
  let G = parseInt(color.substring(3, 5), 16);
  let B = parseInt(color.substring(5, 7), 16);

  R = Math.floor(R * (100 + percent) / 100);
  G = Math.floor(G * (100 + percent) / 100);
  B = Math.floor(B * (100 + percent) / 100);

  R = (R < 255) ? R : 255;
  G = (G < 255) ? G : 255;
  B = (B < 255) ? B : 255;

  const RR = ((R.toString(16).length === 1) ? "0" + R.toString(16) : R.toString(16));
  const GG = ((G.toString(16).length === 1) ? "0" + G.toString(16) : G.toString(16));
  const BB = ((B.toString(16).length === 1) ? "0" + B.toString(16) : B.toString(16));

  return "#" + RR + GG + BB;
};

const promos = [
  {
    id: 1,
    title: '50% OFF',
    description: 'On your first order',
    code: 'WELCOME50',
    backgroundColor: '#FEE2E2',
    textColor: '#EF4444',
  },
  {
    id: 2,
    title: 'Free Delivery',
    description: 'Orders above $20',
    code: 'FREEDEL',
    backgroundColor: '#E0E7FF',
    textColor: '#4F46E5',
  },
];

const categories = [
  { id: 'pizza', name: 'Pizza', image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=200&h=200&fit=crop' },
  { id: 'burger', name: 'Burger', image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200&h=200&fit=crop' },
  { id: 'sushi', name: 'Sushi', image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=200&h=200&fit=crop' },
  { id: 'pasta', name: 'Pasta', image: 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=200&h=200&fit=crop' },
  { id: 'dessert', name: 'Desserts', image: 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=200&h=200&fit=crop' },
  { id: 'drinks', name: 'Drinks', image: 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=200&h=200&fit=crop' },
];

const featuredItems = [
  {
    id: 'pizza-1',
    name: 'Margherita Pizza',
    restaurant: 'Pizza Palace',
    price: 12.99,
    image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=300&h=200&fit=crop',
    rating: 4.8,
    deliveryTime: '20-30',
    discount: '20% OFF',
  },
  {
    id: 'burger-1',
    name: 'Classic Cheeseburger',
    restaurant: 'Burger House',
    price: 9.99,
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=300&h=200&fit=crop',
    rating: 4.7,
    deliveryTime: '15-25',
    discount: '15% OFF',
  },
];

const topPicks = [
  {
    id: 'pasta-1',
    name: 'Spaghetti Carbonara',
    restaurant: 'Noodle House',
    price: 13.99,
    image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=200&fit=crop',
    rating: 4.6,
    orders: '1.2k+ orders',
  },
  {
    id: 'sushi-1',
    name: 'California Roll',
    restaurant: 'Sushi Master',
    price: 8.99,
    image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=300&h=200&fit=crop',
    rating: 4.5,
    orders: '800+ orders',
  },
];

const restaurants = [
  {
    id: 1,
    name: 'Pizza Palace',
    image: 'https://images.unsplash.com/photo-1579751626657-72bc17010498?w=500&h=300&fit=crop',
    rating: 4.5,
    deliveryTime: '25-35',
    distance: 1.2,
    cuisine: 'Italian',
    priceRange: '$$',
    featured: true,
    promotion: '20% OFF on selected items',
  },
  {
    id: 2,
    name: 'Burger House',
    image: 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=500&h=300&fit=crop',
    rating: 4.8,
    deliveryTime: '15-25',
    distance: 0.8,
    cuisine: 'American',
    priceRange: '$$',
    featured: true,
    promotion: 'Free delivery on orders above $30',
  },
  {
    id: 3,
    name: 'Sushi Master',
    image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&h=300&fit=crop',
    rating: 4.9,
    deliveryTime: '30-40',
    distance: 1.5,
    cuisine: 'Japanese',
    priceRange: '$$$',
    featured: false,
    promotion: null,
  },
];

const popularRestaurants = [
  {
    id: 4,
    name: 'Taco Fiesta',
    image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500&h=300&fit=crop',
    rating: 4.7,
    deliveryTime: '20-30',
    distance: 1.0,
    cuisine: 'Mexican',
    priceRange: '$$',
    featured: true,
    promotion: 'Buy 1 Get 1 Free',
  },
  {
    id: 5,
    name: 'Green Garden',
    image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=300&fit=crop',
    rating: 4.6,
    deliveryTime: '25-35',
    distance: 1.8,
    cuisine: 'Vegetarian',
    priceRange: '$$',
    featured: false,
    promotion: null,
  },
];

const specialOffers = [
  {
    id: 3,
    title: 'Flash Sale',
    description: 'Limited time offers',
    code: 'FLASH30',
    backgroundColor: '#FEF3C7',
    textColor: '#D97706',
    icon: <Flame size={24} color="#D97706" />,
  },
  {
    id: 4,
    title: 'Refer & Earn',
    description: 'Get $10 for friend',
    code: 'REFER10',
    backgroundColor: '#D1FAE5',
    textColor: '#059669',
    icon: <Gift size={24} color="#059669" />,
  },
];

const trendingItems = [
  {
    id: 'sushi-2',
    name: 'Dragon Roll',
    restaurant: 'Sushi Master',
    price: 14.99,
    image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=300&h=200&fit=crop',
    rating: 4.9,
    orders: '2.5k+ orders',
  },
  {
    id: 'pasta-2',
    name: 'Fettuccine Alfredo',
    restaurant: 'Noodle House',
    price: 11.99,
    image: 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=300&h=200&fit=crop',
    rating: 4.7,
    orders: '1.8k+ orders',
  },
];

const foodBlogs = [
  {
    id: 1,
    title: 'Top 10 Pizza Places in Town',
    author: 'Food Critic',
    image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&h=300&fit=crop',
    readTime: '5 min read',
  },
  {
    id: 2,
    title: 'Healthy Eating Guide',
    author: 'Nutrition Expert',
    image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=300&fit=crop',
    readTime: '8 min read',
  },
];

export default function HomeScreen() {
  const router = useRouter();
  const { navigateWithTransition } = useNavigation();
  const [refreshing, setRefreshing] = useState(false);

  // Pull-to-refresh animation values
  const refreshAnim = useRef(new Animated.Value(0)).current;
  const refreshRotation = refreshAnim.interpolate({
    inputRange: [0, 1],
    outputRange: ['0deg', '360deg']
  });
  const refreshScale = refreshAnim.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [1, 1.2, 1]
  });

  // Notification pulse animation
  const notificationPulse = useRef(new Animated.Value(1)).current;
  const notificationScale = notificationPulse.interpolate({
    inputRange: [0, 0.5, 1],
    outputRange: [1, 1.15, 1]
  });

  // Bounce animation for scrollable lists
  const bounceAnim = useRef(new Animated.Value(0)).current;

  // Animation values
  const scrollY = useRef(new Animated.Value(0)).current;
  const headerFadeAnim = useRef(new Animated.Value(0)).current;
  const headerSlideAnim = useRef(new Animated.Value(-50)).current;
  const searchBarScaleAnim = useRef(new Animated.Value(0.9)).current;

  // Section animations
  const promosAnim = useRef(new Animated.Value(0)).current;
  const categoriesAnim = useRef(new Animated.Value(0)).current;
  const featuredAnim = useRef(new Animated.Value(0)).current;
  const restaurantsAnim = useRef(new Animated.Value(0)).current;
  const trendingAnim = useRef(new Animated.Value(0)).current;
  const blogsAnim = useRef(new Animated.Value(0)).current;
  const whatsNewAnim = useRef(new Animated.Value(0)).current;

  // Animation for card press
  const animatePress = (ref: Animated.Value) => {
    Animated.sequence([
      Animated.timing(ref, {
        toValue: 0.95,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(ref, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();
  };

  // Handle refresh
  const onRefresh = useCallback(() => {
    setRefreshing(true);

    // Start refresh animation
    Animated.loop(
      Animated.timing(refreshAnim, {
        toValue: 1,
        duration: 1000,
        easing: Easing.linear,
        useNativeDriver: true
      })
    ).start();

    // Simulate data fetching
    setTimeout(() => {
      // Reset all animations
      Animated.parallel([
        Animated.timing(headerFadeAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(headerSlideAnim, {
          toValue: -50,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(searchBarScaleAnim, {
          toValue: 0.9,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(promosAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(categoriesAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(featuredAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(restaurantsAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(trendingAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(blogsAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
        Animated.timing(whatsNewAnim, {
          toValue: 0,
          duration: 0,
          useNativeDriver: true,
        }),
      ]).start(() => {
        // Restart all animations
        startAllAnimations();
        refreshAnim.stopAnimation();
        refreshAnim.setValue(0);
        setRefreshing(false);
      });
    }, 2000);
  }, []);

  // Function to start all animations
  const startAllAnimations = () => {
    Animated.parallel([
      // Header animations
      Animated.timing(headerFadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.timing(headerSlideAnim, {
        toValue: 0,
        duration: 800,
        easing: Easing.out(Easing.back(1.5)),
        useNativeDriver: true,
      }),
      Animated.spring(searchBarScaleAnim, {
        toValue: 1,
        friction: 8,
        tension: 40,
        useNativeDriver: true,
      }),
    ]).start();

    // Staggered animations for content sections
    Animated.stagger(150, [
      Animated.timing(promosAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(categoriesAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(featuredAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(restaurantsAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(trendingAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(blogsAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(whatsNewAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
    ]).start();
  };

  useEffect(() => {
    // Start all animations when component mounts
    startAllAnimations();

    // Start notification pulse animation
    Animated.loop(
      Animated.sequence([
        Animated.timing(notificationPulse, {
          toValue: 0,
          duration: 1000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
        Animated.timing(notificationPulse, {
          toValue: 1,
          duration: 1000,
          easing: Easing.inOut(Easing.ease),
          useNativeDriver: true,
        }),
      ])
    ).start();

    // Setup bounce animation for scrollable lists
    const setupBounceEffect = () => {
      Animated.spring(bounceAnim, {
        toValue: 1,
        friction: 5,
        tension: 40,
        useNativeDriver: true,
      }).start();
    };

    setupBounceEffect();
  }, []);

  // Parallax header effect
  const headerTranslateY = scrollY.interpolate({
    inputRange: [0, 100],
    outputRange: [0, -20],
    extrapolate: 'clamp',
  });

  // Opacity effect for header
  const headerOpacity = scrollY.interpolate({
    inputRange: [0, 60, 90],
    outputRange: [1, 0.8, 0.6],
    extrapolate: 'clamp',
  });

  return (
    <SafeAreaView style={styles.container}>
      {/* Custom Pull-to-Refresh Indicator */}
      {refreshing && (
        <View style={styles.refreshContainer}>
          <Animated.View
            style={{
              transform: [
                { rotate: refreshRotation },
                { scale: refreshScale }
              ]
            }}
          >
            <View style={styles.refreshIconContainer}>
              <Zap size={24} color={colors.primary} />
            </View>
          </Animated.View>
          <Text style={styles.refreshText}>Refreshing...</Text>
        </View>
      )}

      <Animated.ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { y: scrollY } } }],
          { useNativeDriver: false }
        )}
        scrollEventThrottle={16}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor="transparent"
            colors={['transparent']}
            progressBackgroundColor="transparent"
            progressViewOffset={20}
          />
        }
      >
        {/* Header */}
        <Animated.View
          style={[
            styles.header,
            {
              opacity: headerFadeAnim,
              transform: [
                { translateY: headerSlideAnim },
                { translateY: headerTranslateY }
              ]
            }
          ]}
        >
          <View style={styles.headerContent}>
            <View style={styles.headerLeft}>
              <View style={styles.locationContainer}>
                <MapPin size={16} color="#6B7280" />
                <Text style={styles.locationText}>123 Main Street</Text>
                <ChevronRight size={16} color="#6B7280" />
              </View>
              <Text style={styles.greeting}>Hello, John! 👋</Text>
            </View>
            <View style={styles.headerRight}>
              <TouchableOpacity
                style={styles.iconButton}
                activeOpacity={0.7}
              >
                <Bell size={22} color="#6B7280" />
                <Animated.View
                  style={[
                    styles.notificationBadge,
                    { transform: [{ scale: notificationScale }] }
                  ]}
                >
                  <Text style={styles.notificationText}>2</Text>
                </Animated.View>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.profileButton}
                activeOpacity={0.7}
                onPress={() => {
                  const tempAnim = new Animated.Value(1);
                  Animated.sequence([
                    Animated.timing(tempAnim, {
                      toValue: 0.8,
                      duration: 100,
                      useNativeDriver: true,
                    }),
                    Animated.timing(tempAnim, {
                      toValue: 1.1,
                      duration: 100,
                      useNativeDriver: true,
                    }),
                    Animated.timing(tempAnim, {
                      toValue: 1,
                      duration: 100,
                      useNativeDriver: true,
                    }),
                  ]).start();
                }}
              >
                <Animated.View
                  style={{
                    borderRadius: 20,
                    overflow: 'hidden',
                    borderWidth: 2,
                    borderColor: colors.primary,
                  }}
                >
                  <Image
                    source={{ uri: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop' }}
                    style={styles.profileImage}
                  />
                </Animated.View>
              </TouchableOpacity>
            </View>
          </View>

          {/* Search Bar */}
          <Animated.View
            style={{
              transform: [{ scale: searchBarScaleAnim }],
              shadowColor: '#000',
              shadowOffset: { width: 0, height: 2 },
              shadowOpacity: searchBarScaleAnim.interpolate({
                inputRange: [0.9, 1],
                outputRange: [0.1, 0.2]
              }),
              shadowRadius: searchBarScaleAnim.interpolate({
                inputRange: [0.9, 1],
                outputRange: [2, 4]
              }),
              elevation: searchBarScaleAnim.interpolate({
                inputRange: [0.9, 1],
                outputRange: [1, 3]
              }),
            }}
          >
            <TouchableOpacity
              style={styles.searchContainer}
              onPress={() => {
                const tempAnim = new Animated.Value(1);
                animatePress(tempAnim);
                navigateWithTransition('/(tabs)/search', {
                  type: 'zoom',
                  duration: 400,
                  color: 'rgba(255, 255, 255, 0.9)'
                });
              }}
              activeOpacity={0.8}
            >
              <Search size={20} color="#6B7280" />
              <TextInput
                style={styles.searchInput}
                placeholder="Search for food or restaurants"
                placeholderTextColor="#6B7280"
                editable={false}
              />
              <Filter size={20} color="#6B7280" />
            </TouchableOpacity>
          </Animated.View>
        </Animated.View>

        {/* Promotions */}
        <Animated.View style={{ opacity: promosAnim, transform: [{ translateY: promosAnim.interpolate({ inputRange: [0, 1], outputRange: [50, 0] }) }] }}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.promosContainer}>
            {promos.map((promo, index) => {
              const delay = index * 100;
              const cardAnim = useRef(new Animated.Value(0)).current;

              useEffect(() => {
                Animated.timing(cardAnim, {
                  toValue: 1,
                  duration: 500,
                  delay,
                  useNativeDriver: true,
                  easing: Easing.out(Easing.back(1.5))
                }).start();
              }, []);

              return (
                <Animated.View
                  key={promo.id}
                  style={[{ opacity: cardAnim, transform: [{ scale: cardAnim }] }]}
                >
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={() => animatePress(cardAnim)}
                  >
                    <LinearGradient
                      colors={[promo.backgroundColor, shadeColor(promo.backgroundColor, -10)]}
                      start={{ x: 0, y: 0 }}
                      end={{ x: 1, y: 1 }}
                      style={[styles.promoCard]}
                    >
                      <View style={styles.promoContent}>
                        <Percent size={24} color={promo.textColor} />
                        <View style={styles.promoText}>
                          <Text style={[styles.promoTitle, { color: promo.textColor }]}>{promo.title}</Text>
                          <Text style={styles.promoDescription}>{promo.description}</Text>
                        </View>
                      </View>
                      <Text style={styles.promoCode}>{promo.code}</Text>
                    </LinearGradient>
                  </TouchableOpacity>
                </Animated.View>
              );
            })}
            {specialOffers.map((offer, index) => {
              const delay = (promos.length + index) * 100;
              const cardAnim = useRef(new Animated.Value(0)).current;

              useEffect(() => {
                Animated.timing(cardAnim, {
                  toValue: 1,
                  duration: 500,
                  delay,
                  useNativeDriver: true,
                  easing: Easing.out(Easing.back(1.5))
                }).start();
              }, []);

              return (
                <Animated.View
                  key={offer.id}
                  style={[{ opacity: cardAnim, transform: [{ scale: cardAnim }] }]}
                >
                  <TouchableOpacity
                    activeOpacity={0.8}
                    onPress={() => animatePress(cardAnim)}
                  >
                    <LinearGradient
                      colors={[offer.backgroundColor, shadeColor(offer.backgroundColor, -10)]}
                      start={{ x: 0, y: 0 }}
                      end={{ x: 1, y: 1 }}
                      style={[styles.promoCard]}
                    >
                      <View style={styles.promoContent}>
                        {offer.icon}
                        <View style={styles.promoText}>
                          <Text style={[styles.promoTitle, { color: offer.textColor }]}>{offer.title}</Text>
                          <Text style={styles.promoDescription}>{offer.description}</Text>
                        </View>
                      </View>
                      <Text style={styles.promoCode}>{offer.code}</Text>
                    </LinearGradient>
                  </TouchableOpacity>
                </Animated.View>
              );
            })}
          </ScrollView>
        </Animated.View>

        {/* Categories */}
        <Animated.View
          style={[styles.section, {
            opacity: categoriesAnim,
            transform: [{ translateY: categoriesAnim.interpolate({
              inputRange: [0, 1],
              outputRange: [50, 0]
            })}]
          }]}
        >
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Categories</Text>
            <TouchableOpacity
              style={styles.seeAllButton}
              onPress={() => {
                const tempAnim = new Animated.Value(1);
                animatePress(tempAnim);
                navigateWithTransition('/(tabs)/categories', {
                  type: 'slide',
                  duration: 350,
                  color: 'rgba(255, 255, 255, 0.9)'
                });
              }}
              activeOpacity={0.7}
            >
              <Text style={styles.seeAllText}>See All</Text>
              <ChevronRight size={16} color="#6B7280" />
            </TouchableOpacity>
          </View>
          <Animated.ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={[styles.categoriesContainer, { transform: [{ translateX: bounceAnim.interpolate({inputRange: [0, 1], outputRange: [20, 0]}) }] }]}
            contentContainerStyle={{ paddingRight: 20 }}
          >
            {categories.map((category, index) => {
              const cardScale = useRef(new Animated.Value(1)).current;

              useEffect(() => {
                const delay = index * 70;
                Animated.spring(cardScale, {
                  toValue: 1,
                  friction: 4,
                  tension: 40,
                  delay,
                  useNativeDriver: true,
                }).start();
              }, []);

              return (
                <Animated.View key={category.id} style={{ transform: [{ scale: cardScale }] }}>
                  <TouchableOpacity
                    style={styles.categoryCard}
                    onPress={() => {
                      animatePress(cardScale);
                      navigateWithTransition(`/category/${category.id}`, {
                        type: 'flip',
                        duration: 500,
                        color: 'rgba(255, 255, 255, 0.9)'
                      });
                    }}
                    activeOpacity={0.7}
                  >
                    <Image
                      source={{ uri: category.image }}
                      style={styles.categoryImage}
                    />
                    <Text style={styles.categoryName}>{category.name}</Text>
                  </TouchableOpacity>
                </Animated.View>
              );
            })}
          </Animated.ScrollView>
        </Animated.View>

        {/* Featured Items */}
        <Animated.View
          style={[styles.section, {
            opacity: featuredAnim,
            transform: [{ translateY: featuredAnim.interpolate({
              inputRange: [0, 1],
              outputRange: [50, 0]
            })}]
          }]}
        >
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Featured Items</Text>
            <TrendingUp size={20} color="#FF2E56" />
          </View>
          <Animated.ScrollView
            horizontal
            showsHorizontalScrollIndicator={false}
            style={[styles.featuredContainer, { transform: [{ translateX: bounceAnim.interpolate({inputRange: [0, 1], outputRange: [-20, 0]}) }] }]}
            contentContainerStyle={{ paddingRight: 20 }}
          >
            {featuredItems.map((item, index) => {
              const itemAnim = useRef(new Animated.Value(0)).current;

              useEffect(() => {
                Animated.timing(itemAnim, {
                  toValue: 1,
                  duration: 600,
                  delay: index * 200,
                  easing: Easing.out(Easing.back(1.7)),
                  useNativeDriver: true,
                }).start();
              }, []);

              return (
                <Animated.View
                  key={item.id}
                  style={{
                    opacity: itemAnim,
                    transform: [
                      { scale: itemAnim },
                      { translateX: itemAnim.interpolate({
                        inputRange: [0, 1],
                        outputRange: [50, 0]
                      })}
                    ]
                  }}
                >
                  <TouchableOpacity
                    style={styles.featuredCard}
                    onPress={() => {
                      animatePress(itemAnim);
                      navigateWithTransition(`/product/${item.id}`, {
                        type: 'fade',
                        duration: 400,
                        color: 'rgba(255, 255, 255, 0.9)'
                      });
                    }}
                    activeOpacity={0.8}
                  >
                    <Image source={{ uri: item.image }} style={styles.featuredImage} />
                    {item.discount && (
                      <View style={styles.discountTag}>
                        <Text style={styles.discountText}>{item.discount}</Text>
                      </View>
                    )}
                    <LinearGradient
                      colors={[colors.white, shadeColor(colors.white, -3)]}
                      style={styles.featuredInfo}
                    >
                      <Text style={styles.featuredName}>{item.name}</Text>
                      <Text style={styles.featuredRestaurant}>{item.restaurant}</Text>
                      <View style={styles.featuredDetails}>
                        <Text style={styles.featuredPrice}>${item.price}</Text>
                        <View style={styles.ratingContainer}>
                          <Star size={14} color="#F59E0B" fill="#F59E0B" />
                          <Text style={styles.rating}>{item.rating}</Text>
                        </View>
                      </View>
                    </LinearGradient>
                  </TouchableOpacity>
                </Animated.View>
              );
            })}
          </Animated.ScrollView>
        </Animated.View>

        {/* Popular Restaurants */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Popular Restaurants</Text>
            <Award size={20} color="#FF2E56" />
          </View>
          <View style={styles.restaurantsContainer}>
            {restaurants.map((restaurant) => (
              <TouchableOpacity
                key={restaurant.id}
                style={styles.restaurantCard}
                onPress={() => router.push({
                  pathname: "/category/[id]",
                  params: { id: restaurant.cuisine.toLowerCase() }
                })}
              >
                <Image source={{ uri: restaurant.image }} style={styles.restaurantImage} />
                <View style={styles.restaurantInfo}>
                  <View style={styles.restaurantHeader}>
                    <Text style={styles.restaurantName}>{restaurant.name}</Text>
                    <View style={styles.restaurantRating}>
                      <Star size={14} color="#F59E0B" fill="#F59E0B" />
                      <Text style={styles.ratingText}>{restaurant.rating}</Text>
                    </View>
                  </View>
                  <View style={styles.restaurantDetails}>
                    <View style={styles.restaurantDetail}>
                      <Clock size={14} color="#6B7280" />
                      <Text style={styles.detailText}>{restaurant.deliveryTime} min</Text>
                    </View>
                    <View style={styles.restaurantDetail}>
                      <MapPin size={14} color="#6B7280" />
                      <Text style={styles.detailText}>{restaurant.distance} km</Text>
                    </View>
                  </View>
                  <View style={styles.restaurantFooter}>
                    <Text style={styles.cuisineText}>{restaurant.cuisine}</Text>
                    <Text style={styles.priceRangeText}>{restaurant.priceRange}</Text>
                  </View>
                  {restaurant.promotion && (
                    <View style={styles.promotionTag}>
                      <Text style={styles.promotionText}>{restaurant.promotion}</Text>
                    </View>
                  )}
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Trending Now */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Trending Now</Text>
            <Flame size={20} color="#FF2E56" />
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.trendingContainer}>
            {topPicks.map((item) => (
              <TouchableOpacity
                key={item.id}
                style={styles.trendingCard}
                onPress={() => router.push(`/product/${item.id}`)}
              >
                <Image source={{ uri: item.image }} style={styles.trendingImage} />
                <View style={styles.trendingInfo}>
                  <Text style={styles.trendingName}>{item.name}</Text>
                  <Text style={styles.trendingRestaurant}>{item.restaurant}</Text>
                  <View style={styles.trendingDetails}>
                    <Text style={styles.trendingPrice}>${item.price}</Text>
                    <View style={styles.ratingContainer}>
                      <Star size={14} color="#F59E0B" fill="#F59E0B" />
                      <Text style={styles.rating}>{item.rating}</Text>
                    </View>
                  </View>
                  <Text style={styles.ordersText}>{item.orders}</Text>
                </View>
              </TouchableOpacity>
            ))}
            {trendingItems.map((item) => (
              <TouchableOpacity
                key={item.id}
                style={styles.trendingCard}
                onPress={() => router.push(`/product/${item.id}`)}
              >
                <Image source={{ uri: item.image }} style={styles.trendingImage} />
                <View style={styles.trendingInfo}>
                  <Text style={styles.trendingName}>{item.name}</Text>
                  <Text style={styles.trendingRestaurant}>{item.restaurant}</Text>
                  <View style={styles.trendingDetails}>
                    <Text style={styles.trendingPrice}>${item.price}</Text>
                    <View style={styles.ratingContainer}>
                      <Star size={14} color="#F59E0B" fill="#F59E0B" />
                      <Text style={styles.rating}>{item.rating}</Text>
                    </View>
                  </View>
                  <Text style={styles.ordersText}>{item.orders}</Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Food Blogs */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Food Blogs</Text>
            <Utensils size={20} color="#FF2E56" />
          </View>
          <View style={styles.blogsContainer}>
            {foodBlogs.map((blog) => (
              <TouchableOpacity
                key={blog.id}
                style={styles.blogCard}
                onPress={() => router.push({
                  pathname: "/product/[id]",
                  params: { id: `blog-${blog.id}` }
                })}
              >
                <Image source={{ uri: blog.image }} style={styles.blogImage} />
                <View style={styles.blogInfo}>
                  <Text style={styles.blogTitle}>{blog.title}</Text>
                  <View style={styles.blogDetails}>
                    <Text style={styles.blogAuthor}>{blog.author}</Text>
                    <Text style={styles.blogReadTime}>{blog.readTime}</Text>
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* What's New */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>What's New</Text>
            <Zap size={20} color="#FF2E56" />
          </View>
          <View style={styles.whatsNewContainer}>
            <TouchableOpacity
              style={styles.whatsNewCard}
              onPress={() => router.push('/product/dessert-1')}
            >
              <Image
                source={{ uri: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500&h=500&fit=crop' }}
                style={styles.whatsNewImage}
              />
              <View style={styles.whatsNewInfo}>
                <Text style={styles.whatsNewTitle}>New Dessert Menu</Text>
                <Text style={styles.whatsNewDescription}>
                  Try our new selection of desserts from top pastry chefs
                </Text>
                <View style={styles.whatsNewButton}>
                  <Text style={styles.whatsNewButtonText}>Explore</Text>
                  <ChevronRight size={16} color="#FFFFFF" />
                </View>
              </View>
            </TouchableOpacity>
          </View>
        </View>
      </Animated.ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  scrollContent: {
    paddingBottom: 80,
  },
  refreshContainer: {
    position: 'absolute',
    top: 60,
    left: 0,
    right: 0,
    zIndex: 10,
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
  },
  refreshIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 10,
    ...shadows.md,
  },
  refreshText: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.primary,
  },
  header: {
    paddingTop: spacing['4'],
    paddingHorizontal: spacing['4'],
    paddingBottom: spacing['2'],
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  headerLeft: {
    flex: 1,
  },
  headerRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  locationContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 4,
  },
  locationText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
    marginRight: 4,
  },
  greeting: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
  },
  iconButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F3F4F6',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 8,
    position: 'relative',
  },
  notificationBadge: {
    position: 'absolute',
    top: 0,
    right: 0,
    backgroundColor: '#EF4444',
    borderRadius: 10,
    width: 20,
    height: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  profileButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    overflow: 'hidden',
  },
  profileImage: {
    width: '100%',
    height: '100%',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F3F4F6',
    borderRadius: 12,
    paddingHorizontal: 12,
    height: 48,
  },
  searchInput: {
    flex: 1,
    marginLeft: 8,
    fontSize: 16,
    color: '#111827',
  },
  promosContainer: {
    paddingHorizontal: 16,
    marginBottom: 24,
  },
  promoCard: {
    width: 160,
    borderRadius: 10,
    padding: 6,
    marginRight: 8,
    ...shadows.md,
  },
  promoContent: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 2,
  },
  promoText: {
    marginLeft: 6,
    flex: 1,
  },
  promoTitle: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 0,
  },
  promoDescription: {
    fontSize: 11,
    color: '#6B7280',
    marginBottom: 0,
  },
  promoCode: {
    fontSize: 11,
    fontWeight: '500',
    color: '#6B7280',
  },
  section: {
    marginBottom: 24,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#111827',
  },
  seeAllButton: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  seeAllText: {
    fontSize: 14,
    color: '#6B7280',
    marginRight: 4,
  },
  categoriesContainer: {
    paddingHorizontal: 16,
  },
  categoryCard: {
    width: 70,
    marginRight: 4,
    alignItems: 'center',
  },
  categoryImage: {
    width: 60,
    height: 60,
    borderRadius: 6,
    marginBottom: 6,
  },
  categoryName: {
    fontSize: 13,
    color: '#374151',
    textAlign: 'center',
  },
  featuredContainer: {
    paddingHorizontal: 16,
  },
  featuredCard: {
    width: 200,
    marginRight: 12,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    ...shadows.md,
  },
  featuredImage: {
    width: '100%',
    height: 120,
  },
  discountTag: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: '#FF2E56',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  discountText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  featuredInfo: {
    padding: 12,
  },
  featuredName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  featuredRestaurant: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 8,
  },
  featuredDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  featuredPrice: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
  },
  ratingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  rating: {
    fontSize: 14,
    fontWeight: '500',
    color: '#111827',
    marginLeft: 4,
  },
  restaurantsContainer: {
    paddingHorizontal: 16,
  },
  restaurantCard: {
    flexDirection: 'row',
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 16,
    ...shadows.md,
  },
  restaurantImage: {
    width: 100,
    height: 100,
  },
  restaurantInfo: {
    flex: 1,
    padding: 12,
  },
  restaurantHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  restaurantName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
  },
  restaurantRating: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  ratingText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#111827',
    marginLeft: 4,
  },
  restaurantDetails: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  restaurantDetail: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 12,
  },
  detailText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 4,
  },
  restaurantFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  cuisineText: {
    fontSize: 14,
    color: '#6B7280',
  },
  priceRangeText: {
    fontSize: 14,
    color: '#6B7280',
  },
  promotionTag: {
    backgroundColor: '#FEE2E2',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  promotionText: {
    fontSize: 12,
    color: '#EF4444',
    fontWeight: '500',
  },
  trendingContainer: {
    paddingHorizontal: 16,
  },
  trendingCard: {
    width: 200,
    marginRight: 12,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    ...shadows.md,
  },
  trendingImage: {
    width: '100%',
    height: 120,
  },
  trendingInfo: {
    padding: 12,
  },
  trendingName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  trendingRestaurant: {
    fontSize: 14,
    color: '#6B7280',
    marginBottom: 8,
  },
  trendingDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  trendingPrice: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
  },
  ordersText: {
    fontSize: 12,
    color: '#6B7280',
  },
  blogsContainer: {
    paddingHorizontal: 16,
  },
  blogCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    marginBottom: 16,
    ...shadows.md,
  },
  blogImage: {
    width: '100%',
    height: 150,
  },
  blogInfo: {
    padding: 16,
  },
  blogTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 8,
  },
  blogDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  blogAuthor: {
    fontSize: 14,
    color: '#6B7280',
  },
  blogReadTime: {
    fontSize: 14,
    color: '#6B7280',
  },
  whatsNewContainer: {
    paddingHorizontal: 16,
  },
  whatsNewCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    overflow: 'hidden',
    ...shadows.md,
  },
  whatsNewImage: {
    width: '100%',
    height: 200,
  },
  whatsNewInfo: {
    padding: 16,
  },
  whatsNewTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 8,
  },
  whatsNewDescription: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 16,
  },
  whatsNewButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FF2E56',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  whatsNewButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFF',
    marginRight: 4,
  },
});