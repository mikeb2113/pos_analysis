from extract_words_1_doc import extraction
import csv
from collections import defaultdict
import pandas as pd
from csir.pdf_extract import pdf_to_text
from csir.skeletons import Skeletons
from CBOW.prob_functions import synonym_resolution

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

    def display(self, level=0):
        print(f"Level {level}: {self.keys}")
        if not self.leaf:
            for child in self.children:
                #print(f"Level {level + 1}: {self.keys}")
                child.display(level + 1)


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def display(self):
        self.root.display()

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.append(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)  # Make space for the new key
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t - 1]
        x.children.insert(i + 1, z)


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
    print("sentences validation:")
    for element in y.sentences:
        print(element)
    synonoym_mapping = synonym_resolution(y.sentences,window_size)
    #for word in synonoym_mapping.dict:
    #    synonoym_mapping.percentage(word,window_size)
    return synonoym_mapping

def main():
    #text = pd.read_csv(file)
    #for i, (_, row1) in enumerate(text.iterrows(), start=1):

    dictionaries = []
    with open("paths.csv", mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        #extraction()
        for row in reader:
            print("file:")
            use_file = row[0] #"data/dict/working_set/traversable_text/" + row[0] + "_traversable.csv"#Output to the path as a CSV with connections present
            if use_file == "FitzgeraldTheGreatGastby":
                print(use_file)
                #extraction(use_file)
                #print(file_synonym_mapping(use_file).dict)
                dictionary = file_synonym_mapping(use_file,10)
                dictionaries.append(dictionary)
                print(f"Complete analysis for file: {row}")
    #        for entry in dictionary:
    #            print(f"word: {entry} stats: {dictionary[entry]}")
    original = dictionaries[0]
    max = len(dictionaries)
    active = 1
    window_size = 10
    print("dictionary constructed...")
    for word in original.dict:
        original.percentage(word,window_size)
    print("Calculated percent chances of word co-occurances")
    for entry in original.dict:
        print(f"word: {entry} stats: {original.dict[entry]}")

    print("beginning B-Tree...")

    B = BTree(3)
    #input = "The quick brown fox jumped over the lazy dog"
    keys = original.dict
    #keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for key in keys:
        B.insert(key)

    print("B-tree structure:")
    B.display()


if __name__ == '__main__':
    main()