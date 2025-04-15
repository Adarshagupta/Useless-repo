import { View, Text, StyleSheet, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { VictoryLine, VictoryChart, VictoryTheme, VictoryAxis } from 'victory-native';
import { Dimensions } from 'react-native';
import { useState } from 'react';

export default function AnalysisScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [rsiValue, setRsiValue] = useState(65.4);
  const [macdValue, setMacdValue] = useState(0.002);
  const [volumeValue, setVolumeValue] = useState('$24.5B');

  const screenWidth = Dimensions.get('window').width;

  const onRefresh = () => {
    setRefreshing(true);
    // Simulate a data refresh
    setTimeout(() => {
      // In a real app, you would fetch new analysis data
      // For demo purposes, we'll just update some values
      setRsiValue(parseFloat((60 + Math.random() * 10).toFixed(1)));
      setMacdValue(parseFloat((Math.random() * 0.01).toFixed(3)));
      setVolumeValue(`$${(20 + Math.random() * 10).toFixed(1)}B`);
      setRefreshing(false);
    }, 1500);  // 1.5 seconds delay to simulate network request
  };

  const chartData = [
    { x: 1, y: 20 },
    { x: 2, y: 45 },
    { x: 3, y: 28 },
    { x: 4, y: 80 },
    { x: 5, y: 99 },
    { x: 6, y: 43 }
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
        <Text style={styles.title}>Technical Analysis</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Price Analysis</Text>
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
        <View style={styles.indicators}>
          <View style={styles.indicator}>
            <Text style={styles.indicatorLabel}>RSI</Text>
            <Text style={styles.indicatorValue}>{rsiValue}</Text>
            <Text style={styles.indicatorStatus}>Neutral</Text>
          </View>
          <View style={styles.indicator}>
            <Text style={styles.indicatorLabel}>MACD</Text>
            <Text style={styles.indicatorValue}>{macdValue}</Text>
            <Text style={[styles.indicatorStatus, styles.bullish]}>Bullish</Text>
          </View>
          <View style={styles.indicator}>
            <Text style={styles.indicatorLabel}>MA</Text>
            <Text style={styles.indicatorValue}>200</Text>
            <Text style={[styles.indicatorStatus, styles.bearish]}>Bearish</Text>
          </View>
        </View>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Volume Analysis</Text>
        <View style={styles.volumeStats}>
          <Text style={styles.volumeLabel}>24h Volume</Text>
          <Text style={styles.volumeValue}>{volumeValue}</Text>
          <Text style={styles.volumeChange}>+5.2%</Text>
        </View>
      </View>

      <TouchableOpacity style={styles.analysisButton}>
        <Text style={styles.buttonText}>Generate Detailed Report</Text>
      </TouchableOpacity>
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
  card: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    margin: 10,
    padding: 20,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 15,
  },
  chartContainer: {
    marginVertical: 8,
  },
  indicators: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  indicator: {
    alignItems: 'center',
  },
  indicatorLabel: {
    color: '#8E8E93',
    fontSize: 14,
  },
  indicatorValue: {
    color: '#FFFFFF',
    fontSize: 20,
    fontWeight: '600',
    marginVertical: 5,
  },
  indicatorStatus: {
    color: '#8E8E93',
    fontSize: 14,
  },
  bullish: {
    color: '#34C759',
  },
  bearish: {
    color: '#FF3B30',
  },
  volumeStats: {
    alignItems: 'center',
  },
  volumeLabel: {
    color: '#8E8E93',
    fontSize: 14,
  },
  volumeValue: {
    color: '#FFFFFF',
    fontSize: 24,
    fontWeight: '600',
    marginVertical: 5,
  },
  volumeChange: {
    color: '#34C759',
    fontSize: 16,
  },
  analysisButton: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    margin: 10,
    padding: 16,
    alignItems: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
});