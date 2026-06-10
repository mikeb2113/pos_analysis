import pandas as pd
from langdetect import detect_langs, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import unicodedata
from pathlib import Path
from aggregate import file_mapping, files
import csv
import re
#This takes a long time to complete! Rest assured it is not broken. You might want to do something else as this works!
print("=====CLEAN_DATA=====")
DetectorFactory.seed = 0
paths = []
#with open('paths.csv','a',newline='') as file:
#    newrow = ["path"]
#    writer = csv.writer(file,escapechar='"')
#    writer.writerow(newrow)
def clean_text(text):
    if pd.isna(text):
        return ""

    text = unicodedata.normalize("NFKD", str(text))
    text = text.encode("ascii", "ignore").decode("ascii")
    return text

def is_number(input_string):
    regex_string=r'^\d+$'
    temp=re.sub(r"\s","",input_string)
    #print(temp)
    if re.match(regex_string,temp):
        return True
    else:
        return False
    
def is_empty(input_string):
    regex_string=r'^$'
    if re.match(regex_string,input_string):
        return True
    else:
        return False

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
    header = ["Original_Text","Word_Count","Char_Count","Sentiment_Polarity","Translated_Text","Source_Id","Source_Name"]
    rows = []
    for sentence in file.sentences:
        #print(sentence.text)
        if(is_number(sentence.text)) or is_empty(sentence.text):
             continue
        else:
            path = file_mapping.get(file)
            #print(f"Source: {file.source_name}")
            path = "data/dict/working_set/pdfs_as_csvs/" + file.source_name + ".csv" #Output to this address as a csv
            # preserve original text
            #sentence.text #Save the original text in case of a translation being required
            paths.append([path,file.source_name])
            paths_file = "paths.csv"
            #for idx, value in sentence.text.items():#attempt to translate each sentence
            status, confidence = detect_language_status(sentence.text) #Attempt to translate to see if english & confidence

            #Then, save all the aggregated data into a row.
            cleaned_original = clean_text(sentence.text)

            try:
                    # SAFER: only translate when confidently non-English
                if status == "confident_non_english":
                        translated = GoogleTranslator(source="auto", target="en").translate(str(sentence.text))
                        cleaned = clean_text(translated)
                        row = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.text,sentence.source,sentence.source_name,status,confidence,1,cleaned]
                else:
                        cleaned = cleaned_original
                        row = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.text,sentence.source,sentence.source_name,status,confidence,0,cleaned]

            except Exception:
                    cleaned = cleaned_original
                    row = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.text,sentence.source,sentence.source_name,status,confidence,0,""]
            rows.append(row)
            #print("row(clean_data):")
            #print(row)
            with open(path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile,escapechar="\\")
                writer.writerow(header)
                for row in rows:
                    writer.writerow(row)
#for path in paths:
#     print(f"path: {path}")
#path: data/dict/working_set/pdfs_as_csvs/CRISPR_paper.csv
#path: data/dict/working_set/pdfs_as_csvs/CRISPR_paper.csv
#path: data/dict/working_set/pdfs_as_csvs/CRISPR_paper.csv
pathing = set()
for path in paths:
    pathing.add(path[1])
print("End result (pathing):")
print(pathing)
print("Looping test:")
for path in pathing:
    print(path)
columns = ["path"]
df = pd.DataFrame(pathing,columns=columns)
df.to_csv("paths.csv",index=False)
#with open(paths_file, "a", newline="") as csvfile:
#    writer = csv.writer(csvfile,escapechar="\\")
#    for path in pathing:
#        writer.writerow(path)
print("=====END OF CLEAN_DATA=====")
