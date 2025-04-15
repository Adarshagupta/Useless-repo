import { View, Text, StyleSheet, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { useState } from 'react';
import { Brain, TrendingUp, TriangleAlert as AlertTriangle, Target, Zap, ChartBar as BarChart3 } from 'lucide-react-native';

export default function AIInsightsScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [sentimentScore, setSentimentScore] = useState(76);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const onRefresh = () => {
    setRefreshing(true);
    // Simulate a data refresh
    setTimeout(() => {
      // In a real app, you would fetch new AI insights
      // For demo purposes, we'll just update the sentiment score slightly
      setSentimentScore(Math.floor(70 + Math.random() * 20)); // Random score between 70-90
      setLastUpdated(new Date());
      setRefreshing(false);
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
        <Text style={styles.title}>AI Insights</Text>
      </View>

      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Brain color="#007AFF" size={24} />
          <Text style={styles.cardTitle}>Market Sentiment Analysis</Text>
        </View>
        <Text style={styles.sentimentScore}>Score: {sentimentScore}/100</Text>
        <Text style={styles.lastUpdated}>Last updated: {lastUpdated.toLocaleTimeString()}</Text>
        <Text style={styles.sentimentText}>
          Market sentiment is currently bullish based on social media analysis and news sentiment.
        </Text>
        <View style={styles.sentimentMetrics}>
          <View style={styles.metric}>
            <Text style={styles.metricLabel}>Social Media</Text>
            <Text style={styles.metricValue}>82%</Text>
          </View>
          <View style={styles.metric}>
            <Text style={styles.metricLabel}>News</Text>
            <Text style={styles.metricValue}>70%</Text>
          </View>
          <View style={styles.metric}>
            <Text style={styles.metricLabel}>Forums</Text>
            <Text style={styles.metricValue}>76%</Text>
          </View>
        </View>
      </View>

      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Target color="#34C759" size={24} />
          <Text style={styles.cardTitle}>Stock Recommendations</Text>
        </View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.recommendationsScroll}>
          <View style={styles.recommendationCard}>
            <Text style={styles.stockSymbol}>AAPL</Text>
            <Text style={styles.recommendationType}>Strong Buy</Text>
            <Text style={styles.targetPrice}>Target: $190</Text>
          </View>
          <View style={styles.recommendationCard}>
            <Text style={styles.stockSymbol}>MSFT</Text>
            <Text style={styles.recommendationType}>Buy</Text>
            <Text style={styles.targetPrice}>Target: $400</Text>
          </View>
          <View style={styles.recommendationCard}>
            <Text style={styles.stockSymbol}>TSLA</Text>
            <Text style={styles.recommendationType}>Hold</Text>
            <Text style={styles.targetPrice}>Target: $255</Text>
          </View>
        </ScrollView>
      </View>

      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <TrendingUp color="#34C759" size={24} />
          <Text style={styles.cardTitle}>Market Predictions</Text>
        </View>
        <View style={styles.predictions}>
          <View style={styles.prediction}>
            <Text style={styles.predictionTitle}>Short Term (24h)</Text>
            <Text style={styles.predictionValue}>+2.5%</Text>
            <Text style={styles.predictionConfidence}>Confidence: 85%</Text>
          </View>
          <View style={styles.prediction}>
            <Text style={styles.predictionTitle}>Medium Term (7d)</Text>
            <Text style={styles.predictionValue}>+5.8%</Text>
            <Text style={styles.predictionConfidence}>Confidence: 75%</Text>
          </View>
          <View style={styles.prediction}>
            <Text style={styles.predictionTitle}>Long Term (30d)</Text>
            <Text style={styles.predictionValue}>+12.3%</Text>
            <Text style={styles.predictionConfidence}>Confidence: 65%</Text>
          </View>
        </View>
      </View>

      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <BarChart3 color="#FF9500" size={24} />
          <Text style={styles.cardTitle}>Sector Analysis</Text>
        </View>
        <View style={styles.sectors}>
          <View style={styles.sector}>
            <Text style={styles.sectorName}>Technology</Text>
            <View style={styles.sectorScore}>
              <View style={[styles.sectorBar, { width: '85%', backgroundColor: '#34C759' }]} />
            </View>
            <Text style={styles.sectorValue}>85%</Text>
          </View>
          <View style={styles.sector}>
            <Text style={styles.sectorName}>Healthcare</Text>
            <View style={styles.sectorScore}>
              <View style={[styles.sectorBar, { width: '70%', backgroundColor: '#007AFF' }]} />
            </View>
            <Text style={styles.sectorValue}>70%</Text>
          </View>
          <View style={styles.sector}>
            <Text style={styles.sectorName}>Finance</Text>
            <View style={styles.sectorScore}>
              <View style={[styles.sectorBar, { width: '60%', backgroundColor: '#FF9500' }]} />
            </View>
            <Text style={styles.sectorValue}>60%</Text>
          </View>
        </View>
      </View>

      <TouchableOpacity style={styles.generateButton}>
        <Zap size={20} color="#FFFFFF" />
        <Text style={styles.buttonText}>Generate New Analysis</Text>
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
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
    marginLeft: 10,
  },
  sentimentScore: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#007AFF',
    marginBottom: 5,
  },
  lastUpdated: {
    fontSize: 12,
    color: '#8E8E93',
    marginBottom: 10,
  },
  sentimentText: {
    color: '#8E8E93',
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 15,
  },
  sentimentMetrics: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 15,
  },
  metric: {
    alignItems: 'center',
  },
  metricLabel: {
    color: '#8E8E93',
    fontSize: 14,
    marginBottom: 5,
  },
  metricValue: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
  },
  recommendationsScroll: {
    marginTop: 10,
  },
  recommendationCard: {
    backgroundColor: '#2C2C2E',
    borderRadius: 12,
    padding: 15,
    marginRight: 10,
    width: 120,
  },
  stockSymbol: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 5,
  },
  recommendationType: {
    color: '#34C759',
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 5,
  },
  targetPrice: {
    color: '#8E8E93',
    fontSize: 12,
  },
  predictions: {
    marginTop: 10,
  },
  prediction: {
    marginBottom: 15,
  },
  predictionTitle: {
    color: '#8E8E93',
    fontSize: 14,
    marginBottom: 5,
  },
  predictionValue: {
    color: '#34C759',
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 5,
  },
  predictionConfidence: {
    color: '#8E8E93',
    fontSize: 12,
  },
  sectors: {
    marginTop: 10,
  },
  sector: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  sectorName: {
    color: '#FFFFFF',
    fontSize: 14,
    width: 100,
  },
  sectorScore: {
    flex: 1,
    height: 8,
    backgroundColor: '#2C2C2E',
    borderRadius: 4,
    marginHorizontal: 10,
    overflow: 'hidden',
  },
  sectorBar: {
    height: '100%',
    borderRadius: 4,
  },
  sectorValue: {
    color: '#8E8E93',
    fontSize: 14,
    width: 40,
    textAlign: 'right',
  },
  generateButton: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    margin: 10,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
});