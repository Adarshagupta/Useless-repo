import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity, RefreshControl } from 'react-native';
import { useState } from 'react';

const newsData = [
  {
    id: '1',
    title: 'Federal Reserve Announces New Interest Rate Decision',
    source: 'Financial Times',
    time: '2h ago',
    image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'
  },
  {
    id: '2',
    title: 'Tech Stocks Rally Amid Positive Earnings Reports',
    source: 'Bloomberg',
    time: '4h ago',
    image: 'https://images.unsplash.com/photo-1642543492481-44e81e3914a7?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'
  },
  {
    id: '3',
    title: 'Global Markets React to Economic Data',
    source: 'Reuters',
    time: '6h ago',
    image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3'
  }
];

export default function NewsScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [newsItems, setNewsItems] = useState(newsData);

  const onRefresh = () => {
    setRefreshing(true);
    // Simulate a data refresh
    setTimeout(() => {
      // In a real app, you would fetch new data here
      // For demo purposes, we'll just update the timestamps
      const updatedNews = newsItems.map(item => ({
        ...item,
        time: 'Just now'
      }));
      setNewsItems(updatedNews);
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
        <Text style={styles.title}>Market News</Text>
      </View>

      {newsItems.map((news) => (
        <TouchableOpacity key={news.id} style={styles.newsCard}>
          <Image source={{ uri: news.image }} style={styles.newsImage} />
          <View style={styles.newsContent}>
            <Text style={styles.newsTitle}>{news.title}</Text>
            <View style={styles.newsFooter}>
              <Text style={styles.newsSource}>{news.source}</Text>
              <Text style={styles.newsTime}>{news.time}</Text>
            </View>
          </View>
        </TouchableOpacity>
      ))}
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
  newsCard: {
    backgroundColor: '#1C1C1E',
    borderRadius: 16,
    margin: 10,
    overflow: 'hidden',
  },
  newsImage: {
    width: '100%',
    height: 200,
  },
  newsContent: {
    padding: 15,
  },
  newsTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#FFFFFF',
    marginBottom: 10,
  },
  newsFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  newsSource: {
    color: '#8E8E93',
    fontSize: 14,
  },
  newsTime: {
    color: '#8E8E93',
    fontSize: 14,
  },
});