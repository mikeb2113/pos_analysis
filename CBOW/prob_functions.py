import sys
class probability_functions:
    def __init__(self):
        self.dict = {}
        self.word_set = set()

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

    def word_breakdown(self,text=""):
        text = """Since the components of CRISPR-Cas systems are derived from
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
        lem by modifying Cas9 protein or using Cas9 homologues [255]"""
        split = text.split(" ")
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

prob_dict = probability_functions()

context = prob_dict.word_breakdown()
length = len(context)
active = 0
while active < length:
    word = prob_dict.get_word(context,active)
    window = prob_dict.identify_window(context,10,active)
    prob_dict.aggregate_prob(window,word)
    active = active+1

for entry in prob_dict.dict:
    print(f"entry: {entry} probabilities: {prob_dict.dict[entry]}")