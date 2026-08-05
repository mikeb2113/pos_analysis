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
#xmin,ymin,xmax,ymax
for file in files:#go to the original files: take each file individually
    header = ["Original_Text","Word_Count","Char_Count","Sentiment_Polarity","Translated_Text","Source_Id","Source_Name","xmin","ymin","xmax","ymax","Page","Total_Sentences"]
    rows = []
    print('ENTIRE SENTENCES TEST:')
    print(file.sentences)
    for i,sentence in enumerate(file.sentences):
        #print(f"sentence: {sentence.text}")
        #for i,data in enumerate(sentence.text):
        #print(f"text: {sentence.text[0][i]}")
        #print(f"xmin: {sentence.text[1][i][0]}")
        #print(f"ymin: {sentence.text[1][i][1]}")
        #print(f"xmax: {sentence.text[1][i][2]}")
        #print(f"ymax: {sentence.text[1][i][3]}")
        #print(f"Page: {sentence.text[2][i]}")
        #print(f"File: {file.source_name} Sentences length: {len(sentence.text[0])}")
        #print(f"length measure 2: {len(sentence.text[2])}")
        #print(sentence.text[0][0])
        #print(f"Validating sentence: {sentence.text[0][0]}")
        if is_number(sentence.text) or is_empty(sentence.text):
             print("continuing...")
             continue
        else:
            path = file_mapping.get(file)
            #print(f"Source: {file.source_name}")
            path = "data/dict/working_set/pdfs_as_csvs/" + file.source_name + ".csv" #Output to this address as a csv
            # preserve original text
            #sentence.text[0][0] #Save the original text in case of a translation being required
            paths.append([path,file.source_name])
            paths_file = "paths.csv"
            #for idx, value in sentence.text[0][0].items():#attempt to translate each sentence
            status, confidence = detect_language_status(sentence.text) #Attempt to translate to see if english & confidence
            #Then, save all the aggregated data into a row.
            cleaned_original = clean_text(sentence.text)
            cleaned = cleaned_original
            print("sentence:")
            print(sentence)
            print("sentence.text:")
            print(sentence.text)
            print("sentence.word_count:")
            print(sentence.word_count)
            print("sentence.length_chars:")
            print(sentence.length_chars)
            print("sentence.polarity:")
            print(sentence.polarity)
            print("sentence.text:")
            print(sentence.text)
            print("sentence.source:")
            print(sentence.source)
            print("sentence.source_name")
            print(sentence.source_name)
            print("status")
            print(status)
            print("confidenice")
            print(confidence)
            print("cleande")
            print(cleaned)
            print("xmin")
            print(sentence.xmin)
            print("ymin")
            print(sentence.ymin)
            print("xmax")
            print(sentence.xmax)
            print("ymax")
            print(sentence.ymax)
            print("page")
            print(sentence.page)
            print("sentence.total_sentences")
            print(sentence.total_sentences)
#"Original_Text","Word_Count","Char_Count","Sentiment_Polarity","Translated_Text","Source_Id","Source_Name","xmin","ymin","xmax","ymax","Page","Total_Sentences"]


            try:

                    # SAFER: only translate when confidently non-English
                #print(f"xmin: {sentence.text[1][0][0]}")
                #print(f"ymin: {sentence.text[1][0][1]}")
                #print(f"xmax: {sentence.text[1][0][2]}")
                #print(f"ymax: {sentence.text[1][0][3]}")
                #print(f"Page: {sentence.text[2][0]}")
                if status == "confident_non_english":
                        #translated = GoogleTranslator(source="auto", target="en").translate(str(sentence.text[0][0]))
                        #cleaned = clean_text(translated)
                        row = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.text,sentence.source,sentence.source_name,status,confidence,1,cleaned,sentence.xmin,sentence.ymin,sentence.xmax,sentence.ymax,sentence.page,sentence.total_sentences]
                else:
                        #cleaned = cleaned_original
                        row = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.text,sentence.source,sentence.source_name,status,confidence,0,cleaned,sentence.xmin,sentence.ymin,sentence.xmax,sentence.ymax,sentence.page,sentence.total_sentences]

            except Exception:
                    print("exception :(")
                    cleaned = cleaned_original
                    #print("validation:")
                    #print(status)
                    #print(confidence)
                    #print(sentence.text[1][i][0])
                    #print(sentence.text[1][i][1])
                    #print(sentence.text[1][i][2])
                    #print(sentence.text[1][i][3])
                    #print(sentence.text[2][i])
                    #print(sentence.total_sentences)
                    row = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.text,sentence.source,sentence.source_name,status,confidence,0,"",sentence.xmin,sentence.ymin,sentence.xmax,sentence.ymax,sentence.page,sentence.total_sentences]
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
