import pandas as pd

df = pd.read_csv(
    "data/dict/csvs/nouns2.csv",
    header=None,
    engine="python",
    on_bad_lines="skip"
)

flat = pd.DataFrame({
    "word": pd.concat([df[col] for col in df.columns], ignore_index=True)
})

flat = flat.dropna()

flat.to_csv("nouns2_clean.csv", index=False)