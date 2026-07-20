from traverse_function import search_for_target_word, traverse
from sqlite_functions import search, initialize, get_word_count, traverse_db
from csir.word_data import Word
import os.path
import csv
from highlight_functions import highlight_by_text, return_quad

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
    query = keywords
    query_list = query.split(" ")
    instances_list = []
    for word in query_list:
        index = search_for_target_word(word,input_file)
        instances_complete = traverse(input_file,index[0],index[1])
        for instances in instances_complete:
                instances_list.append(search(input_file,instances[2],instances[4]))
    return instances_list
            
def ensure_file_exists(name):
    if not os.path.isfile(f'db_files/{name}.db'):
        initialize(name)

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
            if word not in DET and word not in PREP and word not in AUX and word not in MOD and word not in COMP and word not in CONJ:
                if remove_top_num == 0:
                    words.append(word)
                else:
                    remove_top_num = remove_top_num - 1
                if i > end_index: #Change trigger. Maybe: instead of naively taking the first 10: if there is too high of a word presence, remove the most common counted word?
                    return words
        #later: read the first 10 rows, discounting the and of in to etc. Do a search of the top 10 words. return sentences where these occur
        #consider simply skipping these words, going to the next rather than omitting entirely

def file_overview(input_file, remove_top_num = 0):
    instances = []
    keywords = overview_keywords(input_file,remove_top_num)
    if keywords:
        for word in keywords:
            if remove_top_num == 0:
                instances.append(search_query(word,input_file))
            else:
                remove_top_num = remove_top_num - 1
    return instances

def proceed_from_file(name, remove_top_num = 0):
    ensure_file_exists(name)
    sentence_builder = ""
    sentence_set = set()
    sentence_hash = {}
    num_set = set()
    word_theme_connections = file_overview(name,remove_top_num)
    for word_occurances in word_theme_connections:
        for sentence in word_occurances:
            sentence_num = 0
            for row in sentence:
                sentence_num = row[2]
                num_set.add(sentence_num)
                append = [row[3].replace("[",""),sentence_num]
                append[0] = append[0].replace("]","")
                append[0] = append[0].replace("\'","")
                sentence_builder = sentence_builder + append[0] + " "
                xmin = row[8]
                ymin = row[9]
                xmax = row[10]
                ymax = row[11]
                page = row[12]
                word = sentence_builder
            sentence_builder = sentence_builder[:-1]
            sentence_builder = sentence_builder + "."
            word_info = Word(row[8],row[9],row[10],row[11],page,sentence_builder)
            sentence_set.add(sentence_builder)

            sentence_hash[sentence_num] = word_info
            sentence_num = 0
            sentence_builder = ""
    return [sentence_hash,num_set]

def get_overall_relevent_sentences(file,remove_top_num = 0):
    reduced_length = 0
    relevant_sentences = []
    ensure_file_exists(file)
    full_word_length = get_word_count(file) #Get the total word count of the file
    hash_and_num_set = proceed_from_file(file,remove_top_num)#An object containing a hash of words and the sentence number they occur in
    sentence_hash = hash_and_num_set[0]#The hashset of sentences
    num_set = hash_and_num_set[1]#the set of numbers associated with a likely relevant sentence
    for num in num_set: #For each sentence id, access it's sentence
        relevant_sentences.append(sentence_hash[num])
        sent = sentence_hash[num].word.split(" ")
        reduced_length = reduced_length+len(sent) #Find the word count after removing likely irrelevant sentences
    remaining_words = full_word_length-reduced_length #The word count after removing likely irrelevant sentences
    remaining_words_ratio = remaining_words/full_word_length #Ratio of words that are in a likely relevant sentence
    if remaining_words_ratio < .25:
        remove_top_num = remove_top_num+1
        get_overall_relevent_sentences(file,remove_top_num)
    else:
        return [relevant_sentences,remaining_words_ratio]

def get_relevant_sentences_for_all_training_files():
    file_sentence_hash = {}
    with open("paths.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            use_file = row[0]
            sentences_and_ratio = get_overall_relevent_sentences(use_file)
            if not sentences_and_ratio:
                break
            sentences = sentences_and_ratio[0]
            ratio = sentences_and_ratio[1]
            file_sentence_hash[use_file] = sentences
    return file_sentence_hash

file_sentence_hash = get_relevant_sentences_for_all_training_files()
with open("paths.csv", mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        use_file = row[0]
        sentences = []
        try:
            sentences = file_sentence_hash[use_file]
            for sentence in sentences:
                text = sentence[5]
                dimensions = [sentence[0],sentence[1],sentence[2],sentence[3]]
                page = sentence[4]#input_word,page,input_doc,output_doc
                highlight_by_text(sentence,use_file)
        except KeyError:
            sentences = []