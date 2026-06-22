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
            print("Word absent")
            return [-1,-1] #if the proposed location does not match the word, the word must not be present. Throw -1s to indicate this
        right = bisect.bisect_right(word_list,word)
        support = right - left
        return [left,support] #This returns an array. Index 0 shows the locaiton that the word was found at, if applicable
        #Index 1 shows the number of times that the word is present in the document
    else:
        print(len(index_list))
        print(len(word_list))

def traverse(document,mapping_location,ending_index):
    input = f"data/dict/working_set/mapped/{document}_mapped.csv"
    with open(input,'r') as file:
        rows = list(csv.reader(file))
        #row_info = rows[mapping_location+1]
        instances = []
        #print("Row:")
        #print(row_info)
        i = mapping_location+1
        ending_index=ending_index+mapping_location
        while i < ending_index+1:
            row_info = rows[i]
            instances.append(row_info)
            i = i+1
        #word = row_info[1]
        return instances
    
index = search_for_target_word("classifiers","ClassOverlapping")
print("validation:")
print(index)
input = "ClassOverlapping"
#mapping_index = 900
instances = traverse(input,index[0],index[1])
for instance in instances:
    print(instance[1])
#traverse(input,index[0])


#Need to be able to input starting location:
#This may look like [sentence_id],[location_in_sentence],[bundle_ids]]
#ex: ([73],[0],[0])
#This would lead into: ([73],[1],[0])
#Where itereating at the second index fails, you need to switch to itereation by the third index
#Where iterating at the third index fails, the sentence is over. Return a proposed starting location of ([74],[0],[0])