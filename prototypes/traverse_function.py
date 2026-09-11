import csv
import bisect

def search_for_target_word(word,document,index=-1,index_list=[]):
    if index<0:
        input = f"data/dict/working_set/mapped/{document}_mapped.csv"
        word_list = []
        with open(input,'r') as file:
            reader = csv.reader(file)
            next(reader)
            rows = list(reader)
        for row in rows:
            #print(row)
            #print(row[1])
            word_list.append(row[1])
        left = bisect.bisect_left(word_list,word) #These bisects find the location that a given word would be inserted, if applicable
        if word_list[left]!=word:
            #print("Word absent")
            return [-1,-1] #if the proposed location does not match the word, the word must not be present. Throw -1s to indicate this
        right = bisect.bisect_right(word_list,word)
        support = right - left
        return [left,support] #This returns an array. Index 0 shows the locaiton that the word was found at, if applicable
        #Index 1 shows the number of times that the word is present in the document
    else:
        print(len(index_list))
        print(len(word_list))

def traverse(document,mapping_location,ending_index):
    #return each row in the mapped file where a given word occurs
    input = f"data/dict/working_set/mapped/{document}_mapped.csv"
    with open(input,'r') as file:
        rows = list(csv.reader(file)) #read the file
        instances = []#Where relevant row information will be saved
        i = mapping_location+1#+1 to account for the header - the first instance of the input word
        ending_index=ending_index+mapping_location#Add the total occurances to the starting index. This gives the last instance of the word
        while i < ending_index+1: #iterate up to the last instance
            row_info = rows[i] #Take the occurant row
            instances.append(row_info) #Add it to instances
            i = i+1 #iterate
        return instances #Return each row from mapped where the word occurs :D (Assuming the pdf split properly - no split/combined instances)
    
#This will print each row in the mapping that contains the specified word
#This will appear in the form: (mapped_id,word,sentence_id,location_in_sentence,bundle_id)
#So we can bring this back to the traverable by looking at indexes 1 and 4 in the traversable and 2 and 4 in mapped. so (trav1)->(map2) and (trav4)->(map4)
#These, respectively, are: sentence_id and bundle_id. We don't look at the individual word, but at the word's surroundings
#With this, words may be analyzed less granularly than a word-by-word approach, which should preserve the original context better

#The next step would be to change the csvs to a database file, and join where trav1=map2 and trav4=map4



#So from the mapped, look only at indexes 2 and 4 to connect it to the traversable
