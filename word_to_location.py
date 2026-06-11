import csv
import pandas as pd
import numpy as np

def get_dict(dataframe):
    mapping = []
    dictionary = {}
    for idx,column in enumerate(dataframe):
        mapping.append([idx,column])

    for idx,item in enumerate(mapping):
        dictionary.setdefault(mapping[idx][1],mapping[idx][0])#access the first and second values of array at idx
    #Dictionary can now be used to automatically get the index of a given column!
    return dictionary

trav = "data/dict/working_set/traversable_text/ClassOverlapping_traversable.csv"
stats = "data/dict/working_set/stats/ClassOverlapping_stats.csv"

df_trav = pd.read_csv(trav)
df_stats = pd.read_csv(stats)

trav_dict = get_dict(df_trav)
stats_dict = get_dict(df_stats)

for index,row in df_trav.iterrows():
    phrase = row[trav_dict.get("phrase")]
    cleaned = phrase.replace('[',"")
    cleaned = cleaned.replace(']',"")
    cleaned = cleaned.replace('\'',"")
    #cleaned = cleaned.replace(', ',"\n")
    sent_id = row["sentence_id"]
    bund_id = row["bundle_id"]
    if cleaned != "":
        print(f"{cleaned}, {sent_id}, {bund_id}")

for index,row in df_stats.iterrows():
    word = row[stats_dict.get("word")]
    print(word)