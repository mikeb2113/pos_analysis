import re

string = " 776"
reg_string=r'^\d+$'
def reg(input_string):
    regex_string=r'^\d+$'
    temp=re.sub(r"\s","",input_string)
    print(temp)
    if re.match(regex_string,temp):
        print("match!")
    else:
        print("no match!")

reg(string,reg_string)