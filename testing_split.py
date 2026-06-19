import re

x = "higher"
#regex = r"(?:\d|[0-9])"
regex = r"^[\d]+?"
num_regex=r"[/^\d{1,6}$/]"
chars = r"[a-z]"
permissive_test = "agdd"
ssn_regex_bad = r"[/^\d{3}-\d{2}-\d{4}$/]"
ssn_regex_good = r'^[0-9]+-[0-9]+-[0-9]+$'
#letters + range1|range2
refined_test = r"[a-z]+[^/\[-\]/]|[/^/:-;/]"

positive_example = "d):this"
negative_example1 = "11(2):53–65"
negative_example2 = "ministry"

def regex_test(word):
    bracket_dash = r"/({\{-\}}/)"
    square_bracket_dash = r"[/\[-\]/]"
    colon = r"[/^/:-;/]"
    char = r"[A-Za-z]+"
    rules = [bracket_dash,square_bracket_dash,colon]
    passes = 0
    for rule in rules:
        if re.search(rule,word) and re.search(char,word):
            return True
            #passes = passes+1
    #if passes==3:
    #    return True
    return False

ssn = "126756453-42-4222"
#print(regex_test(positive_example))
#print(regex_test(negative_example))
#print(regex_test(permissive_test))
#pos/pos | pos/neg | neg/pos | neg/neg
another_regex = f"[s/\s+$//]"
another_test = " foo bar "
print(regex_test(positive_example))
print(regex_test(negative_example1))
print(regex_test(negative_example2))
print(regex_test(another_test))
#Must have letters in front! Numbers in front are often connected math expressions or indexes

