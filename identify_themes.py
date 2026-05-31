from extract_words import pathing
import pandas as pd
import numpy as np

first_split = { #These 3 words should be present in the 10 most common words of any document which uses conventional english, but does not contain many mathematical expressions
    "the" : 0,
    "The" : 0,
    "and" : 1,
    "And" : 1,
    "Of" : 2,
    "of" : 2
}

second_split = {
    "to" : 0,
    "To" : 0
}

ignore = { #These words frequently appear, but not commonly enough to say they MUST appear. We ignore these
    "in" : 0,
    "In" : 0,
    "a" : 1,
    "A" : 1,
    "is" : 2,
    "Is" : 2,
    "to" : 3,
    "To" : 3
}

classifications = { #A text may be english, or some code/math document
    "English" : 0,
    "Representational_Logic" : 1
}

representational_logic_subclassifications = {#These are various types of math/code documents
    "Document" : 0, #This refers to analytical reports - liekly contains a mix of representational logic and english 
    "Code" : 1, #Refers to misclanious encoding systems that may not incude english. May be binary files hex, etc
    "Program" : 2, #Refers to software code. Will be mostly english, but not in the same patterend way as standard
}

for path in pathing: #Iterate through each document
    words = set() #A set of the common words in the document
    themes = "" #Stores the detected overarching themes of a document
    participation = 0 #The # of words in the top 10 frequent words that are present in the first split
    input_file = "data/dict/working_set/stats_with_features" + path + ".csv"
    df = pd.read_csv(input_file) #Read the input file
    head = df.head(11) #Take the top 10 rows of the input file
    print(f"head:")
    print(head)
    for i, (_, row) in enumerate(head.iterrows(), start=1):
        print("target:")
        #print(row) #Iterating through row gives the colum info of the word...?
        print(_)
        words.add(row["word"]) #Add the individual word to the words array
    for word in words: #Iterate through the top 10 words
        print(f"path: {path}")
        #print(f"row: {_["word"]}")
        print(f"words: {words}")
        print(f"word: {word}")
        if word in first_split:
            participation = participation+1 #Count how many words participate in first split
        if word not in ignore and word not in first_split:
            themes += word + ", " #If word is not to be ignored, track it as an overarching theme
    if participation >= 3: #Passes the first pass test - is likely a standard english document
        print("English!")
    if participation<= 1: #Likely not a standard english document - may contain representational logic which skews results
        print("Representational_Logic!")
    if themes != "":
        themes = themes[:-2] #Remove the trailing ", " from the themes list
    df['overarcing_theme'] = themes #Add the themes to the dataframe 
    df.to_csv(input_file, index=False) #Output to the dataframe