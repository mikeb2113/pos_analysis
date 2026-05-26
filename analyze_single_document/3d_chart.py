import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap.umap_ as umap

input = "data/word_sentiment_stats_with_features.csv"

df = pd.read_csv(input)

open_class = ["noun", "verb", "adjective", "adverb"]

closed_class = [
    "auxiliary",
    "conjunctions",
    "determiners",
    "prepositions",
    "pronouns"
]

df["open_class"] = df[open_class].sum(axis=1) > 0
df["closed_class"] = df[closed_class].sum(axis=1) > 0

# Assign colors
df["color"] = np.where(df["closed_class"], "orange", "teal")

# 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(
    df['log_relative_frequency'],
    df['length'],
    df['participation_score'],
    marker='o',
    c=df["color"]
)

ax.set_xlabel('Relative Frequency')
ax.set_ylabel('Word Length')
ax.set_zlabel('Participation Score')

plt.show()

features = df[
    ["log_relative_frequency", "length", "participation_score"]
]
# Scale features
scaled = StandardScaler().fit_transform(features)

# Cluster
dbscan = DBSCAN(
    eps=0.3,
    min_samples=10
)

clusters = dbscan.fit_predict(scaled)

df["cluster"] = clusters

ax.scatter(
    df['log_relative_frequency'],
    df['length'],
    df['participation_score'],
    c=df['cluster'],
    cmap='tab10'
)


pca = PCA(n_components=2)

reduced = pca.fit_transform(scaled)

plt.scatter(
    reduced[:,0],
    reduced[:,1],
    c=df["closed_class"],
    alpha=0.5
)

plt.show()

reducer = umap.UMAP()

embedding = reducer.fit_transform(scaled)

plt.scatter(
    embedding[:,0],
    embedding[:,1],
    c=df["closed_class"],
    alpha=0.5
)

plt.show()
#word,noun,verb,adjective,adverb,auxiliary,compositions,conjunctions,determiners,
#existential_determiners,modifiers,negative_quantifiers,prepositions,universal_determiners,
#possessive_determiners,pronouns,frequency,review_count,avg_sentiment,length,confident,
#resolved_word,relative_frequency,log_relative_frequency,participation_score

