from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap.umap_ as umap
from sklearn.metrics import balanced_accuracy_score
from sklearn.metrics import average_precision_score
from sklearn.preprocessing import label_binarize
import spacy
from wordcloud import WordCloud
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
import hdbscan
from sklearn.datasets import make_blobs
from sklearn.model_selection import GridSearchCV

input = "data/word_sentiment_stats_with_features.csv"
df = pd.read_csv(input)

df["confident"] = pd.to_numeric(df["confident"], errors="coerce").fillna(0)

# Do NOT filter them out anymore
bad_words = df[df["confident"] == 0].copy()

print("Low-confidence words included:", len(bad_words))
print(bad_words[["word", "resolved_word", "frequency", "avg_sentiment"]].head(50))
bad_words.to_csv("data/included_low_confidence_words.csv", index=False)

open_class = ["noun", "verb", "adjective", "adverb"]

closed_class = [
    "auxiliary",
    "conjunctions",
    "determiners",
    "prepositions",
    "pronouns"
]

df["open_count"] = df[open_class].sum(axis=1)
df["closed_count"] = df[closed_class].sum(axis=1)

df["word_length"] = df["word"].astype(str).str.len()
df["vowel_count"] = df["word"].astype(str).str.count(r"[aeiouAEIOU]")
df = df[df["vowel_count"] >= 1].copy()
df = df[df["frequency"] >= 5].copy()
short_closed_rule = (
    (df["word_length"] <= 3) &
    (df["vowel_count"] >= 1) &
    (df["closed_count"] > 0)
)

closed_dictionary_rule = (
    (df["closed_count"] > 0) &
    (df["open_count"] <= 1) &
    (df["frequency"] >= 100)
)

df["class_type"] = np.select(
    [
        short_closed_rule | closed_dictionary_rule,
        (df["open_count"] > 0) & ~(short_closed_rule | closed_dictionary_rule),
    ],
    [
        "closed",
        "open",
    ],
    default="ambiguous"
)

summary = df.groupby("class_type")[
    [
        "word_length",
        "vowel_count",
        "open_count",
        "closed_count",
        "frequency",
        "double_log_freq",
        "avg_sentiment",
    ]
].agg(
    [
        "mean",
        "median",
        "std",
        "min",
        "max",
        "count",
    ]
)

print("\nClass Summary Statistics:")
print(summary)

summary.to_csv("data/class_summary_statistics.csv")
#features = df[
#    ["double_log_freq", "word_length", "participation_score"]
#].copy()

df["is_short"] = df["word"].str.len() <= 4
df["has_apostrophe"] = df["word"].str.contains("'", regex=False)
df["is_alpha"] = df["word"].str.isalpha()
df["vowel_count"] = df["word"].str.count(r"[aeiou]")

df["unique_char_ratio"] = df["word"].apply(
    lambda w: len(set(str(w))) / len(str(w))
    if len(str(w)) > 0 else 0
)
df["weighted_sentiment"] = df["avg_sentiment"] * 2
features = df[
    [
        "avg_sentiment",
        "double_log_freq",
        "word_length",
    ]
].copy()

features = features.replace([np.inf, -np.inf], np.nan).dropna()

df_model = df.loc[features.index].copy()

df_model = df_model[
    df_model["class_type"].isin(["open", "closed", "ambiguous"])
].copy()

ambiguous_words = df[df["class_type"] == "ambiguous"].copy()

print("\nAmbiguous words:")
print(ambiguous_words[
    [
        "word",
        "open_count",
        "closed_count",
        "noun",
        "verb",
        "adjective",
        "adverb",
        "auxiliary",
        "conjunctions",
        "determiners",
        "prepositions",
        "pronouns",
        "frequency",
        "avg_sentiment"
    ]
].head(100))

print("\nAmbiguous count:", len(ambiguous_words))

ambiguous_words.to_csv("data/ambiguous_words.csv", index=False)

