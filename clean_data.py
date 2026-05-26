import pandas as pd
from langdetect import detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import unicodedata
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path
from aggregate import file_mapping, files

#This takes a long time to complete! Rest assured it is not broken. You might want to do something else as this works!
analyzer = SentimentIntensityAnalyzer()
DetectorFactory.seed = 0

def clean_text(text):
    if pd.isna(text):
        return ""

    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    return text


def detect_language_status(text):
    try:
        text = str(text).strip()
        if not text:
            return "empty", None

        langs = detect_langs(text)
        top = langs[0]

        if top.lang == "en" and top.prob >= 0.80:
            return "english", top.prob

        if any(l.lang == "en" and l.prob >= 0.30 for l in langs):
            return "maybe_english", top.prob

        if top.prob >= 0.90:
            return "confident_non_english", top.prob

        return "uncertain_non_english", top.prob

    except LangDetectException:
        return "unknown", None

for file in files:#go to the original files: take each file individually
    for sentence in file.sentences:
        print(sentence.text)
        path = file_mapping.get(file)
        print(f"Source: {file.source_name}")
        path = "data/dict/working_set/pdfs_as_csvs/" + file.source_name + ".csv" #Output to this address as a csv
        # preserve original text
        file["Original_Review_Text"] = sentence.text #Save the original text in case of a translation being required

        for idx, value in sentence.text.items():#attempt to translate each sentence
            status, confidence = detect_language_status(value)

            file.at[idx, "Language_Status"] = status
            file.at[idx, "Language_Confidence"] = confidence

            cleaned_original = clean_text(value)

            try:
                # SAFER: only translate when confidently non-English
                if status == "confident_non_english":
                    translated = GoogleTranslator(source="auto", target="en").translate(str(value))
                    cleaned = clean_text(translated)
                    file.at[idx, "Was_Translated"] = 1
                    file.at[idx, "Translated_Text"] = cleaned
                else:
                    cleaned = cleaned_original
                    file.at[idx, "Was_Translated"] = 0
                    file.at[idx, "Translated_Text"] = ""

            except Exception:
                cleaned = cleaned_original
                file.at[idx, "Was_Translated"] = 0
                file.at[idx, "Translated_Text"] = ""

            file.at[idx, "Review_Text"] = cleaned
            file.at[idx, "Sentiment_Polarity"] = analyzer.polarity_scores(cleaned)["compound"]

        file.to_csv(path, index=False)