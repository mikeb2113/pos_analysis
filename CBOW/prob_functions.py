import sys
from numpy import argmax
class probability_functions:
    def __init__(self,text):
        self.dict = {}
        self.word_set = set()
        self.text = text
        self.onehot_encoding = list()

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
            print("word already in dict!")
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
        #length = len(self.dict[word_entry])
        #print(f"length: {length}")
        for word_key in self.dict:
            total_words = 0
            for target_word in self.dict[word_key]:
                total_words = total_words+self.dict[word_key][target_word]
                #print("word_key:")
                #print(self.dict[word_key])
                #print("target word:")
                #print(self.dict[word_key])
                #print(f"{word_key} total word count: {total_words}")
            for target_word in self.dict[word_key]:
                self.dict[word_key][target_word] = self.dict[word_key][target_word]/total_words
            #print(self.dict[word_entry][word])
    
    def word_to_int(self):
        return dict((word, i) for i, word in enumerate(self.dict))
    
    def int_to_word(self):
        return dict((i,word) for i, word in enumerate(self.dict))

        #char_to_int = dict((c, i) for i, c in enumerate(self.dict))
        #int_to_char = dict((i, c) for i, c in enumerate(self.dict))
    def onehot(self):
        # define input string
        #data = 'hello world'
        #print(data)
        # define universe of possible input values
        #alphabet = 'abcdefghijklmnopqrstuvwxyz '
        # define a mapping of chars to integers
        length = len(self.dict)
        word_to_int = self.word_to_int()#dict((c, i) for i, c in enumerate(self.dict))
        int_to_word = self.int_to_word()#dict((i, c) for i, c in enumerate(self.dict))
        #print("word to int:")
        #print(char_to_int)
        #print("int to word:")
        #print(int_to_char)
        # integer encode input data
        integer_encoded = [word_to_int[char] for char in self.dict]
        #print(integer_encoded)
        # one hot encode
        onehot_encoded = list()
        #for entry in 
        entries = []
        for word in self.dict:
            entries.append(word)
        for entry in integer_encoded:
            letter = [0 for _ in range(len(self.dict))] 
            #print("entries:")
            #print(entries)
            #letter = [0 for _ in range(len(entries))]
            #print("entry:")
            #print(entry)
            letter[entry] = 1
            onehot_encoded.append(letter)
        #print(onehot_encoded)
        # invert encoding
        inverted = int_to_word[argmax(onehot_encoded[0])]
        #print(inverted)
        self.onehot_encoding = onehot_encoded



text = """
        Since the components of CRISPR-Cas systems are derived from
        bacteria, host immune response to Cas gene and Cas protein is
        regarded as one of the most important challenges in the clinical tri-
        als of CRISPR-Cas system [156,252]. It was found that in vivo deliv-
        ery of CRISPR-Cas components can elicit immune responses against
        the Cas protein [252,253]. Furthermore, researchers also found that
        there were anti-Cas9 antibodies and anti-Cas9 T cells existing in
        healthy humans, suggesting the pre-existing of humoral and cel-
        luar immune responses to Cas9 protein in humans [254]. There-
        fore, how to detect and reduce the immunogenicity of Cas
        proteins is a major challenge will be faced in clinical application
        of CRISPR-Cas systems. Researchers are trying to handle this prob-
        lem by modifying Cas9 protein or using Cas9 homologues [255]
        """
prob_dict = probability_functions(text)
window_size = 2
context = prob_dict.word_breakdown()
length = len(context)
active = 0

while active < length:
    word = prob_dict.get_word(context,active)
    window = prob_dict.identify_window(context,window_size,active)
    prob_dict.aggregate_prob(window,word)
    active = active+1

for entry in prob_dict.dict:
    prob_dict.percentage(entry,window_size)
    #print(f"entry: {entry} probabilities: {prob_dict.dict[entry]}")
    #print()
prob_dict.onehot()
#print(prob_dict.onehot_encoding)
for encoding in prob_dict.onehot_encoding:
    print(encoding)
    print()
#print(prob_dict.int_to_word)

#encodings = prob_dict.onehot()

#onehot_encodings = prob_dict.onehot()

#prob_dict.percentage("Since")