from __future__ import with_statement
from scraper import csvable
from pathlib import Path
import csv
import os
import sys
import codecs
from pypdf import PdfReader
import pandas as pd

files = []
output = ""
file_mapping = {}
#print(test.sentences)
directory = Path('./pdfs')

#convert_to_utf8('your_file.txt')

for idx,file in enumerate(directory.iterdir()): #Go through each pdf, breaking them down by sentence
    if file.is_file():
        path = "./pdfs/"+file.name
        #print(f"path: {path}")
        pathing = path.split("/") #Break up the file path
        name = pathing[-1] #Take only the end of the path
        name_no_extension = name.split(".") #break ending into before and after the period
        name_no_extension = name_no_extension[0] #Take only the part before the period
        files.append(csvable(path,idx,name_no_extension)) #For each file found, break it down into sentences, saving pertinent data
        file_mapping[path] = (name_no_extension,f"pdfs_as_csvs/{name}.csv") #add to dictionary. 
        #Now, input will be the original file path.
        #It will write to pdfs_as_csvs, with the csv file taking the name of the original document

columns=[
    ["source"],
    ["text"],
    ["length"],
    ["char_length"],
    ["subject"],
    ["rating"],
    ["polarity"]
]
data = []
df = pd.DataFrame(columns=columns)

#for file in file_mapping:
#    print(file_mapping.get(file)[0])

#with open('./data/dict/working_set/pdfs_as_csvs/more_sources.csv','a',newline='') as file:
#    newrow = ["Text","Word_Count","Length_Chars","Sentiment_Polarity","Source","Source_Name","Subject","Star_Rating"]
#    writer = csv.writer(file,escapechar='"')
#    writer.writerow(newrow)

#for file in files:
#    for sentence in file.sentences:
#        out = "./pdfs_as_csvs/" + sentence.source_name + ".csv"
##        newrow = [sentence.text,sentence.word_count,sentence.length_chars,sentence.polarity,sentence.source,sentence.source_name,sentence.subject,sentence.star_rating]
#        if len(sentence.text)>0:
#            with open(out,'a',newline='') as file:
#                writer = csv.writer(file,escapechar='"')
#                writer.writerow(newrow)