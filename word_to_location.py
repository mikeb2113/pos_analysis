import csv
import pandas as pd
import numpy as np
import bisect
from itertools import islice

DET = {"the", "a", "an", "this", "that", "these", "those",}

PREP = {"of", "in", "on", "at", "over", "under", "with", "by", "for", "to", "from", "into", "onto"}

CONJ = {"and", "or", "but"}

COMP = {"that", "which", "who", "whom"}

MOD = {"can", "could", "will", "would", "shall", "should", "may", "might", "must"}

AUX = {"be", "am", "is", "are", "was", "were", "been", "being",
            "have", "has", "had",
            "do", "does", "did"}

    #Montague Operand Identifiers:
EXISTENTIAL_DET = {
        "a", "an",
        "some",
        "one",          # as in "one student" (often ∃)
        "somebody", "someone", "something", "somewhere",
        "certain"     # multiword, but you can detect "a" + "certain"
}

UNIVERSAL_DET = {
        "every", "each",
        "all", 
        "any",       # context-sensitive; treated as universal in generic contexts
        "whoever", "whatever", "whichever"  # “free-choice” style universals
}

NEGATIVE_QUANT = {
        "no",
        "nobody", "noone", "no-one", "none",
        "nothing",
        "nowhere",
        "never"  # temporal but still a negative quantificational flavor
}

OPEN = {}

THE_WHITELIST = {
        "theorem", "theoretical", "theatre", "theater", "therapy",
        "therapist", "thermal", "thermodynamics", "theme", "thematic",
        "thesis", "theology", "theologian", "therefore", "thereby",
        "therein", "thereof", "thereon", "therewith", "thereafter",
        "thence", "thenceforth", "theft", "their", "theirs", "them",
        "themselves", "then", "there", "thereupon","they"
        # add more as you encounter them
}

WITH_WHITELIST = {
        "without", "within", "withstand",
}

OVER_WHITELIST = {
        "overall", "overlap", "overload", "overflow", "overhead",
        "overnight", "overseas", "oversee", "overcome", "overgrown",
        "overly", "overuse", "overestimate", "overwhelm",
}

UNDER_WHITELIST = {
        "undergo", "undergrad", "undergraduate", "underground",
        "understand", "understood", "undertake", "undertaker",
        "underline", "underlying", "underworld", "underestimate",
}

