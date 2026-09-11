import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# ===================== CONFIG =====================
input_file = "data/dict/working_set/word_sentiment_stats.csv"
output_file = "data/word_sentiment_stats_with_clusters.csv"

df = pd.read_csv(input_file)

pos_columns = [
    "noun", "verb", "adjective", "adverb", "auxiliary", "compositions",
    "conjunctions", "determiners", "existential_determiners", "modifiers",
    "negative_quantifiers", "prepositions", "universal_determiners",
    "possessive_determiners", "pronouns"
]

open_class_cols = ["noun", "verb", "adjective", "adverb"]
closed_class_cols = [col for col in pos_columns if col not in open_class_cols]

# ===================== FEATURE ENGINEERING =====================
df["frequency"] = pd.to_numeric(df["frequency"], errors="coerce").fillna(0)
total_frequency = df["frequency"].sum()
df["relative_frequency"] = df["frequency"] / total_frequency
df["log_relative_frequency"] = np.log(df["relative_frequency"].replace(0, np.nan))

df[pos_columns] = df[pos_columns].apply(pd.to_numeric, errors="coerce").fillna(0)

# Scores
df["open_score"] = df[open_class_cols].sum(axis=1)
df["closed_score"] = df[closed_class_cols].sum(axis=1)
df["participation_score"] = df[pos_columns].sum(axis=1) / len(pos_columns)

# True linguistic class
def classify_word(row):
    if row["open_score"] > 0 and row["closed_score"] == 0:
        return "open"
    elif row["closed_score"] > 0 and row["open_score"] == 0:
        return "closed"
    elif row["open_score"] > 0 and row["closed_score"] > 0:
        return "mixed"
    else:
        return "unknown"

df["true_class"] = df.apply(classify_word, axis=1)

# ===================== CLUSTERING =====================
cluster_features = [
    "log_relative_frequency",
    "participation_score",
    "open_score",
    "closed_score"
]

# Normalize open/closed scores for better clustering
df["open_score_norm"] = df["open_score"] / (df["open_score"] + df["closed_score"] + 1e-8)
df["closed_score_norm"] = df["closed_score"] / (df["open_score"] + df["closed_score"] + 1e-8)

cluster_features = ["log_relative_frequency", "participation_score", 
                   "open_score_norm", "closed_score_norm"]

df_cluster = df.dropna(subset=cluster_features).copy()
X = df_cluster[cluster_features]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Evaluate k
print("Silhouette scores:")
for k in range(2, 8):
    kmeans_test = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels_test = kmeans_test.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels_test)
    print(f"k={k}: {score:.4f}")

# Final clustering (you can adjust k)
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
df_cluster["cluster"] = kmeans.fit_predict(X_scaled)

# Map back to original df
df["cluster"] = np.nan
df.loc[df_cluster.index, "cluster"] = df_cluster["cluster"]

# ===================== ANALYSIS =====================
print("\n=== Cluster vs True Class ===")
print(pd.crosstab(df_cluster["cluster"], df_cluster["true_class"], margins=True))

print("\n=== Cluster Summary ===")
summary = df_cluster.groupby("cluster").agg({
    "frequency": "mean",
    "log_relative_frequency": "mean",
    "participation_score": "mean",
    "open_score_norm": "mean",
    "true_class": lambda x: x.value_counts().to_dict()
}).round(4)
print(summary)

# ===================== SAVE =====================
df.to_csv(output_file, index=False)
print(f"\nSaved to {output_file}")

# ===================== PREVIEW =====================
for cluster_id in sorted(df_cluster["cluster"].unique()):
    print(f"\n--- Cluster {cluster_id} ---")
    preview = df_cluster[df_cluster["cluster"] == cluster_id].sort_values(
        "frequency", ascending=False
    )[["word", "frequency", "true_class", "open_score_norm", 
       "log_relative_frequency", "participation_score"]].head(15)
    print(preview.to_string(index=False))

# ===================== PLOTS =====================
plt.figure(figsize=(12, 8))

# Main scatter plot colored by cluster
scatter = plt.scatter(
    df_cluster["log_relative_frequency"],
    df_cluster["participation_score"],
    c=df_cluster["cluster"],
    s=12,
    cmap="viridis",
    alpha=0.7
)
plt.xlabel("Log Relative Frequency")
plt.ylabel("Participation Score")
plt.title("Word Clusters (Open vs Closed Class)")
plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.show()

# Optional: Plot colored by true linguistic class
plt.figure(figsize=(12, 8))
colors = {"open": "blue", "closed": "red", "mixed": "green", "unknown": "gray"}
for cls, color in colors.items():
    subset = df_cluster[df_cluster["true_class"] == cls]
    plt.scatter(
        subset["log_relative_frequency"],
        subset["participation_score"],
        c=color,
        s=12,
        alpha=0.7,
        label=cls
    )
plt.xlabel("Log Relative Frequency")
plt.ylabel("Participation Score")
plt.title("Words Colored by True Class (Open/Closed)")
plt.legend()
plt.tight_layout()
plt.show()