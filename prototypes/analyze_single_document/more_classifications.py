import csv
import pandas as pd
#DET = {"the", "a", "an", "this", "that", "these", "those",}
DET = [
    ["the","det"],
       ["a", "det"],
       ["an", "det"],
       ["this", "det"],
       ["that", "det"],
       ["these", "det"],
       ["those","det"],
        ]
        

PREP = [
    ["of", "prep"],
    ["in", "prep"],
    ["on", "prep"],
    ["at", "prep"],
    ["over", "prep"],
    ["under", "prep"],
    ["with", "prep"],
    ["by", "prep"],
    ["for", "prep"],
    ["to", "prep"],
    ["from","prep"],
    ["into", "prep"],
    ["onto", "prep"],
    ["about", "prep"],
     ]

CONJ = [
    ["and","conj"],
    ["or", "conj"],
    ["but", "conj"],
]

COMP = [
    ["that", "comp"],
    ["which", "comp"],
    ["who", "comp"],
    ["whom", "comp"],
    ]

AUX = [
    ["be", "aux"],
    ["am", "aux"],
    ["is", "aux"],
    ["are", "aux"],
    ["was", "aux"],
    ["were", "aux"],
    ["been", "aux"],
    ["being", "aux"],
    ["have", "aux"],
    ["has", "aux"],
    ["had", "aux"],
    ["do", "aux"],
    ["does", "aux"],
    ["did", "aux"],
]

MOD = [
    ["can", "mod"],
    ["could","mod"],
    ["will", "mod"],
    ["would", "mod"],
    ["shall", "mod"],
    ["should", "mod"],
    ["may", "mod"],
    ["might", "mod"],
    ["must", "mod"],
    ]

#Montague Operand Identifiers:
EXISTENTIAL_DET = [
    ["a", "exst_det"],
    ["an", "exst_det"],
    ["some", "exst_det"],
    ["one", "exst_det"],          #  (often ∃)
    ["somebody", "exst_det"], 
    ["someone", "exst_det"],
    ["something", "exst_det"], 
    ["somewhere", "exst_det"],
    ["certain", "exst_det"], 
]

UNIVERSAL_DET = [
    ["every", "univ_det"],
    ["each","univ_det"],
    ["all","univ_det" ],
    ["any",  "univ_det"],
    ["whoever","univ_det"], 
    ["whatever", "univ_det"],
    ["whichever", "univ_det"],
    ["what","univ_det"], 
]

NEGATIVE_QUANT = [
    ["no", "neg_quant"],
    ["nobody", "neg_quant"],
    ["noone", "neg_quant"],
    ["no-one", "neg_quant"],
    ["none", "neg_quant"],
    ["nothing", "neg_quant"],
    ["not", "neg_quant"],
    ["nowhere", "neg_quant"],
    ["never", "neg_quant"],
]

PRONOUNS = [
  ["I", "pronoun"],
  ["you", "pronoun"],
  ["he", "pronoun"],
  ["she", "pronoun"],
  ["it", "pronoun"],
  ["we", "pronoun"],
  ["they", "pronoun"],
  ["me", "pronoun"],
  ["him", "pronoun"],
  ["her", "pronoun"],
  ["us", "pronoun"],
  ["them", "pronoun"],
  ["myself", "pronoun"],
  ["yourself", "pronoun"],
  ["yourselves", "pronoun"],
  ["herself", "pronoun"],
  ["himself", "pronoun"],
  ["itself", "pronoun"],
  ["ourselves", "pronoun"],
  ["themselves", "pronoun"],
  ["themself", "pronoun"],
  ["mine", "pronoun"],
  ["yours", "pronoun"],
  ["his", "pronoun"],
  ["hers", "pronoun"],
  ["ours", "pronoun"],
  ["theirs", "pronoun"],
  ["this", "pronoun"],
  ["that", "pronoun"],
  ["these", "pronoun"],
  ["those", "pronoun"],
  ["who", "pronoun"],
  ["whom", "pronoun"],
  ["whose", "pronoun"],
  ["which", "pronoun"],
  ["what", "pronoun"],
  ["someone", "pronoun"],
  ["somebody", "pronoun"],
  ["something", "pronoun"],
  ["anyone", "pronoun"],
  ["anybody", "pronoun"],
  ["anything", "pronoun"],
  ["no one", "pronoun"],
  ["nobody", "pronoun"],
  ["everyone", "pronoun"],
  ["everybody", "pronoun"],
  ["everything", "pronoun"],
  ["each", "pronoun"],
  ["either", "pronoun"],
  ["neither", "pronoun"],
  ["another", "pronoun"],
  ["other", "pronoun"],
  ["some", "pronoun"],
  ["many", "pronoun"],
  ["few", "pronoun"],
  ["all", "pronoun"],
  ["both", "pronoun"],
  ["none", "pronoun"],
  ["several", "pronoun"],
  ["any", "pronoun"],
  ["one", "pronoun"],
  ["each other", "pronoun"],
  ["one another", "pronoun"]
]

POSESSIVE_DET = [
    ["my","det"],
    ["your", "det"],
    ["his", "det"],
    ["her", "det"],
    ["its", "det"],
    ["our", "det"],
    ["their","det"],
    ["whose","det"]
    ]

df = pd.DataFrame(DET, columns=["word", "pos"])
df.to_csv("data/determiners.csv", index=False)

df = pd.DataFrame(PREP, columns=["word", "pos"])
df.to_csv("data/prepositions.csv", index=False)

df = pd.DataFrame(COMP, columns=["word", "pos"])
df.to_csv("data/compositions.csv", index=False)

df = pd.DataFrame(AUX, columns=["word", "pos"])
df.to_csv("data/auxiliary.csv", index=False)

df = pd.DataFrame(MOD, columns=["word", "pos"])
df.to_csv("data/modifiers.csv", index=False)

df = pd.DataFrame(EXISTENTIAL_DET, columns=["word", "pos"])
df.to_csv("data/existential_determiners.csv", index=False)

df = pd.DataFrame(UNIVERSAL_DET, columns=["word", "pos"])
df.to_csv("data/universal_determiners.csv", index=False)

df = pd.DataFrame(NEGATIVE_QUANT, columns=["word", "pos"])
df.to_csv("data/negative_quantifiers.csv", index=False)

df = pd.DataFrame(PRONOUNS, columns=["word", "pos"])
df.to_csv("data/pronouns.csv", index=False)

df = pd.DataFrame(POSESSIVE_DET, columns=["word", "pos"])
df.to_csv("data/posessive_det.csv", index=False)

dfconj = pd.read_csv("data/dict/intermediate_data/conjunctions-in-english.csv")#take the conj csv as input
#dfconj.rename(columns={"Word":"word"})
df = pd.DataFrame(dfconj, columns=["Word", "pos"]) #define a new df with the word pos pattern
df['pos'] = df['pos'].fillna("conj") #pos should be null - here, set the default fo conj
df.rename(columns={1:"Word"}, inplace=True)
df.rename({"Word": "word"}, axis=1, inplace=True)
df.to_csv("data/pos/directors/conjunctions.csv", index=False)