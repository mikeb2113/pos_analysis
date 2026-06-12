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

def generate_mapping(file):
    trav = f"data/dict/working_set/traversable_text/{file}_traversable.csv"
    output = f"data/dict/working_set/mapped/{file}_mapped.csv"
    with open(output,"a",newline="") as file:
        header = ["word","sentence_id","location_in_sentence","bundle_id"]
        writer = csv.writer(file,escapechar='"')
        writer.writerow(header)
    #word,source,sentence_id,bundle_id
    #stats = f"data/dict/working_set/stats/{file}_stats.csv"

    df_trav = pd.read_csv(trav)
    #df_stats = pd.read_csv(stats)

    trav_dict = get_dict(df_trav)
    #stats_dict = get_dict(df_stats)
    with open(output,"a",newline="") as file:
        writer = csv.writer(file,escapechar='"')
        idx = 0
        for index,row in df_trav.iterrows():
            phrase = row[trav_dict.get("phrase")]
            cleaned = phrase.replace('[',"")
            cleaned = cleaned.replace(']',"")
            cleaned = cleaned.replace('\'',"")
            items = cleaned.split(", ")
            sent_id = row["sentence_id"]
            bund_id = row["bundle_id"]
            for item in items:
                if item != "":
                    newline = [item,sent_id,idx,bund_id]
                    writer.writerow(newline)
                    idx = idx+1
                    #print(f"{item}, {sent_id}, {bund_id}")
generate_mapping("ClassOverlapping")

#for index,row in df_stats.iterrows():
#    word = row[stats_dict.get("word")]
#    print(word)