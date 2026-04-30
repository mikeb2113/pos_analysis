import pandas as pd
import re
from collections import defaultdict

# Load reviews
reviews = pd.read_csv("data/reviews.csv")

# Load POS tables
nouns = set(pd.read_csv("data/pos/core_pos/nouns.csv")["word"].str.lower())
plural_nouns = set(pd.read_csv("data/pos/core_pos/plural_nouns.csv")["word"].str.lower())
verbs = set(pd.read_csv("data/pos/core_pos/verbs.csv")["word"].str.lower())
adjectives = set(pd.read_csv("data/pos/core_pos/adjectives.csv")["word"].str.lower())
adverbs = set(pd.read_csv("data/pos/core_pos/adverbs.csv")["word"].str.lower())

auxiliary = set(pd.read_csv("data/pos/directors/auxiliary.csv")["word"].str.lower())
compositions = set(pd.read_csv("data/pos/directors/compositions.csv")["word"].str.lower())
conjunctions = set(pd.read_csv("data/pos/directors/conjunctions.csv")["word"].str.lower())
determiners = set(pd.read_csv("data/pos/directors/determiners.csv")["word"].str.lower())
existential_determiners = set(pd.read_csv("data/pos/directors/existential_determiners.csv")["word"].str.lower())
modifiers = set(pd.read_csv("data/pos/directors/modifiers.csv")["word"].str.lower())
negative_quantifiers = set(pd.read_csv("data/pos/directors/negative_quantifiers.csv")["word"].str.lower())
prepositions = set(pd.read_csv("data/pos/directors/prepositions.csv")["word"].str.lower())
universal_determiners = set(pd.read_csv("data/pos/directors/universal_determiners.csv")["word"].str.lower())
pronouns = set(pd.read_csv("data/pronouns.csv")["word"].str.lower())
possessive_determiners = set(pd.read_csv("data/posessive_det.csv")["word"].str.lower())




# Store word stats
word_stats = defaultdict(lambda: {
    "frequency": 0,
    "sentiment_sum": 0.0,
    "review_count": 0
})

def tokenize(text):
    if pd.isna(text):
        return []
    
    text = str(text).lower()
    
    # Remove all non-letter characters
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    
    return text.split()

for _, row in reviews.iterrows():
    text = row["Review_Text"]
    sentiment = row["Sentiment_Polarity"]

    words = tokenize(text)

    for word in words:
        word_stats[word]["frequency"] += 1
        word_stats[word]["sentiment_sum"] += sentiment

    # Optional: count review-level appearances only once per review
    #for word in set(words):
    #    word_stats[word]["review_count"] += 1

rows = []

for word, stats in word_stats.items():
    frequency = stats["frequency"]

    rows.append({
        "word": word,

        "noun": int(word in nouns),
        "verb": int(word in verbs),
        "adjective": int(word in adjectives),
        "adverb": int(word in adverbs),

        "auxiliary": int(word in auxiliary),
        "compositions": int(word in compositions),
        "conjunctions": int(word in conjunctions),
        "determiners": int(word in determiners),
        "existential_determiners": int(word in existential_determiners),
        "modifiers": int(word in modifiers),
        "negative_quantifiers": int(word in negative_quantifiers),
        "prepositions": int(word in prepositions),
        "universal_determiners": int(word in universal_determiners),
        "possessive_determiners": int(word in possessive_determiners),
        "pronouns": int(word in pronouns),

        "frequency": frequency,
        "review_count": stats["review_count"],
        "avg_sentiment": stats["sentiment_sum"] / frequency
    })

word_df = pd.DataFrame(rows)

word_df = word_df.sort_values(
    by="frequency",
    ascending=False
)

word_df.to_csv("data/word_sentiment_stats.csv", index=False)