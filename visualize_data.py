import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
df = pd.read_csv("data/word_sentiment_stats.csv")

# Only use clean words
df = df[df["confident"] == 1]
df = df[df["frequency"] >= 5]

# Normalize sentiment around dataset baseline
mean_sentiment = df["avg_sentiment"].mean()
df["normalized_sentiment"] = df["avg_sentiment"] - mean_sentiment

print("Mean sentiment baseline:", mean_sentiment)

pos_columns = [
    "noun","verb","adjective","adverb","auxiliary","conjunctions",
    "determiners","prepositions","pronouns"
]

data = []
labels = []

for pos in pos_columns:
    values = df[df[pos] == 1]["normalized_sentiment"]
    if len(values) > 0:
        data.append(values)
        labels.append(pos)

plt.figure()
plt.boxplot(data, labels=labels)
plt.xticks(rotation=45)
plt.title("POS vs Sentiment Distribution")
plt.ylabel("Normalized Sentiment")
plt.show()

positive = df[df["normalized_sentiment"] > 0]
negative = df[df["normalized_sentiment"] < 0]

plt.figure()

plt.scatter(positive["frequency"], positive["normalized_sentiment"], alpha=0.5)
plt.scatter(negative["frequency"], negative["normalized_sentiment"], alpha=0.5)

plt.xlabel("Frequency")
plt.ylabel("Normalized Sentiment")
plt.title("Positive vs Negative Word Distribution")
plt.show()

columns = pos_columns + ["normalized_sentiment", "frequency"]

corr = df[columns].corr()

plt.figure()
plt.imshow(corr)
plt.colorbar()
plt.xticks(range(len(columns)), columns, rotation=90)
plt.yticks(range(len(columns)), columns)
plt.title("Correlation Heatmap")
plt.show()

weights = {}

for pos in pos_columns:
    subset = df[df[pos] == 1]
    if len(subset) > 0:
        weights[pos] = subset["normalized_sentiment"].abs().mean()

plt.figure()
plt.bar(weights.keys(), weights.values())
plt.xticks(rotation=45)
plt.ylabel("Average Absolute Normalized Sentiment")
plt.title("POS vs Semantic Weight")
plt.show()