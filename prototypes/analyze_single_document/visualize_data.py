from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
#df = pd.read_csv("data/word_sentiment_stats.csv")
df = pd.read_csv("data/word_sentiment_stats_with_features.csv")

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

plt.scatter(positive["double_log_freq"], positive["normalized_sentiment"], alpha=0.5)
plt.scatter(negative["double_log_freq"], negative["normalized_sentiment"], alpha=0.5)

plt.xlabel("double_log_freq")
plt.ylabel("Normalized Sentiment")
plt.title("Positive vs Negative Word Distribution")
plt.show()

plt.figure()

for pos in pos_columns:
    subset = df[df[pos] == 1]

    if len(subset) > 0:
        plt.scatter(
            subset["double_log_freq"],
            subset["normalized_sentiment"],
            alpha=0.5,
            label=pos
        )

plt.xlabel("double_log_freq")
plt.ylabel("Normalized Sentiment")
plt.title("Word double_log_freq vs Normalized Sentiment by POS")
plt.legend()
plt.show()

open_class = ["noun", "verb", "adjective", "adverb"]
closed_class = [
    "auxiliary", "conjunctions", "determiners",
    "prepositions", "pronouns"
]

df["open_class"] = df[open_class].sum(axis=1) > 0
df["closed_class"] = df[closed_class].sum(axis=1) > 0
# -------------------------
# Feature Engineering (REQUIRED for classifier)
# -------------------------
df["sentiment_strength"] = df["normalized_sentiment"].abs()
df["log_double_log_freq"] = np.log1p(df["double_log_freq"])
df["double_log_freq_rank"] = df["double_log_freq"].rank(ascending=False)
df["pos_count"] = df[pos_columns].sum(axis=1)
df["word_length"] = df["word"].astype(str).str.len()
plt.figure()

open_df = df[df["open_class"]]
closed_df = df[df["closed_class"]]

plt.scatter(
    open_df["double_log_freq"],
    open_df["normalized_sentiment"],
    alpha=0.5,
    label="Open Class"
)

plt.scatter(
    closed_df["double_log_freq"],
    closed_df["normalized_sentiment"],
    alpha=0.5,
    label="Closed Class"
)

plt.xlabel("double_log_freq")
plt.ylabel("Normalized Sentiment")
plt.title("Word double_log_freq vs Sentiment (Open vs Closed Class)")
plt.legend()
plt.show()

columns = pos_columns + ["normalized_sentiment", "double_log_freq"]

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

# -------------------------
# Prepare labels
# -------------------------
df["label"] = df["open_class"].astype(int)

# Remove ambiguous words (in both open + closed)
clf_df = df[df["open_class"] != df["closed_class"]].copy()

# -------------------------
# Features (you can tweak these)
# -------------------------
features = [
    "normalized_sentiment",
    "sentiment_strength",
    "log_double_log_freq",
    "double_log_freq_rank",
    "pos_count",
    "word_length"
]

clf_df = clf_df.dropna(subset=features)

X = clf_df[features]
y = clf_df["label"]

# -------------------------
# Train/test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------
# Scale features
# -------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -------------------------
# Train model
# -------------------------
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# -------------------------
# Predictions
# -------------------------
y_pred = model.predict(X_test_scaled)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -------------------------
# Feature importance
# -------------------------
importance = model.coef_[0]

print("\nFeature Importance:")
for f, w in zip(features, importance):
    print(f"{f}: {w:.4f}")

# -------------------------
# Plot feature importance
# -------------------------
plt.figure()
plt.barh(features, importance)
plt.xlabel("Coefficient Value")
plt.title("Feature Importance for Open vs Closed Classification")
plt.show()