X = features.loc[df_model.index]
y = df_model["class_type"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)
cluster_features = [
    "double_log_freq",
    "word_length",
    "avg_sentiment"
    #"participation_score"
]

X_cluster = X_test[cluster_features].copy()
X_cluster = X_cluster.replace([np.inf, -np.inf], np.nan)
X_cluster = X_cluster.dropna()

scaler = StandardScaler()
X_cluster_scaled = scaler.fit_transform(X_cluster)

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,
    min_samples=5
)

cluster_labels = clusterer.fit_predict(X_cluster_scaled)

df.loc[X_cluster.index, "cluster_labels"] = cluster_labels

# ----------------------------------------
# HDBSCAN evaluation
# ----------------------------------------

cluster_eval = df_model.loc[X_test.index].copy()

cluster_eval["cluster"] = cluster_labels
cluster_eval["actual"] = cluster_eval["class_type"]

# assign each cluster its majority class
cluster_to_label = {}

for cluster_id in cluster_eval["cluster"].unique():

    # skip noise for now
    if cluster_id == -1:
        continue

    subset = cluster_eval[
        cluster_eval["cluster"] == cluster_id
    ]

    majority = subset["actual"].mode()[0]

    cluster_to_label[cluster_id] = majority

print("\nCluster → class mapping")
print(cluster_to_label)

# map cluster IDs to labels
cluster_eval["predicted"] = (
    cluster_eval["cluster"]
    .map(cluster_to_label)
)

# treat HDBSCAN noise as ambiguous
cluster_eval["predicted"] = (
    cluster_eval["predicted"]
    .fillna("ambiguous")
)

labels = ["open", "closed", "ambiguous"]

print("\nHDBSCAN Classification Report")
print(
    classification_report(
        cluster_eval["actual"],
        cluster_eval["predicted"],
        labels=labels
    )
)

hdb_cm = confusion_matrix(
    cluster_eval["actual"],
    cluster_eval["predicted"],
    labels=labels
)

disp = ConfusionMatrixDisplay(
    confusion_matrix=hdb_cm,
    display_labels=labels
)

disp.plot()
plt.title("HDBSCAN Confusion Matrix")
plt.tight_layout()
plt.show()

print(
    "HDBSCAN Balanced Accuracy:",
    balanced_accuracy_score(
        cluster_eval["actual"],
        cluster_eval["predicted"]
    )
)

# Add cluster labels into the model feature set
features = features.copy()
features["cluster_labels"] = df.loc[features.index, "cluster_labels"]

# HDBSCAN uses -1 for noise. Fill missing rows as noise too.
features["cluster_labels"] = features["cluster_labels"].fillna(-1)

X = features.loc[df_model.index]
y = df_model["class_type"]

params = {
    "n_estimators":[100,300,500],
    "max_depth":[3,5,10,None],
    "min_samples_leaf":[1,5,10]
}

grid = GridSearchCV(
    RandomForestClassifier(
        class_weight="balanced",
        random_state=42
    ),
    params,
    scoring="balanced_accuracy",
    cv=5
)

grid.fit(X_train,y_train)

print(grid.best_params_)
print(grid.best_score_)

models = {
    "Bayes": Pipeline([
        ("scaler", StandardScaler()),
        ("model", GaussianNB())
    ]),

    "SVM": Pipeline([
        ("scaler", StandardScaler()),
        ("model", SVC(
            kernel="rbf",
            class_weight="balanced",
            probability=True,
            random_state=42
        ))
    ]),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsClassifier(
            n_neighbors=7,
            weights="distance"
        ))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        max_depth=5,
        min_samples_leaf=10,
        random_state=42,
        class_weight="balanced"
    )
}

model_scores = []

