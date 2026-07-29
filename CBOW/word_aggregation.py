def aggregate_prob(target_word="who",window =["partner","abroad","who","can","accommodate"],window_size=10):
    word_count = len(window) #Get the word count
    window.remove(window[int(word_count/2)]) #Remove the center of the window - this should be the input word
    prob_dict = {}
    word_set = set()
    #print(word_count)

    for word in window:
        if word not in word_set:
            word_set.add(word)
            prob_dict[word] = 1/word_count
        else:
            prob_dict[word] = prob_dict[word]+1
    return prob_dict
        #print(word)
        #if word not in prob_dict:
        #    prob_dict[word] = 
print(aggregate_prob())