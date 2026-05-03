# Source - https://stackoverflow.com/a/73756253
# Posted by user7070613, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-30, License - CC BY-SA 4.0

import csv

# -------- VERBS --------
header = None
verbs_merged = []

for f in ('data/pos/core_pos/verbs.csv', 'new_types/Verbs2_202604300832.csv'):
    with open(f, newline='') as csv_file:
        reader = csv.reader(csv_file)
        if not header:
            verbs_merged.append(next(reader))
            header = True
        else:
            next(reader)
        for row in reader:
            verbs_merged.append(row)

with open('verbs.csv', 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(verbs_merged)


# -------- NOUNS --------
header = None
nouns_merged = []

for f in ('data/pos/core_pos/nouns.csv', 'data/dict/intermediate_data/nouns2.csv'):
    with open(f, newline='') as csv_file:
        reader = csv.reader(csv_file)
        if not header:
            nouns_merged.append(next(reader))
            header = True
        else:
            next(reader)
        for row in reader:
            nouns_merged.append(row)

with open('nouns.csv', 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(nouns_merged)


# -------- ADVERBS --------
header = None
adverbs_merged = []

for f in ('data/pos/core_pos/adverbs.csv', 'data/dict/intermediate_data/Adverbs2_202604300831.csv'):
    with open(f, newline='') as csv_file:
        reader = csv.reader(csv_file)
        if not header:
            adverbs_merged.append(next(reader))
            header = True
        else:
            next(reader)
        for row in reader:
            adverbs_merged.append(row)

with open('adverbs.csv', 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(adverbs_merged)

# -------- ADJECTIVES --------
header = None
adverbs_merged = []

for f in ('data/pos/core_pos/adjectives.csv', 'data/dict/intermediate_data/Adjectives2_202604300830.csv'):
    with open(f, newline='') as csv_file:
        reader = csv.reader(csv_file)
        if not header:
            adverbs_merged.append(next(reader))
            header = True
        else:
            next(reader)
        for row in reader:
            adverbs_merged.append(row)

with open('adjectives.csv', 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(adverbs_merged)


#cat csv_new_file.csv

#id,col1,col2,col3
#1,'test','dog','cat'
#2,'foo','fish','rabbit'
#3,'bar','owl','crow'
#4,'spam','eel','cow'