for name, model in models.items():
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_probs = model.predict_proba(X_test)

    bal_acc = balanced_accuracy_score(y_test, y_pred)

    try:
        classes = ["open","closed","ambiguous"]

        y_bin = label_binarize(
            y_test,
            classes=classes
        )

        pr_auc = average_precision_score(
            y_bin,
            y_probs,
            average="macro"
        )

        print("PR-AUC:", pr_auc)
    except ValueError:
        pr_auc = np.nan

    print("Balanced Accuracy:", bal_acc)
    print("ROC-AUC:", pr_auc)

    print(classification_report(
        y_test,
        y_pred,
        labels=["open", "closed", "ambiguous"]
    ))

    cm = confusion_matrix(
        y_test,
        y_pred,
        labels=["open", "closed", "ambiguous"]
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=["open", "closed", "ambiguous"]
    )

    disp.plot()
    plt.title(f"{name} Confusion Matrix")
    plt.tight_layout()
    plt.show()

    model_scores.append({
        "model": name,
        "balanced_accuracy": bal_acc,
        "pr_auc": pr_auc
    })

scores_df = pd.DataFrame(model_scores).sort_values(
    "balanced_accuracy",
    ascending=False
)

print("\nMODEL COMPARISON")
print(scores_df)

scores_df.to_csv("data/model_comparison.csv", index=False)


best_model_name = scores_df.iloc[0]["model"]
best_model = models[best_model_name]

print("\nBest model:", best_model_name)

y_pred = best_model.predict(X_test)
y_probs = best_model.predict_proba(X_test)

classes = best_model.classes_ if hasattr(best_model, "classes_") else best_model.named_steps["model"].classes_

# Create a results dataframe using the same test indexes
results = df_model.loc[X_test.index].copy()

results["actual"] = y_test.values
results["predicted"] = y_pred

results["actual_label"] = results["actual"]
results["predicted_label"] = results["predicted"]
closed_index = list(classes).index("closed")
open_index = list(classes).index("open")
ambiguous_index = list(classes).index("ambiguous")

test_probs = best_model.predict_proba(X_test)

results["prob_closed"] = test_probs[:, closed_index]
results["prob_open"] = test_probs[:, open_index]
results["prob_ambiguous"] = test_probs[:, ambiguous_index]
results["prob_ambiguous"] = test_probs[:, ambiguous_index]

# ----------------------------------------
# Resolve ambiguous predictions
# ----------------------------------------

results["final_prediction"] = results["predicted"]

ambiguous_mask = results["predicted"] == "ambiguous"

results.loc[
    ambiguous_mask &
    (results["prob_open"] > results["prob_closed"]),
    "final_prediction"
] = "open"

results.loc[
    ambiguous_mask &
    (results["prob_closed"] >= results["prob_open"]),
    "final_prediction"
] = "closed"

results["certainty"] = results[
    ["prob_open", "prob_closed", "prob_ambiguous"]
].max(axis=1)

results["final_actual"] = results["actual"]

actual_ambiguous_mask = results["actual"] == "ambiguous"

results.loc[
    actual_ambiguous_mask &
    (results["prob_open"] > results["prob_closed"]),
    "final_actual"
] = "open"

results.loc[
    actual_ambiguous_mask &
    (results["prob_closed"] >= results["prob_open"]),
    "final_actual"
] = "closed"

print("\nResolved ambiguous predictions:")
print(results[
    [
        "word",
        "actual",
        "predicted",
        "final_prediction",
        "certainty",
        "prob_open",
        "prob_closed",
        "prob_ambiguous"
    ]
].head(100))

# ----------------------------------------
# Word clouds from TEST predictions only
# closed -> Function Words
# open -> Concrete Words
# ----------------------------------------

function_words = results[
    results["final_prediction"] == "closed"
]["word"].astype(str)

concrete_words = results[
    results["final_prediction"] == "open"
]["word"].astype(str)

function_text = " ".join(function_words)
concrete_text = " ".join(concrete_words)

function_cloud = WordCloud(
    width=1000,
    height=600,
    background_color="white",
    collocations=False
).generate(function_text)

plt.figure(figsize=(12, 7))
plt.imshow(function_cloud, interpolation="bilinear")
plt.axis("off")
plt.title("Predicted Function Words")
plt.tight_layout()
plt.savefig("data/function_words_wordcloud.png", dpi=300)
plt.show()

