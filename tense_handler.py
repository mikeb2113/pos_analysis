import pandas as pd
import re

INPUT_FILE = "data/pos/core_pos/verbs.csv"
OUTPUT_FILE = "data/pos/core_pos/expanded_verbs.csv"

WORD_COL = "word"


def is_vowel(char):
    return char.lower() in "aeiou"


def should_double_final_consonant(word):
    """
    Rough rule:
    stop -> stopped, stopping
    plan -> planned, planning
    but not: need -> needed, needing
    """
    if len(word) < 3:
        return False

    if word[-1] in "wxy":
        return False

    return (
        not is_vowel(word[-1])
        and is_vowel(word[-2])
        and not is_vowel(word[-3])
    )


def regular_verb_forms(word):
    word = str(word).strip().lower()
    forms = {word}

    if not word or not re.fullmatch(r"[a-z]+", word):
        return forms

    # 3rd person singular: walks, tries, goes
    if word.endswith(("s", "x", "z", "ch", "sh", "o")):
        forms.add(word + "es")
    elif word.endswith("y") and len(word) > 1 and not is_vowel(word[-2]):
        forms.add(word[:-1] + "ies")
    else:
        forms.add(word + "s")

    # past tense: walked, tried, stopped
    if word.endswith("e"):
        forms.add(word + "d")
    elif word.endswith("y") and len(word) > 1 and not is_vowel(word[-2]):
        forms.add(word[:-1] + "ied")
    elif should_double_final_consonant(word):
        forms.add(word + word[-1] + "ed")
    else:
        forms.add(word + "ed")

    # -ing form: walking, making, lying, stopping
    if word.endswith("ie"):
        forms.add(word[:-2] + "ying")
    elif word.endswith("e") and word not in {"be", "see", "flee", "knee"}:
        forms.add(word[:-1] + "ing")
    elif should_double_final_consonant(word):
        forms.add(word + word[-1] + "ing")
    else:
        forms.add(word + "ing")

    return forms


def main():
    verbs = pd.read_csv(INPUT_FILE)

    expanded_rows = []

    for word in verbs[WORD_COL].dropna():
        for form in regular_verb_forms(word):
            expanded_rows.append({
                "word": form,
                "pos": "verb",
                "source_base": str(word).strip().lower()
            })

    expanded = pd.DataFrame(expanded_rows)

    # remove duplicates
    expanded = expanded.drop_duplicates(subset=["word", "pos"])

    # sort nicely
    expanded = expanded.sort_values(["word", "source_base"])

    expanded.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(expanded)} verb forms to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()