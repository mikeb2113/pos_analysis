from extract_words_1_doc import extraction
import csv
from collections import defaultdict
import pandas as pd
from csir.pdf_extract import pdf_to_text
from csir.skeletons import Skeletons
from CBOW.prob_functions import synonym_resolution

#text = pd.read_csv(file)
#for i, (_, row1) in enumerate(text.iterrows(), start=1):

def file_synonym_mapping(file,window_size):
    pdf_path = "pdfs/" + file + ".pdf"
    #pdf_transform = pdf_to_text(pdf_path)[0]
    #print(f"source -> {input_file} pdf: {pdf_transform}")
    #pdf = unstick_library_prefixes(pdf_to_text(pdf_path)[0])
    pdf_info = pdf_to_text(pdf_path)
    #print(f"validating pdf info: {pdf_info}")
    #print(pdf_info)
    pdf = pdf_info[0]
    page_count = pdf_info[2]
    #print(f"file: {input_file}")
    #print(f"page count: {pdf_info}")
    #print(f"referencing: {pdf_info[0][2]}")
    #print(f"page info: {pdf_info[0][2]}")

    output_file2 = "" #"data/dict/working_set/traversable_text/" + file + "_traversable.csv"#Output to the path as a CSV with connections present
    #y = Skeletons(pdf,output_file2,pdf_info)
    #print("VALIDATING COORDINATES:")
    #print(pdf_info[0][1])
    #print(f"sentences: {len(pdf_info)}")
    #print("VALIDATING PDF: ")
    ##print(pdf)
    #print("Info:")
    #print(pdf_info)
    #passes an array of sentences into skeletons
    y = Skeletons(pdf_info,output_file2,pdf_info[1],pdf_info[2],len(pdf_info),False)
    #print("Sentences validation:")
    #print(y.sentences)
    synonoym_mapping = synonym_resolution(y.sentences,window_size)
    for word in synonoym_mapping.dict:
        synonoym_mapping.percentage(word,window_size)
    return synonoym_mapping

with open("paths.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    #extraction()
    for row in reader:
        print("file:")
        use_file = row[0] #"data/dict/working_set/traversable_text/" + row[0] + "_traversable.csv"#Output to the path as a CSV with connections present
        print(use_file)
        #extraction(use_file)
        #print(file_synonym_mapping(use_file).dict)
        dictionary = file_synonym_mapping(use_file,10).dict
        for entry in dictionary:
            print(f"word: {entry} stats: {dictionary[entry]}")