concrete_cloud = WordCloud(
    width=1000,
    height=600,
    background_color="white",
    collocations=False
).generate(concrete_text)

plt.figure(figsize=(12, 7))
plt.imshow(concrete_cloud, interpolation="bilinear")
plt.axis("off")
plt.title("Predicted Concrete Words")
plt.tight_layout()
plt.savefig("data/concrete_words_wordcloud.png", dpi=300)
plt.show()


# ----------------------------------------
# Final resolved statistics
# ----------------------------------------

print("\nFINAL RESOLVED CLASSIFICATION REPORT")

print(classification_report(
    results["final_actual"],
    results["final_prediction"],
    labels=["open", "closed"],
    target_names=["open", "closed"]
))

final_cm = confusion_matrix(
    results["final_actual"],
    results["final_prediction"],
    labels=["open", "closed"]
)

final_disp = ConfusionMatrixDisplay(
    confusion_matrix=final_cm,
    display_labels=["open", "closed"]
)

final_disp.plot()
plt.title("Final Resolved Predictions")
plt.show()

print("\nFinal Balanced Accuracy:")
print(
balanced_accuracy_score(
    results["final_actual"],
    results["final_prediction"]
)
)

# ----------------------------------------
# Final prediction averages
# ----------------------------------------

final_summary = results.groupby("final_prediction")[
    [
        "frequency",
        "double_log_freq",
        "word_length",
        "avg_sentiment",
        "certainty"
    ]
].agg(
    [
        "mean",
        "median",
        "std",
        "count"
    ]
)

print("\nFinal Prediction Statistics:")
print(final_summary)

final_summary.to_csv(
    "data/final_prediction_statistics.csv"
)

# ----------------------------------------
# Lowest certainty words
# ----------------------------------------

lowest_certainty = results.sort_values(
    "certainty",
    ascending=True
)

print("\nLowest certainty words:")
print(lowest_certainty[
    [
        "word",
        "actual",
        "predicted",
        "final_prediction",
        "certainty",
        "prob_open",
        "prob_closed",
        "prob_ambiguous"
    ]
].head(100))

lowest_certainty.to_csv(
    "data/lowest_certainty_words.csv",
    index=False
)

# Four confusion-matrix buckets
true_open_pred_open = results[
    (results["actual"] == "open") &
    (results["predicted"] == "open")
].sort_values("prob_closed", ascending=False)

true_open_pred_closed = results[
    (results["actual"] == "open") &
    (results["predicted"] == "closed")
].sort_values("prob_closed", ascending=False)

true_closed_pred_open = results[
    (results["actual"] == "closed") &
    (results["predicted"] == "open")
].sort_values("prob_closed", ascending=False)

true_closed_pred_closed = results[
    (results["actual"] == "closed") &
    (results["predicted"] == "closed")
].sort_values("prob_closed", ascending=False)

cols = [
    "word",
    "actual",
    "predicted",
    "prob_open",
    "prob_closed",
    "frequency",
    "double_log_freq",
    "word_length",
    "participation_score",
    "avg_sentiment",
    "is_short",
    "has_apostrophe",
    "is_alpha",
    "vowel_count",
    "unique_char_ratio",
]

true_open_pred_open[cols].to_csv("data/true_open_pred_open.csv", index=False)
true_open_pred_closed[cols].to_csv("data/true_open_pred_closed.csv", index=False)
true_closed_pred_open[cols].to_csv("data/true_closed_pred_open.csv", index=False)
true_closed_pred_closed[cols].to_csv("data/true_closed_pred_closed.csv", index=False)

print("\nTRUE OPEN → PREDICTED OPEN")
print(true_open_pred_open[cols].head(30))

print("\nTRUE OPEN → PREDICTED CLOSED")
print(true_open_pred_closed[cols].head(30))

print("\nTRUE CLOSED → PREDICTED OPEN")
print(true_closed_pred_open[cols].head(30))

