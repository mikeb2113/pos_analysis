import csv
import pandas as pd

def possible_regular_past_bases(word):
    word = word.lower()
    candidates = []

    if word.endswith("ed"):
        candidates.append(word[:-2])

    if word.endswith("d"):
        candidates.append(word[:-1])

    if word.endswith("ied"):
        candidates.append(word[:-3] + "y")

    if (
        len(word) > 4
        and word.endswith("ed")
        and len(word) >= 5
        and word[-3] == word[-4]
    ):
        candidates.append(word[:-3])

    return candidates

def classify_unknown_word(word, known_verbs):
    bases = possible_regular_past_bases(word)

    for base in bases:
        if base in known_verbs:
            return {
                "word": word,
                "pos": "verb",
                "tense": "past",
                "base_form": base,
                "source": "regular_past_rule"
            }

    return {
        "word": word,
        "pos": "unknown",
        "tense": None,
        "base_form": None,
        "source": "unclassified"
    }

reviews = pd.read_csv('backup_csvs/50k_reviews.csv')
verb_list = pd.read_csv('data/pos/core_pos/verbs.csv')
#known_verbs = pd.read_csv('')
#reviews["Original_Review_Text"] = reviews["Review_Text"]
for word in verb_list["word"]:
    tensed = classify_unknown_word(word,verb_list)
    print(tensed)