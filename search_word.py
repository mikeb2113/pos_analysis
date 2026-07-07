from traverse_function import search_for_target_word, traverse
from sqlite_functions import search, initialize, get_word_count, traverse_db
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
        #print(f"complete: {instances_complete}")
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
            
def overview_keywords(input_file,remove_top_num = 0):
    file = open(f"data/dict/working_set/stats_with_features/stats_with_features_{input_file}.csv")
    words = []
    end_index = 10
    reader = csv.reader(file)
    next(reader)
    with open(f"data/dict/working_set/stats_with_features/stats_with_features_{input_file}.csv",'r') as file:
        for i,row in enumerate(reader):
            word = row[0]
            take = row[22]
            #print(f"word search: {word}")
            if word not in DET and word not in PREP and word not in AUX and word not in MOD and word not in COMP and word not in CONJ:
                #print(word)
                if remove_top_num == 0:
                    words.append(word)
                else:
                    remove_top_num = remove_top_num - 1
                #print(f"full row: {row}")
                if i > end_index: #Change trigger. Maybe: instead of naively taking the first 10: if there is too high of a word presence, remove the most common counted word?
                    print("words:")
                    for word in words:
                        print(word)
                    return words
        #later: read the first 10 rows, discounting the and of in to etc. Do a search of the top 10 words. return sentences where these occur
        #consider simply skipping these words, going to the next rather than omitting entirely

def file_overview(input_file, remove_top_num = 0):
    instances = []
    keywords = overview_keywords(input_file,remove_top_num)
    if keywords:
        #print(f"====={input_file} OVERVIEW=====")
        for word in keywords:
            if remove_top_num == 0:
                instances.append(search_query(word,input_file))
            else:
                remove_top_num = remove_top_num - 1
        #print(f"====={input_file} OVERVIEW END=====")
    return instances

def proceed_from_file(name, remove_top_num = 0):
    #name = "ClassOverlapping"
    if not os.path.isfile(f'db_files/{name}.db'):
        initialize(name)
    #print(f"overview: {file_overview(name)}")
    #print(file_overview(name))
    sentence_builder = ""
    sentence_set = set()
    sentence_hash = {}
    num_set = set()
    word_theme_connections = file_overview(name,remove_top_num)
    for word_occurances in word_theme_connections:
        #print(f"instance: {word_occurances}")
        #print("sentences:")
        for sentence in word_occurances:
            #print(sentence)
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
            #print()
            #print(f"sentence: {sentence}")
    #for sentence in sentence_set:
    #    print(sentence)

    #for word in sentences:
    #    print(word)
    #print(file_overview(name))
    #search_query("classification",name)
    #print("traversing...")
    return [sentence_hash,num_set]
    #traverse_db(name)

def get_overall_relevent_sentences(file,remove_top_num = 0):
#    with open("paths.csv", mode='r', encoding='utf-8') as file:
#        reader = csv.reader(file)
#        next(reader)
#        for row in reader:
#            #print("file:")
#            use_file = row[0]
    reduced_length = 0
    relevant_sentences = []
    full_word_length = get_word_count(file) #Get the total word count of the file
    #print(f"file: {file}")
    hash_and_num_set = proceed_from_file(file,remove_top_num)#An object containing a hash of words and the sentence number they occur in
    sentence_hash = hash_and_num_set[0]#The hashset of sentences
    num_set = hash_and_num_set[1]#the set of numbers associated with a likely relevant sentence
    for num in num_set: #For each sentence id, access it's sentence
        relevant_sentences.append(sentence_hash[num])
        sent = sentence_hash[num].split(" ")
            #print(sentence_hash[num])
            #print(len(sent))
        reduced_length = reduced_length+len(sent) #Find the word count after removing likely irrelevant sentences
    remaining_words = full_word_length-reduced_length #The word count after removing likely irrelevant sentences
    remaining_words_ratio = remaining_words/full_word_length #Ratio of words that are in a likely relevant sentence
    #print(f"full words: {full_word_length}")
    #print(f"reduced word length: {reduced_length}")
    #print(f"remaining words: {remaining_words}")
    #print(f"remaining words ratio: {remaining_words_ratio}")
    if remaining_words_ratio < .25:
        remove_top_num = remove_top_num+1
        get_overall_relevent_sentences(file,remove_top_num)
    if not relevant_sentences:
        print("There are no relevant sentences!")
    else:
        return [relevant_sentences,remaining_words_ratio]
        #print(sentence_hash[num])
#print(get_word_count("Constantinople"))

def get_relevant_sentences_for_all_training_files():
    file_sentence_hash = {}
    with open("paths.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            use_file = row[0]
            print(f"evaluating file: {use_file}")
            sentences_and_ratio = get_overall_relevent_sentences(use_file)
            print("==========sentences and ratio test==========")
            print(sentences_and_ratio)
            print("==========end of sentences and ratio test==========")
            print("==========sentences test==========")
            print(sentences_and_ratio[0])
            print("==========end of sentence test==========")
            sentences = sentences_and_ratio[0]
            ratio = sentences_and_ratio[1]
            file_sentence_hash[use_file] = sentences
            print(f"ratio: {ratio}")
    return file_sentence_hash

file_sentence_hash = get_relevant_sentences_for_all_training_files()
with open("paths.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        print(f"Accessing file: {row[0]}")
        use_file = row[0]
        for sentence in file_sentence_hash[use_file]:
            print(sentence)