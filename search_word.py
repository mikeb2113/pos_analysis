from traverse_function import search_for_target_word, traverse
from sqlite_functions import search

def search_query(input_file="ClassOverlapping"):
    query = input("Please enter a query:\n")
    query_list = query.split(" ")
    for word in query_list:
        index = search_for_target_word(word,input_file)
        print("validation:")
        print(index)
        instances = traverse(input_file,index[0],index[1])
        for instance in instances:
            print(f"instance: {instance}")
            print(f"Sentence_id: {instance[2]}")
            print(f"bundle_id: {instance[4]}")
            print(f"file: {input_file}")
            search(input_file,instance[2],instance[4])

search_query()