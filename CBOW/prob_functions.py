import sys
from numpy import argmax
class synonym_resolution:
    def __init__(self,text,window_size):
        self.dict = {}
        self.word_set = set()
        self.text = self.flatten_input(text)
        self.generate_probabilities(window_size)

    def sort(self):
        arr = []
        for word in self.dict:
            #print(word)
            arr.append(word)
        return arr

    def set_target_text(self,text):
        self.text = text

    def add_to_word_dict(self,context,target_word):
        local_dict = {}
        local_set = set()
        if target_word not in self.word_set:
            self.word_set.add(target_word)
            for idx,word in enumerate(context): 
                        if word not in local_set:
                            local_set.add(word)
                            local_dict[word] = 1
                        else:
                            local_dict[word] = local_dict[word]+1

        else:
            #print("word already in dict!")
            local_dict = self.dict[target_word]
            for idx,word in enumerate(context): 
                if word not in local_dict:
                    local_dict[word] = 1
                else:
                    local_dict[word] = local_dict[word]+1
        self.dict[target_word] = local_dict
            

    def aggregate_prob(self,context,target_word,dict={},window_size=10):
        self.add_to_word_dict(context,target_word)

    def word_breakdown(self):
        split = self.text.split(" ")
        context = []
        for word in split:
            if len(word) != 0:
                context.append(word)
        return context

    def get_word(self,context,index):
        return context[index]

    def onehot_to_word(self,idx):
        return self.int_to_word()[idx]

    def word_to_onehot(self,idx):
        return self.onehot_encoding[self.word_to_int()[idx]]
    
    def identify_window(self,context,window_size,index):
        words_goal = 2*window_size+1
        left = index-window_size
        right = index+window_size
        active_index = left
        word = ""
        window = []
        max = len(context)
        while active_index < right:
            if active_index == index:
                active_index+=1
                right = right+1
            if active_index >= max:
                return window
            if active_index >= 0:
                window.append(context[active_index])
            active_index+=1
        return window

    def percentage(self,word_entry,window):
        for word_key in self.dict:
            total_words = 0
            for target_word in self.dict[word_key]:
                total_words = total_words+self.dict[word_key][target_word]
            for target_word in self.dict[word_key]:
                self.dict[word_key][target_word] = self.dict[word_key][target_word]/total_words

    def get_encoding(self,word):
        number = self.word_to_int()[word]
        return number

    def word_to_int(self):
        return dict((word, i) for i, word in enumerate(self.dict))
    
    def int_to_word(self):
        return dict((i,word) for i, word in enumerate(self.dict))

    def onehot(self):
        length = len(self.dict)
        word_to_int = self.word_to_int()
        int_to_word = self.int_to_word()
        integer_encoded = [word_to_int[char] for char in self.dict]
        onehot_encoded = list()
        entries = []
        for word in self.dict:
            entries.append(word)
        for entry in integer_encoded:
            letter = [0 for _ in range(len(self.dict))] 
            letter[entry] = 1
            onehot_encoded.append(letter)
        inverted = int_to_word[argmax(onehot_encoded[0])]
        self.onehot_encoding = onehot_encoded

    def get_encoding(self,word):
        idx = self.word_to_int()[word]
        list = [0]*len(self.dict)
        list[idx] = 1
        return list

    def get_input_vector(self,word):
        input_vector = [0]*len(self.dict)
        for neighbor in self.dict[word]:
            encoding = self.word_to_int()[neighbor]#prob_dict.word_to_int()#get_encoding(word)
            #print("intermediate encoding:")
            #print(encoding)
            input_vector[encoding] = 1
        #This finds the desired input vector in predicting words of an input
        return input_vector

    def generate_probabilities(self,window_size):
        context = self.word_breakdown()
        length = len(context)
        active = 0

        while active < length:
            word = self.get_word(context,active)
            window = self.identify_window(context,window_size,active)
            self.aggregate_prob(window,word)
            active = active+1

    def jaccards(self,word1,word2):
        arr1 = self.get_input_vector(word1)
        arr2 = self.get_input_vector(word2)
        print(f"entry: {word1}")
        print(arr1)
        print(f"entry: {word2}")
        print(arr2)
        ones = 0 
        like_ones = 0
        for idx,number1 in enumerate(arr1):
            number2 = arr2[idx]
            if number1 == 1 or number2 == 1:
                if number1 == 1 and number2 == 1:
                    like_ones = like_ones+1
                ones = ones+1
        return like_ones/ones

    def flatten_input(self,array_of_words):
        flat = ""
        for word in array_of_words:
            flat = flat + word + " "
        return flat


#window_size = 5
#ex = ["Advances in Humanities Research Vol.12 Issue 6", "EWA Publishing", "Available Online: 10 September 2025", "DOI: 10.54254/2753-7080/2025.26572", "The Cold War: origins,causes, and global impacts", "Yixuan Bai", "Nanjing Jingling High School Hexi Campus, Nanjing, China", "646467343@qq.com", "Abstract.\xa0", "Republics between 1947 and 1991. After World War II, the US and the USSR became two poles of the world by virtue of their", "great strength, and they became opposed due to differences in ideology and geopolitics. Militarily, NATO confronts the Warsaw", "Pact and launches an arms race; Economically, the US implemented the Marshall Plan, and the USSR established the Economic", "and Mutual Association; There is also a fierce ideological confrontation. It profoundly affected the international landscape,", "economic development and cultural exchanges, and finally ended with the collapse of the USSR and the drastic changes in the", "Eastern Europe. As an important historical stage in the second half of the 20th century, the Cold War had an extremely far-", "reaching impact on the world.This article will introduce the basic concepts related to the Cold War, such as the historical", "background of the Cold War, the introduction of the two camps, the introduction of emphasis, the aspects of struggle, and the", "international political theories related to the Cold War. It also discuss the key events of the Cold War and discuss the impact of", "the Cold War and its implications for the present day from three periods: the pre-60s, the 70s, the 80s and beyond.", "Keywords:\xa0", "1. Introduction", "The Cold War originated from the Yalta Conference at the end of the Second World War. After the end of the Second World War,", "the United States(the US)and the Soviet Union(the USSR), as the most powerful countries, naturally formed opposition due to", "different ideologies. In 1946, former British Prime Minister Winston Churchill delivered his 'Iron Curtain Speech', marking the"]

#text = """Since the components of CRISPR-Cas systems are derived from bacteria, host immune response to Cas gene and Cas protein is regarded as one of the most important challenges in the clinical trials of CRISPR-Cas system [156,252]. It was found that in vivo delivery of CRISPR-Cas components can elicit immune responses against the Cas protein [252,253]. Furthermore, researchers also found that there were anti-Cas9 antibodies and anti-Cas9 T cells existing in healthy humans, suggesting the pre-existing of humoral and celluar immune responses to Cas9 protein in humans [254]. Therefore, how to detect and reduce the immunogenicity of Cas proteins is a major challenge will be faced in clinical application of CRISPR-Cas systems. Researchers are trying to handle this problem by modifying Cas9 protein or using Cas9 homologues [255]"""
#prob_dict = synonym_resolution(ex,window_size)

#for entry in prob_dict.dict:
#    prob_dict.percentage(entry,window_size)

#for entry in prob_dict.dict:
#    print(prob_dict.get_input_vector(entry))


#print(prob_dict.jaccards("US","NATO"))
