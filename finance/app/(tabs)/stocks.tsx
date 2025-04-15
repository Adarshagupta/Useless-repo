import { View, Text, StyleSheet, ScrollView, TextInput, TouchableOpacity, Image, RefreshControl } from 'react-native';
import { Search, TrendingUp, TrendingDown, Star } from 'lucide-react-native';
import { useState } from 'react';

const popularStocks = [
  {
    symbol: 'AAPL',
    name: 'Apple Inc.',
    price: '173.50',
    change: '+2.5%',
    positive: true,
    image: 'https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'
  },
  {
    symbol: 'TSLA',
    name: 'Tesla, Inc.',
    price: '248.48',
    change: '-1.2%',
    positive: false,
    image: 'https://images.unsplash.com/photo-1617788138017-80ad40651399?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'
  },
  {
    symbol: 'MSFT',
    name: 'Microsoft Corporation',
    price: '378.85',
    change: '+1.8%',
    positive: true,
    image: 'https://images.unsplash.com/photo-1642132652075-2f62cdfc3d0e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'
  }
];

export default function StocksScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  const onRefresh = () => {
    setRefreshing(true);
    // Simulate a data refresh
    setTimeout(() => {
      setRefreshing(false);
      // You could update stock data here in a real app
    }, 1500);  // 1.5 seconds delay to simulate network request
  };

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
          tintColor="#FFFFFF"
          colors={["#007AFF"]} // Android
          progressBackgroundColor="#1C1C1E" // Android
        />
      }>
      <View style={styles.header}>
        <Text style={styles.title}>Stocks</Text>
      </View>

      <View style={styles.searchContainer}>
        <View style={styles.searchBox}>
          <Search color="#8E8E93" size={20} />
          <TextInput
            style={styles.searchInput}
            placeholder="Search stocks..."
            placeholderTextColor="#8E8E93"
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Popular Stocks</Text>
        {popularStocks.map((stock, index) => (
          <TouchableOpacity key={stock.symbol} style={styles.stockCard}>
            <Image source={{ uri: stock.image }} style={styles.stockImage} />
            <View style={styles.stockInfo}>
              <View style={styles.stockHeader}>
                <Text style={styles.stockSymbol}>{stock.symbol}</Text>
                <TouchableOpacity>
                  <Star size={20} color="#8E8E93" />
                </TouchableOpacity>
              </View>
              <Text style={styles.stockName}>{stock.name}</Text>
            </View>
            <View style={styles.stockPrice}>
              <Text style={styles.priceText}>${stock.price}</Text>
              <View style={[styles.changeContainer, stock.positive ? styles.positive : styles.negative]}>
                {stock.positive ? (
                  <TrendingUp size={16} color="#34C759" />
                ) : (
                  <TrendingDown size={16} color="#FF3B30" />
                )}
                <Text style={[styles.changeText, stock.positive ? styles.positiveText : styles.negativeText]}>
                  {stock.change}
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Market Movers</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.moversScroll}>
          {popularStocks.map((stock) => (
            <TouchableOpacity key={stock.symbol} style={styles.moverCard}>
              <Text style={styles.moverSymbol}>{stock.symbol}</Text>
              <Text style={[styles.moverChange, stock.positive ? styles.positiveText : styles.negativeText]}>
                {stock.change}
              </Text>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
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
  searchContainer: {
    padding: 20,
    paddingTop: 0,
  },
  searchBox: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1C1C1E',
    borderRadius: 12,
    padding: 12,
  },
  searchInput: {
    flex: 1,
    color: '#FFFFFF',
    marginLeft: 10,
    fontSize: 16,
  },
  section: {
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 20,
    marginBottom: 15,
  },
  stockCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1C1C1E',
    marginHorizontal: 20,
    marginBottom: 10,
    borderRadius: 16,
    padding: 15,
  },
  stockImage: {
    width: 40,
    height: 40,
    borderRadius: 20,
  },
  stockInfo: {
    flex: 1,
    marginLeft: 15,
  },
  stockHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  stockSymbol: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  stockName: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 4,
  },
  stockPrice: {
    alignItems: 'flex-end',
  },
  priceText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  changeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
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
  moversScroll: {
    paddingLeft: 20,
  },
  moverCard: {
    backgroundColor: '#1C1C1E',
    borderRadius: 12,
    padding: 15,
    marginRight: 10,
    width: 100,
    alignItems: 'center',
  },
  moverSymbol: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  moverChange: {
    fontSize: 14,
    fontWeight: '600',
  },
});