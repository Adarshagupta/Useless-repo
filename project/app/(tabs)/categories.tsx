import { StyleSheet, Text, View, ScrollView, StatusBar } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Grid } from 'lucide-react-native';
import CategoryCard from '../components/CategoryCard';
import SectionHeader from '../components/SectionHeader';
import { colors, typography, spacing, shadows, borderRadius } from '../theme';

// Sample category data
const categories = [
  {
    id: 'pizza',
    name: 'Pizza',
    image: 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&h=500&fit=crop',
    description: 'Delicious pizzas with a variety of toppings',
    count: 12,
  },
  {
    id: 'burger',
    name: 'Burgers',
    image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&h=500&fit=crop',
    description: 'Juicy burgers with premium ingredients',
    count: 8,
  },
  {
    id: 'pasta',
    name: 'Pasta',
    image: 'https://images.unsplash.com/photo-1563379926898-05f4575a45d8?w=500&h=500&fit=crop',
    description: 'Authentic Italian pasta dishes',
    count: 10,
  },
  {
    id: 'sushi',
    name: 'Sushi',
    image: 'https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500&h=500&fit=crop',
    description: 'Fresh and delicious Japanese sushi',
    count: 15,
  },
  {
    id: 'dessert',
    name: 'Desserts',
    image: 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=500&h=500&fit=crop',
    description: 'Sweet treats to satisfy your cravings',
    count: 9,
  },
  {
    id: 'drinks',
    name: 'Drinks',
    image: 'https://images.unsplash.com/photo-1544145945-f90425340c7e?w=500&h=500&fit=crop',
    description: 'Refreshing beverages for any occasion',
    count: 14,
  },
];

export default function CategoriesScreen() {
  const router = useRouter();

  const featuredCategories = categories.slice(0, 2);
  const otherCategories = categories.slice(2);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor={colors.white} />
      <View style={styles.header}>
        <Text style={styles.title}>Categories</Text>
        <Text style={styles.subtitle}>Browse all food categories</Text>
      </View>

      <ScrollView 
        style={styles.content} 
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        <SectionHeader
          title="Featured Categories"
          icon={<Grid size={20} color={colors.primary} />}
          showSeeAll={false}
        />

        <View style={styles.featuredContainer}>
          {featuredCategories.map((category) => (
            <CategoryCard
              key={category.id}
              id={category.id}
              name={category.name}
              image={category.image}
              count={category.count}
              size="large"
              style={styles.featuredCard}
            />
          ))}
        </View>

        <SectionHeader
          title="All Categories"
          showSeeAll={false}
        />

        <View style={styles.categoriesGrid}>
          {otherCategories.map((category) => (
            <CategoryCard
              key={category.id}
              id={category.id}
              name={category.name}
              image={category.image}
              count={category.count}
              size="medium"
            />
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: spacing['5'],
    backgroundColor: colors.white,
    borderBottomLeftRadius: borderRadius.xl,
    borderBottomRightRadius: borderRadius.xl,
    ...shadows.md,
  },
  title: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.dark,
  },
  subtitle: {
    fontSize: typography.fontSize.base,
    color: colors.gray,
    marginTop: spacing['1'],
  },
  content: {
    flex: 1,
    padding: spacing['4'],
  },
  scrollContent: {
    paddingBottom: 80, // Add padding at the bottom to prevent content from being hidden by the tab bar
  },
  featuredContainer: {
    marginBottom: spacing['6'],
  },
  featuredCard: {
    width: '100%',
    marginBottom: spacing['3'],
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginHorizontal: -spacing['2'],
  },
});
