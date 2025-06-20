import React, { useState, useEffect } from "react";
import { SafeAreaView, ScrollView, StyleSheet, RefreshControl } from "react-native";
import { Card, Title, Paragraph, Chip, Text, ActivityIndicator } from "react-native-paper";
import axios from "axios";

export default function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchScanResults = async () => {
    setLoading(true);
    try {
      const res = await axios.get("http://YOUR_API_IP:8000/scan");
      setData(res.data);
    } catch (e) {
      alert("Failed to fetch data. Is the backend running?");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchScanResults();
  }, []);

  const onRefresh = () => {
    fetchScanResults();
  };

  const renderChip = (label, active, color) =>
    active ? <Chip style={[styles.chip, { backgroundColor: color }]}>{label}</Chip> : null;

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        refreshControl={<RefreshControl refreshing={loading} onRefresh={onRefresh} />}
        contentContainerStyle={{ paddingBottom: 30 }}
      >
        <Title style={styles.title}>📈 Breakout & Signal Scanner</Title>
        {loading && <ActivityIndicator animating={true} size="large" style={{ marginVertical: 20 }} />}
        {!loading &&
          data.map((item) => (
            <Card key={item.Symbol} style={styles.card}>
              <Card.Content>
                <Title>{item.Symbol}</Title>
                <Paragraph>Close: {item.Close}</Paragraph>
                <Paragraph>Week High: {item.Week_High} | Week Low: {item.Week_Low}</Paragraph>
                <Paragraph>Month High: {item.Month_High} | Month Low: {item.Month_Low}</Paragraph>
                <Paragraph style={styles.chipsRow}>
                  {renderChip("Breakout Up", item.Breakout_Up, "#4caf50")}
                  {renderChip("Breakout Down", item.Breakout_Down, "#f44336")}
                  {renderChip("FRD", item.FRD, "#f44336")}
                  {renderChip("FGD", item.FGD, "#4caf50")}
                  {renderChip("Inside Day", item.Inside_Day, "#9e9e9e")}
                  {renderChip("2+ Up", item.TwoPlus_Up, "#4caf50")}
                  {renderChip("2+ Down", item.TwoPlus_Down, "#f44336")}
                </Paragraph>
              </Card.Content>
            </Card>
          ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 10, backgroundColor: "#fff" },
  title: { textAlign: "center", marginVertical: 20 },
  card: { marginBottom: 15 },
  chipsRow: { flexDirection: "row", flexWrap: "wrap", marginTop: 10 },
  chip: { marginRight: 8, marginBottom: 6 },
});