import { View, Text, StyleSheet, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { VictoryLine, VictoryChart, VictoryTheme, VictoryAxis } from 'victory-native';
import { Dimensions } from 'react-native';
import { TrendingUp, TrendingDown, DollarSign, ChartPie as PieChart, ArrowUpRight } from 'lucide-react-native';
import { useState } from 'react';

export default function PortfolioScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [portfolioValue, setPortfolioValue] = useState('$32,000.00');
  const [portfolioChange, setPortfolioChange] = useState('+$2,500 (8.47%)');

  const screenWidth = Dimensions.get('window').width;

  const onRefresh = () => {
    setRefreshing(true);
    // Simulate a data refresh
    setTimeout(() => {
      // In a real app, you would fetch updated portfolio data
      // For demo purposes, we'll just update the portfolio value slightly
      setPortfolioValue('$32,150.75');
      setPortfolioChange('+$2,650.75 (8.98%)');
      setRefreshing(false);
    }, 1500);  // 1.5 seconds delay to simulate network request
  };

  const chartData = [
    { x: 1, y: 25000 },
    { x: 2, y: 27500 },
    { x: 3, y: 26800 },
    { x: 4, y: 30000 },
    { x: 5, y: 29500 },
    { x: 6, y: 32000 }
  ];

  const holdings = [
    { symbol: 'AAPL', shares: 50, value: 8675, change: '+2.5%', positive: true },
    { symbol: 'TSLA', shares: 20, value: 4969.60, change: '-1.2%', positive: false },
    { symbol: 'MSFT', shares: 30, value: 11365.50, change: '+1.8%', positive: true },
  ];

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
        <Text style={styles.title}>Portfolio</Text>
        <TouchableOpacity style={styles.addButton}>
          <Text style={styles.addButtonText}>Add Assets</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.totalValue}>
        <Text style={styles.totalValueLabel}>Total Value</Text>
        <Text style={styles.totalValueAmount}>{portfolioValue}</Text>
        <View style={styles.changeIndicator}>
          <TrendingUp size={16} color="#34C759" />
          <Text style={styles.changeText}>{portfolioChange}</Text>
        </View>
      </View>

      <View style={styles.chart}>
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

      <View style={styles.quickStats}>
        <View style={styles.statCard}>
          <DollarSign size={24} color="#007AFF" />
          <Text style={styles.statValue}>$2.5K</Text>
          <Text style={styles.statLabel}>Today's Gain</Text>
        </View>
        <View style={styles.statCard}>
          <PieChart size={24} color="#007AFF" />
          <Text style={styles.statValue}>12</Text>
          <Text style={styles.statLabel}>Holdings</Text>
        </View>
        <View style={styles.statCard}>
          <ArrowUpRight size={24} color="#007AFF" />
          <Text style={styles.statValue}>8.47%</Text>
          <Text style={styles.statLabel}>Return</Text>
        </View>
      </View>

      <View style={styles.holdingsSection}>
        <Text style={styles.sectionTitle}>Your Holdings</Text>
        {holdings.map((holding) => (
          <TouchableOpacity key={holding.symbol} style={styles.holdingCard}>
            <View style={styles.holdingMain}>
              <Text style={styles.holdingSymbol}>{holding.symbol}</Text>
              <Text style={styles.holdingShares}>{holding.shares} shares</Text>
            </View>
            <View style={styles.holdingValue}>
              <Text style={styles.valueText}>${holding.value.toLocaleString()}</Text>
              <View style={[styles.changeContainer, holding.positive ? styles.positive : styles.negative]}>
                {holding.positive ? (
                  <TrendingUp size={16} color="#34C759" />
                ) : (
                  <TrendingDown size={16} color="#FF3B30" />
                )}
                <Text style={[styles.holdingChange, holding.positive ? styles.positiveText : styles.negativeText]}>
                  {holding.change}
                </Text>
              </View>
            </View>
          </TouchableOpacity>
        ))}
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  addButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  addButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  totalValue: {
    padding: 20,
    alignItems: 'center',
  },
  totalValueLabel: {
    fontSize: 16,
    color: '#8E8E93',
    marginBottom: 8,
  },
  totalValueAmount: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  changeIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(52, 199, 89, 0.1)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  changeText: {
    color: '#34C759',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 6,
  },
  chart: {
    padding: 20,
  },
  quickStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
  },
  statCard: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    flex: 1,
    marginHorizontal: 5,
  },
  statValue: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 8,
  },
  statLabel: {
    color: '#8E8E93',
    fontSize: 12,
    marginTop: 4,
  },
  holdingsSection: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 15,
  },
  holdingCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#1C1C1E',
    padding: 16,
    borderRadius: 12,
    marginBottom: 10,
  },
  holdingMain: {
    flex: 1,
  },
  holdingSymbol: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  holdingShares: {
    fontSize: 14,
    color: '#8E8E93',
  },
  holdingValue: {
    alignItems: 'flex-end',
  },
  valueText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
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
  holdingChange: {
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