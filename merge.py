# Source - https://stackoverflow.com/a/73756253
# Posted by user7070613, modified by community. See post 'Timeline' for change history
# Retrieved 2026-04-30, License - CC BY-SA 4.0

import csv

header = None
new_file = []
for f in ('data/dict/csvs/verbs.csv', 'new_types/Verbs2_202604300832.csv'):
    with open(f, newline='') as csv_file:
        reader = csv.reader(csv_file)
        if not header:
            new_file.append(next(reader))
            header = True
        else:
            next(reader)
        for row in reader:
            new_file.append(row)

with open('verbs.csv', 'w', newline='') as csv_out:
    writer = csv.writer(csv_out)
    writer.writerows(new_file)


#cat csv_new_file.csv

#id,col1,col2,col3
#1,'test','dog','cat'
#2,'foo','fish','rabbit'
#3,'bar','owl','crow'
#4,'spam','eel','cow'
