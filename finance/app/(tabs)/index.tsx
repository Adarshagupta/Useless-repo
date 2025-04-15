import { View, Text, StyleSheet, TouchableOpacity, Dimensions, Animated, ScrollView, RefreshControl, ActivityIndicator } from 'react-native';
import { VictoryLine, VictoryChart, VictoryTheme, VictoryAxis } from 'victory-native';
import { TrendingUp, TrendingDown, Globe, DollarSign, Percent, Clock, ArrowUpRight, ArrowDownRight } from 'lucide-react-native';
import { useState, useRef, useCallback, useEffect } from 'react';
import { RefreshAnimation } from '../../components/RefreshAnimation';
import { useMarketData } from '../hooks';

// Define types for our data
interface MarketIndex {
  id: string;
  name: string;
  current_value: number;
  change_percent: number;
  change_amount: number;
  is_positive: boolean;
  is_global: boolean;
  region: string;
  chart_data?: any[];
}

interface Stock {
  id: string;
  name: string;
  current_price: number;
  change_percent: number;
  change_amount: number;
  is_positive: boolean;
  image_url?: string;
}

export default function MarketsScreen() {
  const { data: marketIndices, loading: isLoading, error, refetch } = useMarketData();
  const [refreshing, setRefreshing] = useState(false);
  const [lastUpdated, setLastUpdated] = useState('Just now');
  const screenWidth = Dimensions.get('window').width;

  // Animation values
  const fadeAnim = useRef(new Animated.Value(1)).current;
  const scrollY = useRef(new Animated.Value(0)).current;

  // Calculate the translation for the pull effect - this will move the content down as user pulls
  const translateY = scrollY.interpolate({
    inputRange: [-200, -150, -100, -50, -20, 0],
    outputRange: [150, 110, 70, 35, 15, 0],  // More responsive movement with larger values
    extrapolate: 'clamp',
  });

  // Scale effect for pull-to-refresh - subtle zoom as user pulls
  const scale = scrollY.interpolate({
    inputRange: [-200, -100, 0],
    outputRange: [1.08, 1.04, 1],  // More pronounced scaling
    extrapolate: 'clamp',
  });

  // Rotation effect for pull-to-refresh - subtle tilt as user pulls
  const rotate = scrollY.interpolate({
    inputRange: [-200, -100, 0],
    outputRange: ['4deg', '2deg', '0deg'],  // More gradual rotation
    extrapolate: 'clamp',
  });

  // Opacity effect for content as user pulls
  const contentOpacity = scrollY.interpolate({
    inputRange: [-200, -100, 0],
    outputRange: [0.65, 0.85, 1],  // More gradual opacity change
    extrapolate: 'clamp',
  });

  // Shadow effect that increases as you pull down
  const shadowOpacity = scrollY.interpolate({
    inputRange: [-200, 0],
    outputRange: [0.5, 0],
    extrapolate: 'clamp',
  });

  // Update last updated time when data is refreshed
  useEffect(() => {
    if (!isLoading) {
      const now = new Date();
      setLastUpdated(`${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`);
    }
  }, [isLoading]);

  const onRefresh = useCallback(() => {
    setRefreshing(true);

    // Add a subtle fade effect during refresh
    Animated.timing(fadeAnim, {
      toValue: 0.8,
      duration: 300,
      useNativeDriver: true,
    }).start();

    // Update to handle the refetch properly
    const doRefetch = async () => {
      await refetch();
      
      // Fade back in
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 400,
        useNativeDriver: true,
      }).start();

      setRefreshing(false);
    };
    
    doRefetch();
  }, [refetch, fadeAnim]);

  // Format chart data for S&P 500
  const chartData = marketIndices?.find((index: MarketIndex) => index.name === 'S&P 500')?.chart_data || [
    { x: 1, y: 20 },
    { x: 2, y: 45 },
    { x: 3, y: 28 },
    { x: 4, y: 80 },
    { x: 5, y: 99 },
    { x: 6, y: 43 }
  ];

  // Filter global markets
  const globalMarkets = marketIndices?.filter((index: MarketIndex) => index.is_global) || [];

  // Mock data for top movers
  const topGainers = [
    {
      id: "AAPL",
      name: "Apple Inc.",
      current_price: 173.75,
      change_percent: 2.58,
      change_amount: 4.38,
      is_positive: true
    },
    {
      id: "MSFT",
      name: "Microsoft Corporation",
      current_price: 399.04,
      change_percent: 1.95,
      change_amount: 7.64,
      is_positive: true
    }
  ];

  return (
    <View style={styles.container}>
      <RefreshAnimation visible={refreshing} />
      <Animated.ScrollView
        style={styles.scrollView}
        contentContainerStyle={styles.contentContainer}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor="#007AFF"
            colors={["#007AFF"]} // Android
            progressBackgroundColor="#1C1C1E" // Android
            progressViewOffset={30} // Increased offset for better visibility
            // size="large" // Larger indicator (not supported in all versions)
          />
        }
        scrollEventThrottle={16}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { y: scrollY } } }],
          { useNativeDriver: true }
        )}
      >
        <Animated.View
          style={[styles.content, {
            opacity: Animated.multiply(fadeAnim, contentOpacity),
            transform: [
              { translateY },
              { scale },
              { rotate }
            ],
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 10 },
            shadowOpacity: shadowOpacity,
            shadowRadius: 15,
            elevation: 10
          }]}>
          <View style={styles.header}>
            <Text style={styles.title}>Market Overview</Text>
            <View style={styles.timeContainer}>
              <Clock size={16} color="#8E8E93" />
              <Text style={styles.timeText}>Last updated: {lastUpdated}</Text>
            </View>
          </View>

          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.indicesScroll}>
        {isLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#007AFF" />
          </View>
        ) : (marketIndices || []).filter((index: MarketIndex) => !index.is_global).map((index: MarketIndex) => (
          <View key={index.name} style={styles.indexCard}>
            <Text style={styles.indexName}>{index.name}</Text>
            <Text style={styles.indexValue}>{index.current_value.toLocaleString()}</Text>
            <View style={[styles.changeContainer, index.is_positive ? styles.positive : styles.negative]}>
              {index.is_positive ? (
                <TrendingUp size={16} color="#34C759" />
              ) : (
                <TrendingDown size={16} color="#FF3B30" />
              )}
              <Text style={[styles.changeText, index.is_positive ? styles.positiveText : styles.negativeText]}>
                {index.is_positive ? '+' : ''}{index.change_percent.toFixed(2)}%
              </Text>
            </View>
          </View>
        ))}
      </ScrollView>

      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Text style={styles.cardTitle}>S&P 500</Text>
          <TouchableOpacity style={styles.periodSelector}>
            <Text style={styles.periodText}>1Y</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.chartContainer}>
          <VictoryChart
            theme={VictoryTheme.material}
            width={screenWidth - 40}
            height={220}
            padding={{ top: 10, bottom: 30, left: 40, right: 40 }}
          >
            <VictoryAxis
              style={{
                axis: { stroke: '#8E8E93' },
                tickLabels: { fill: '#8E8E93', fontSize: 12 }
              }}
            />
            <VictoryAxis
              dependentAxis
              style={{
                axis: { stroke: '#8E8E93' },
                tickLabels: { fill: '#8E8E93', fontSize: 12 }
              }}
            />
            <VictoryLine
              data={chartData}
              style={{
                data: { stroke: '#007AFF' },
              }}
              animate={{
                duration: 2000,
                onLoad: { duration: 1000 }
              }}
            />
          </VictoryChart>
        </View>
      </View>

      <View style={styles.marketStats}>
        <View style={styles.statCard}>
          <DollarSign size={20} color="#007AFF" />
          <Text style={styles.statLabel}>Market Cap</Text>
          <Text style={styles.statValue}>$34.5T</Text>
          <Text style={styles.statChange}>+2.3%</Text>
        </View>
        <View style={styles.statCard}>
          <ArrowUpRight size={20} color="#007AFF" />
          <Text style={styles.statLabel}>24h Volume</Text>
          <Text style={styles.statValue}>$86.2B</Text>
          <Text style={styles.statChange}>+5.8%</Text>
        </View>
        <View style={styles.statCard}>
          <Percent size={20} color="#007AFF" />
          <Text style={styles.statLabel}>Volatility</Text>
          <Text style={styles.statValue}>1.2%</Text>
          <Text style={styles.statChange}>-0.3%</Text>
        </View>
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Top Movers</Text>
          <TouchableOpacity>
            <Text style={styles.seeAll}>See All</Text>
          </TouchableOpacity>
        </View>
        {isLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#007AFF" />
          </View>
        ) : topGainers.map((stock: Stock) => (
          <TouchableOpacity key={stock.id} style={styles.moverCard}>
            <View>
              <Text style={styles.stockSymbol}>{stock.id}</Text>
              <Text style={styles.stockName}>{stock.name}</Text>
            </View>
            <View style={styles.stockInfo}>
              <Text style={styles.stockPrice}>${stock.current_price.toFixed(2)}</Text>
              <View style={[styles.changeContainer, stock.is_positive ? styles.positive : styles.negative]}>
                {stock.is_positive ? (
                  <ArrowUpRight size={16} color="#34C759" />
                ) : (
                  <ArrowDownRight size={16} color="#FF3B30" />
                )}
                <Text style={[styles.changeText, stock.is_positive ? styles.positiveText : styles.negativeText]}>
                  {stock.is_positive ? '+' : ''}{stock.change_percent.toFixed(2)}%
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <View style={styles.sectionTitleContainer}>
            <Globe size={20} color="#FFFFFF" />
            <Text style={styles.sectionTitle}>Global Markets</Text>
          </View>
          <TouchableOpacity>
            <Text style={styles.seeAll}>See All</Text>
          </TouchableOpacity>
        </View>
        {isLoading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color="#007AFF" />
          </View>
        ) : globalMarkets.map((market: MarketIndex) => (
          <View key={market.name} style={styles.globalMarketCard}>
            <Text style={styles.marketName}>{market.name}</Text>
            <View style={styles.marketInfo}>
              <Text style={styles.marketValue}>{market.current_value.toLocaleString()}</Text>
              <View style={[styles.changeContainer, market.is_positive ? styles.positive : styles.negative]}>
                {market.is_positive ? (
                  <TrendingUp size={16} color="#34C759" />
                ) : (
                  <TrendingDown size={16} color="#FF3B30" />
                )}
                <Text style={[styles.changeText, market.is_positive ? styles.positiveText : styles.negativeText]}>
                  {market.is_positive ? '+' : ''}{market.change_percent.toFixed(2)}%
                </Text>
              </View>
            </View>
          </View>
        ))}
      </View>
        </Animated.View>
      </Animated.ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  scrollView: {
    flex: 1,
    backgroundColor: '#000000',
  },
  contentContainer: {
    paddingBottom: 20,
  },
  content: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    minWidth: 150,
  },
  header: {
    padding: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  timeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  timeText: {
    color: '#8E8E93',
    marginLeft: 6,
    fontSize: 14,
  },
  indicesScroll: {
    paddingLeft: 20,
    marginBottom: 20,
  },
  indexCard: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    padding: 16,
    marginRight: 12,
    width: 160,
  },
  indexName: {
    color: '#8E8E93',
    fontSize: 14,
    marginBottom: 8,
  },
  indexValue: {
    color: '#FFFFFF',
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  card: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    margin: 20,
    padding: 15,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  periodSelector: {
    backgroundColor: '#2C2C2E',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  periodText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  chartContainer: {
    marginVertical: 8,
    borderRadius: 16,
  },
  marketStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    paddingTop: 0,
  },
  statCard: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    padding: 16,
    flex: 1,
    marginHorizontal: 5,
    alignItems: 'center',
  },
  statLabel: {
    color: '#8E8E93',
    fontSize: 14,
    marginTop: 8,
  },
  statValue: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 4,
  },
  statChange: {
    color: '#34C759',
    fontSize: 14,
    marginTop: 4,
  },
  section: {
    padding: 20,
    paddingTop: 0,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 8,
  },
  seeAll: {
    color: '#007AFF',
    fontSize: 14,
  },
  moverCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#1C1C1E',
    padding: 16,
    borderRadius: 12,
    marginBottom: 10,
  },
  stockSymbol: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  stockName: {
    color: '#8E8E93',
    fontSize: 14,
  },
  stockInfo: {
    alignItems: 'flex-end',
  },
  stockPrice: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  globalMarketCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#1C1C1E',
    padding: 16,
    borderRadius: 12,
    marginBottom: 10,
  },
  marketName: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  marketInfo: {
    alignItems: 'flex-end',
  },
  marketValue: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 4,
  },
  changeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  positive: {
    backgroundColor: 'rgba(52, 199, 89, 0.1)',
  },
  negative: {
    backgroundColor: 'rgba(255, 59, 48, 0.1)',
  },
  changeText: {
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 4,
  },
  positiveText: {
    color: '#34C759',
  },
  negativeText: {
    color: '#FF3B30',
  },
});