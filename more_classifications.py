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
  ['I', "pronoun"],
  ['you', "pronoun"],
  ['my', "pronoun"],
  ['mine', "pronoun"],
  ['myself', "pronoun"],
  ['we', "pronoun"],
  ['us', "pronoun"],
  ['our', "pronoun"],
  ['ours', "pronoun"],
  ['ourselves', "pronoun"],
  ['you', "pronoun"],
  ['you', "pronoun"],
  ['your', "pronoun"],
  ['yours', "pronoun"],
  ['yourself', "pronoun"],
  ['you', "pronoun"],
  ['you', "pronoun"],
  ['your', "pronoun"],
  ['your', "pronoun"],
  ['yourselves', "pronoun"],
  ['he', "pronoun"],
  ['him', "pronoun"],
  ['his', "pronoun"],
  ['his', "pronoun"],
  ['himself', "pronoun"],
  ['she', "pronoun"],
  ['her', "pronoun"],
  ['her', "pronoun"],
  ['her', "pronoun"],
  ['herself', "pronoun"],
  ['it', "pronoun"],
  ['it', "pronoun"],
  ['its', "pronoun"],
  ['itself', "pronoun"],
  ['they', "pronoun"],
  ['them', "pronoun"],
  ['their', "pronoun"],
  ['theirs', "pronoun"],
  ['themself', "pronoun"],
  ['they', "pronoun"],
  ['them', "pronoun"],
  ['their', "pronoun"],
  ['theirs', "pronoun"],
  ['themselves', "pronoun"],
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

df = pd.DataFrame(CONJ, columns=["word", "pos"])
df.to_csv("data/conjunctions.csv", index=False)

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