IN_WHITELIST = {
        "in", "inability", "inaccessible", "inaccurate", "inactive",
        "inadequate", "inadmissible", "inadvertent", "inadvisable",
        "inalienable", "inanimate", "inappropriate", "inaugural",
        "inbound", "inbred", "incentive", "incest", "inch", "incident",
        "incidental", "incidence", "incidentally", "incline",
        "inclined", "include", "included", "including", "inclusion",
        "inclusive", "incoherent", "income", "incoming", "incompatible",
        "incomplete", "inconclusive", "incongruent", "incongruous",
        "inconsistent", "inconvenient", "incorporate", "incorporated",
        "incorrect", "increase", "increased", "increasing", "increasingly",
        "incredible", "incredibly", "increment", "incremental",
        "incubate", "incubation", "incumbent", "indebted", "indecent",
        "indecision", "indefinite", "indefinitely", "indelible",
        "indemnity", "indentation", "independent", "independently",
        "index", "indexing", "indicate", "indicated", "indication",
        "indicative", "indicator", "indictment", "indigenous",
        "indigent", "indignant", "indignation", "indirect",
        "indirectly", "indiscreet", "indiscriminate", "indispensable",
        "indistinguishable", "individual", "individualism",
        "individualist", "individuality", "individually", "indivisible",
        "indoctrinate", "indolent", "indoor", "indoors", "induce",
        "induced", "induction", "inductive", "indulge", "indulgence",
        "industrial", "industrialize", "industry", "ineffective",
        "ineffectual", "inefficiency", "inefficient", "inelastic",
        "inept", "inequality", "inequitable", "inert", "inertia",
        "inescapable", "inevitable", "inevitably", "inexact",
        "inexcusable", "inexhaustible", "inexpensive", "inexperience",
        "inexperienced", "inexpert", "inexplicable", "infallible",
        "infamous", "infancy", "infant", "infantry", "infect",
        "infection", "infectious", "infer", "inference", "inferior",
        "inferiority", "infinite", "infinitely", "infinity", "inflame",
        "inflammation", "inflate", "inflated", "inflation", "inflect",
        "inflection", "inflexible", "inflow", "influence", "influential",
        "info", "inform", "informal", "informally", "information",
        "informative", "infrared", "infrastructure", "infrequent",
        "infrequently", "infuriate", "ingenious", "ingenuity",
        "ingredient", "inhabit", "inhabitant", "inhale", "inherent",
        "inherently", "inherit", "inheritance", "inhibit", "inhibition",
        "inhibitor", "inhospitable", "initial", "initially",
        "initiate", "initiation", "initiative", "inject", "injection",
        "injure", "injured", "injury", "injustice", "ink", "inland",
        "inlet", "inline", "inner", "innermost", "innocence",
        "innocent", "innovation", "innovative", "innovator", "innumerable",
        "inordinate", "input", "inquire", "inquiry", "inquisition",
        "inquisitive", "insane", "insanity", "insecure", "insecurity",
        "insensitive", "insert", "insertion", "inside", "insider",
        "insight", "insightful", "insignia", "insignificant",
        "insist", "insistence", "insistent", "insoluble", "inspect",
        "inspection", "inspector", "inspiration", "inspire", "inspired",
        "instability", "install", "installation", "instance",
        "instant", "instantaneous", "instantly", "instead", "instinct",
        "instinctive", "institute", "institution", "institutional",
        "instruct", "instruction","instructions", "instructional", "instructor",
        "instrument", "instrumental", "insufficient","insufficiency" "insulate",
        "insulation", "insulin", "insult", "insurance", "insure",
        "intact", "intake", "integer", "integral", "integrate",
        "integrated", "integration", "integrity", "intellect",
        "intellectual", "intelligent", "intelligible", "intend",
        "intended", "intense", "intensely", "intensify", "intensity",
        "intensive", "intent", "intention", "intentional", "interact",
        "interaction", "interactive", "intercept", "interchange",
        "interconnect", "interconnection", "interdependence",
        "interest", "interested", "interesting", "interface",
        "interfere", "interference", "interim", "interior", "interject",
        "interlock", "intermediate", "internal", "internally",
        "international", "internet", "interpersonal", "interpret",
        "interpretation", "interpreter", "interrogate", "interrupt",
        "interruption", "intersection", "interval", "intervene",
        "intervention", "interview", "intestate", "intestinal",
        "intimate", "intimately", "intimidate", "into", "intolerable",
        "intolerance", "intolerant", "intone", "intramural", "intranet",
        "intransitive", "intrinsic", "intrinsically", "introduce",
        "introduction", "introductory", "introspective", "intrude",
        "intrusion", "intuition", "intuitive", "inundate", "invade",
        "invalid", "invaluable", "invasion", "invasive", "invent",
        "invention", "inventive", "inventor", "inverse", "invert",
        "invest", "investigate", "investigation", "investigator",
        "investment", "investor", "invisible", "invitation", "invite",
        "invoke", "involuntary", "involve", "involved", "involvement",
        "invulnerable", "inward", "inwards"
}

PREFIX_WHITELIST = {
        "the": THE_WHITELIST,
        "with": WITH_WHITELIST,
        "over": OVER_WHITELIST,
        "under": UNDER_WHITELIST,
        "in": IN_WHITELIST
        # Add more as needed:
        # "from": FROM_WHITELIST,
        # "into": INTO_WHITELIST,
        # etc.
}
def get_dict(dataframe):
    mapping = []
    dictionary = {}
    for idx,column in enumerate(dataframe):
        mapping.append([idx,column])

    for idx,item in enumerate(mapping):
        dictionary.setdefault(mapping[idx][1],mapping[idx][0])#access the first and second values of array at idx
    #Dictionary can now be used to automatically get the index of a given column!
    return dictionary

#df = pd.DataFrame

