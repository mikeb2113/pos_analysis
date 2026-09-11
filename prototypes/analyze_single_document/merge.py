import csv
import os

VALID_POS_TAGS = {"noun", "verb", "adj", "adv"}
SKIP_VALUES = {"word", "pos", "noun", "verb", "adj", "adv", "adjective", "adverb"}


def normalize_pos_files(input_files, output_file, pos_label):
    rows_out = [["word", "pos"]]
    seen = set()

    def clean_word(value):
        return str(value).strip().lower()

    def add_word(value):
        word = clean_word(value)

        if not word:
            return

        if word in SKIP_VALUES:
            return

        key = (word, pos_label)

        if key not in seen:
            rows_out.append([word, pos_label])
            seen.add(key)

    for file_path in input_files:
        with open(file_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                cleaned = [clean_word(cell) for cell in row if clean_word(cell)]

                if not cleaned:
                    continue

                # skip headers like: word,pos
                if cleaned[0] == "word":
                    continue

                # CASE 1: one column
                # word
                if len(cleaned) == 1:
                    add_word(cleaned[0])

                # CASE 2: two columns
                # word,pos
                elif len(cleaned) == 2:
                    first, second = cleaned

                    if second in VALID_POS_TAGS or second in {"adjective", "adverb"}:
                        add_word(first)
                    else:
                        # two words accidentally side-by-side
                        add_word(first)
                        add_word(second)

                # CASE 3: three+ columns
                # awake,awoke,awoken
                else:
                    for cell in cleaned:
                        add_word(cell)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as csv_out:
        writer = csv.writer(csv_out)
        writer.writerows(rows_out)

    print(f"Saved {len(rows_out) - 1} rows to {output_file}")


normalize_pos_files(
    [
        "data/dict/intermediate_data/wordnet_data/verbs.csv",
        "data/dict/intermediate_data/kaggle_sets/verbs.csv"
    ],
    "data/output/verbs.csv",
    "verb"
)

normalize_pos_files(
    [
        "data/dict/intermediate_data/wordnet_data/nouns.csv",
        "data/dict/intermediate_data/kaggle_sets/nouns.csv"
    ],
    "data/dict/working_set/open_class/nouns.csv",
    "noun"
)

normalize_pos_files(
    [
        "data/dict/intermediate_data/wordnet_data/adverbs.csv",
        "data/dict/intermediate_data/kaggle_sets/adverbs.csv"
    ],
    "data/dict/working_set/open_class/adverbs.csv",
    "adv"
)

normalize_pos_files(
    [
        "data/dict/intermediate_data/wordnet_data/adjectives.csv",
        "data/dict/intermediate_data/kaggle_sets/adjectives.csv"
    ],
    "data/dict/working_set/open_class/adjectives.csv",
    "adj"
)