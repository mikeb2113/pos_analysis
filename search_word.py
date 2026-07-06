from traverse_function import search_for_target_word, traverse
from sqlite_functions import search, initialize, traverse_db
import os.path
import csv

#def create_table(input_file):

DET = {"the", "a", "an", "this", "that", "these", "those",}

PREP = {"of", "in", "on", "at", "over", "under", "with", "by", "for", "to", "from", "into", "onto"}

CONJ = {"and", "or", "but"}

COMP = {"that", "which", "who", "whom"}

MOD = {"can", "could", "will", "would", "shall", "should", "may", "might", "must"}

AUX = {"be", "am", "is", "are", "was", "were", "been", "being",
        "have", "has", "had",
        "do", "does", "did"}

#Montague Operand Identifiers:
EXISTENTIAL_DET = {
    "a", "an",
    "some",
    "one",          # as in "one student" (often ∃)
    "somebody", "someone", "something", "somewhere",
    "certain"     # multiword, but you can detect "a" + "certain"
}

UNIVERSAL_DET = {
    "every", "each",
    "all", 
    "any",       # context-sensitive; treated as universal in generic contexts
    "whoever", "whatever", "whichever"  # “free-choice” style universals
}

NEGATIVE_QUANT = {
    "no",
    "nobody", "noone", "no-one", "none",
    "nothing",
    "nowhere",
    "never"  # temporal but still a negative quantificational flavor
}

def search_query(keywords,input_file="ClassOverlapping"):
    query = keywords#input("Please enter a query:\n")
    query_list = query.split(" ")
    #print(f"word: {keywords}")
    instances_list = []
    for word in query_list:
        index = search_for_target_word(word,input_file)
        #print("validation:")
        #print(index)
        instances_complete = traverse(input_file,index[0],index[1])
        print(f"complete: {instances_complete}")
        for instances in instances_complete:
            #for instance in instances:
                #print(f"instance: {instances}")
                #print(f"Sentence_id: {instances[2]}")
                #print(f"bundle_id: {instances[4]}")
                #print(f"file: {input_file}")
                #search(input_file,instances[2],instances[4])
                #print()
                #print(f"return: {search(input_file,instances[2],instances[4])}")
                instances_list.append(search(input_file,instances[2],instances[4]))
    return instances_list
            
def overview_keywords(input_file):
    file = open(f"data/dict/working_set/stats_with_features/stats_with_features_{input_file}.csv")
    words = []
    reader = csv.reader(file)
    next(reader)
    with open(f"data/dict/working_set/stats_with_features/stats_with_features_{input_file}.csv",'r') as file:
        for i,row in enumerate(reader):
            word = row[0]
            #print(f"word search: {word}")
            if word not in DET and word not in PREP and word not in AUX and word not in MOD and word not in COMP and word not in CONJ:
                print(word)
                words.append(word)
                if i > 10:
                    return words
        #later: read the first 10 rows, discounting the and of in to etc. Do a search of the top 10 words. return sentences where these occur
        #consider simply skipping these words, going to the next rather than omitting entirely

def file_overview(input_file):
    instances = []
    keywords = overview_keywords(input_file)
    if keywords:
        #print(f"====={input_file} OVERVIEW=====")
        for word in keywords:
            instances.append(search_query(word,input_file))
        #print(f"====={input_file} OVERVIEW END=====")
    return instances

def proceed_from_file(name):
    #name = "ClassOverlapping"
    if not os.path.isfile(f'db_files/{name}.db'):
        initialize(name)
    print(f"overview: {file_overview(name)}")
    #print(file_overview(name))
    sentence_builder = ""
    sentence_set = set()
    sentence_hash = {}
    num_set = set()
    word_theme_connections = file_overview(name)
    for word_occurances in word_theme_connections:
        print(f"instance: {word_occurances}")
        print("sentences:")
        for sentence in word_occurances:
            print(sentence)
            sentence_num = 0
            for row in sentence:
                sentence_num = row[2]
                num_set.add(sentence_num)
                append = [row[3].replace("[",""),sentence_num]
                append[0] = append[0].replace("]","")
                append[0] = append[0].replace("\'","")
                sentence_builder = sentence_builder + append[0] + " "
                #print(row[3])
                #sentences.append(row[3])
            sentence_builder = sentence_builder[:-1]
            sentence_builder = sentence_builder + "."
            sentence_set.add(sentence_builder)
            sentence_hash[sentence_num] = sentence_builder
            sentence_num = 0
            sentence_builder = ""
            print()
            #print(f"sentence: {sentence}")
    print("set:")

    for num in num_set:
        print(sentence_hash[num])
    #for sentence in sentence_set:
    #    print(sentence)

    #for word in sentences:
    #    print(word)
    #print(file_overview(name))
    #search_query("classification",name)
    print("traversing...")
    #traverse_db(name)

with open("paths.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    #extraction()
    for row in reader:
        print("file:")
        use_file = row[0]
        proceed_from_file(use_file)