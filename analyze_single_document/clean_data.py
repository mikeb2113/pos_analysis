import pandas as pd
from load_data import pos, reviews
from langdetect import detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import unicodedata
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
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


# preserve original text
reviews["Original_Review_Text"] = reviews["Review_Text"]

for idx, value in reviews["Review_Text"].items():
    status, confidence = detect_language_status(value)

    reviews.at[idx, "Language_Status"] = status
    reviews.at[idx, "Language_Confidence"] = confidence

    cleaned_original = clean_text(value)

    try:
        # SAFER: only translate when confidently non-English
        if status == "confident_non_english":
            translated = GoogleTranslator(source="auto", target="en").translate(str(value))
            cleaned = clean_text(translated)
            reviews.at[idx, "Was_Translated"] = 1
            reviews.at[idx, "Translated_Text"] = cleaned
        else:
            cleaned = cleaned_original
            reviews.at[idx, "Was_Translated"] = 0
            reviews.at[idx, "Translated_Text"] = ""

    except Exception:
        cleaned = cleaned_original
        reviews.at[idx, "Was_Translated"] = 0
        reviews.at[idx, "Translated_Text"] = ""

    reviews.at[idx, "Review_Text"] = cleaned
    reviews.at[idx, "Sentiment_Polarity"] = analyzer.polarity_scores(cleaned)["compound"]

reviews.to_csv("data/dict/working_set/reviews.csv", index=False)