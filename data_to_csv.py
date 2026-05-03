import csv

wordnet_files = {
    "data/dict/unprocessed_taggers/data.noun": "noun",
    "data/dict/unprocessed_taggers/data.verb": "verb",
    "data/dict/unprocessed_taggers/data.adj": "adjective",
    "data/dict/unprocessed_taggers/data.adv": "adverb"
}

for input_file, pos in wordnet_files.items():
    output_file = f"{pos}s.csv"

    rows = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("  ") or line.strip() == "":
                continue

            parts = line.split()

            if len(parts) > 4:
                word = parts[4].replace("_", " ").lower()
                rows.append([word, pos])

    with open(output_file, "w", newline="", encoding="utf-8") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["word", "pos"])
        writer.writerows(rows)