from extract_words_1_doc import extraction
import csv
from collections import defaultdict
import pandas as pd

#text = pd.read_csv(file)
#for i, (_, row1) in enumerate(text.iterrows(), start=1):
with open("paths.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    #extraction()
    for row in reader:
        print("file:")
        use_file = row[0]
        print(use_file)
        extraction(use_file)