def whitelisted(word):
    if word in DET or word in PREP or word in CONJ or word in COMP or word in MOD or word in AUX or word in EXISTENTIAL_DET or word in UNIVERSAL_DET or word in NEGATIVE_QUANT or word in OPEN or word in THE_WHITELIST or word in WITH_WHITELIST or word in OVER_WHITELIST or word in UNDER_WHITELIST or word in IN_WHITELIST or word in PREFIX_WHITELIST:
        return True
    else:
        return False
    
def at_least_3_chars(word):
    if len(word) >= 3:
        return True
    else:
        return False
    
def basic_plural_possible(word):
    if(word[-1]=="s"):
        return True
    if(word[-2]=="es"):
        return True
    
def word_to_location_mapping(file):
    trav = f"data/dict/working_set/traversable_text/{file}_traversable.csv"
    output = f"data/dict/working_set/mapped/{file}_mapped.csv"
    dataset = []
    #with open(output,"a",newline="") as file:
    #    header = ["word","sentence_id","location_in_sentence","bundle_id"]
    #    writer = csv.writer(file,escapechar='"')
    #    writer.writerow(header)
    #word,source,sentence_id,bundle_id
    #stats = f"data/dict/working_set/stats/{file}_stats.csv"

    df_trav = pd.read_csv(trav)
    #df_stats = pd.read_csv(stats)

    trav_dict = get_dict(df_trav)
    #stats_dict = get_dict(df_stats)
    #with open(output,"a",newline="") as file:
        #writer = csv.writer(file,escapechar='"')
    idx = 0
    last_num = 0
    for index,row in df_trav.iterrows():
        phrase = row[trav_dict.get("phrase")]
        cleaned = phrase.replace('[',"")
        cleaned = cleaned.replace(']',"")
        cleaned = cleaned.replace('\'',"")
        items = cleaned.split(", ")
        sent_id = row["sentence_id"]
        bund_id = row["bundle_id"]
        for item in items:
            if item != "":
                if last_num != sent_id:
                    idx = 0
                    last_num = sent_id
                newline = [item,sent_id,idx,bund_id]
                    #last_num=item[2]
                dataset.append(newline)
                idx = idx+1
                    #print(f"{item}, {sent_id}, {bund_id}")
    dataset.sort()
    with open(output,"w",newline="") as file:
        header = ["index","word","sentence_id","location_in_sentence","bundle_id"]
        writer = csv.writer(file,escapechar='"')
        writer.writerow(header)
        for idx,item in enumerate(dataset):
            row = [idx,item[0],item[1],item[2],item[3]]
            writer.writerow(row)
    #print(dataset)

def word_to_idx_mapping(file):
    stats = f"data/dict/working_set/stats/{file}_stats.csv"
    location_mapping = f"data/dict/working_set/mapped/{file}_mapped.csv"
    df = pd.read_csv(stats)
    df_loc = pd.read_csv(location_mapping)
    rows1=df.shape[0]
    rows2=df_loc.shape[0]
    search_index=int(rows2/2)
    #reader = csv.DictReader(islice(location_mapping,search_index,None))
    #reader = csv.DictReader(location_mapping)
    #with open(location_mapping,newline="") as file:
    #    reader = csv.reader(file)
    #for index1,row1 in df.iterrows():
        #search_index=int(rows2/2)
        #print("Reader 1:")
        #print(reader["word"])

        #print(df_loc.iloc(search_index))
        #if(df_loc.index(search_index))
        #print(index)
        #print(row["word"])
        #for index2,row2 in df_loc.iterrows():
            #The middle should be h (int=8)
            #So begin by immedietaly jumping to the middle, and go up or down depending on it's location relative to h

def search(word,document):
    input = f"data/dict/working_set/mapped/{document}_mapped.csv"
    word_list = []
    with open(input,'r') as file:
        reader = csv.reader(file)
        next(reader)
        rows = list(reader)
    for row in rows:
        word_list.append(row[1])
    print(bisect.bisect_left(word_list,word))
    print(bisect.bisect_right(word_list,word))
        #row_count = len(list(reader))
        #print(row_count)

word = "experiemnt"
#print(word_to_idx_mapping("ClassOverlapping"))
#word_to_location_mapping("ClassOverlapping")
search(word,"ClassOverlapping")

#pdfs/TheKingInYellow.pdf
#for index,row in df_stats.iterrows():
#    word = row[stats_dict.get("word")]
#    print(word)