import pandas as pd


reviews = pd.read_csv('data/dict/intermediate_data/The_ Generative_AI_Ecosystem_50k_User_Reviews_2026.csv')

# Load the POS CSVs
df1 = pd.read_csv('data/dict/working_set/open_class/adjectives.csv')
df2 = pd.read_csv('data/dict/working_set/open_class/adverbs.csv')
df3 = pd.read_csv('data/dict/working_set/open_class/nouns.csv')
df4 = pd.read_csv('data/dict/working_set/open_class/expanded_verbs.csv')

#make seperate classes so that we have all of our data in the same place
class parts_of_speech:
    def __init__(self,adjs,advs,nouns,verbs):
        self.adjs = adjs
        self.advs = advs
        self.nouns = nouns
        self.verbs = verbs

class data:
    def __init__(self,reviews,pos):
        self.reviews = reviews
        self.pos = pos

#Before loading, drop the review columns that we don't need
try:
    reviews = reviews.drop('Thumbs_Up_Count', axis=1)
except KeyError:
    pass
try:
    reviews = reviews.drop('Review_Date', axis=1)
except KeyError:
    pass
try:
    reviews = reviews.drop('App_Version', axis=1)
except KeyError:
    pass
try:
    reviews = reviews.drop('Review_Theme', axis=1)
except KeyError:
    pass

pos=parts_of_speech(df1,df2,df3,df4)