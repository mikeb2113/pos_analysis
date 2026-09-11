import csv
import os

wordnet_files = {
    "data/dict/unprocessed_taggers/data.noun": ("noun", "data/dict/intermediate_data/nouns.csv"),
    "data/dict/unprocessed_taggers/data.verb": ("verb", "data/dict/intermediate_data/verbs.csv"),
    "data/dict/unprocessed_taggers/data.adj": ("adjective", "data/dict/intermediate_data/adjectives.csv"),
    "data/dict/unprocessed_taggers/data.adv": ("adverb", "data/dict/intermediate_data/adverbs.csv")
}

for input_file, (pos, output_file) in wordnet_files.items():

    rows = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            # Skip comments and blank lines
            if line.startswith("  ") or line.strip() == "":
                continue

            parts = line.split()

            # WordNet lemma extraction
            if len(parts) > 4:
                word = parts[4].replace("_", " ").lower()
                rows.append([word, pos])

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["word", "pos"])
        writer.writerows(rows)