print("\nTRUE CLOSED → PREDICTED CLOSED")
print(true_closed_pred_closed[cols].head(30))
closed_results = results[
    results["actual"] == "closed"
].copy()

print("\nClosed-class cases only:")
print(closed_results[
    [
        "word",
        "predicted",
        "frequency",
        "double_log_freq",
        "word_length",
        "participation_score",
        "avg_sentiment"
    ]
])

missed_closed = results[
    (results["actual"] == "closed") &
    (results["predicted"] != "closed")
].copy()

print("\nMissed closed-class words:")
print(missed_closed[
    [
        "word",
        "predicted",
        "frequency",
        "double_log_freq",
        "word_length",
        "participation_score",
        "avg_sentiment"
    ]
])
# Misclassified rows only
misclassified = results[results["actual"] != results["predicted"]]

print(misclassified[
    [
        "word",
        "actual_label",
        "predicted_label",
        "double_log_freq",
        "word_length",
        "participation_score",
        "frequency",
        "avg_sentiment"
    ]
])

ambiguous_results = results[
    (results["actual"] == "ambiguous") &
    (results["frequency"] >= 5)
].copy()

print("\nAmbiguous word predictions:")
print(ambiguous_results[
    [
        "word",
        "actual",
        "predicted",
        "prob_open",
        "prob_closed",
        "prob_ambiguous",
        "frequency",
        "double_log_freq",
        "word_length",
        "avg_sentiment",
    ]
].head(100))

ambiguous_results[
    [
        "word",
        "actual",
        "predicted",
        "prob_open",
        "prob_closed",
        "prob_ambiguous",
        "frequency",
        "double_log_freq",
        "word_length",
        "avg_sentiment",
    ]
].to_csv(
    "data/ambiguous_word_predictions.csv",
    index=False
)

labels = ["open", "closed", "ambiguous"]
print(classification_report(
    y_test,
    y_pred,
    labels=labels,
    target_names=labels
))
cm = confusion_matrix(y_test, y_pred, labels=labels)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)
disp.plot()
plt.show()
if best_model_name == "Random Forest":
    importance = pd.DataFrame({
        "feature": X.columns,
        "importance": best_model.feature_importances_
    }).sort_values("importance", ascending=False)

    print(importance)

    plt.bar(importance["feature"], importance["importance"])
    plt.xticks(rotation=45)
    plt.ylabel("Importance")
    plt.title("Random Forest Feature Importance")
    plt.tight_layout()
    plt.show()
else:
    print(f"\n{best_model_name} does not have built-in feature_importances_.")

print(importance)

plt.bar(importance["feature"], importance["importance"])
plt.xticks(rotation=45)
plt.ylabel("Importance")
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.show()

print("Balanced Accuracy:",
      balanced_accuracy_score(y_test, y_pred))

audit = df_model.sample(200, random_state=42)

audit[
    [
        "word",
        "class_type",
        #"spacy_label",
        "open_count",
        "closed_count",
        "noun",
        "verb",
        "adjective",
        "adverb",
        "auxiliary",
        "conjunctions",
        "determiners",
        "prepositions",
        "pronouns"
    ]
].to_csv("data/label_audit_sample.csv", index=False)

open_pos = ["noun", "verb", "adjective", "adverb"]

closed_pos = [
    "auxiliary",
    "conjunctions",
    "determiners",
    "prepositions",
    "pronouns"
]

df["open_count"] = df[open_pos].sum(axis=1)
df["closed_count"] = df[closed_pos].sum(axis=1)
df["total_pos_count"] = df[open_pos + closed_pos].sum(axis=1)

df_strict = df[
    (
        ((df["open_count"] > 0) & (df["closed_count"] == 0)) |
        ((df["closed_count"] > 0) & (df["open_count"] == 0))
    )
    &
    (df["total_pos_count"] == 1)
    &
    (df["confident"] == 1)
    &
    (df["frequency"] >= 3)
].copy()

nlp = spacy.load("en_core_web_sm")