import csv
import pandas as pd

def optimal_string_alignment_distance(s1, s2):
    # Create a table to store the results of subproblems
    dp = [[0 for j in range(len(s2)+1)] for i in range(len(s1)+1)]
    
    # Initialize the table
    for i in range(len(s1)+1):
        dp[i][0] = i
    for j in range(len(s2)+1):
        dp[0][j] = j

    # Populate the table using dynamic programming
    for i in range(1, len(s1)+1):
        for j in range(1, len(s2)+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

    # Return the edit distance
    return dp[len(s1)][len(s2)]
    
words = pd.read_csv("data/word_sentiment_stats.csv")

pos_cols = [
    "noun",
    "verb",
    "adjective",
    "adverb",
    "auxiliary",
    "compositions",
    "conjunctions",
    "determiners",
    "existential_determiners",
    "modifiers",
    "negative_quantifiers",
    "prepositions",
    "universal_determiners",
    "possessive_determiners",
    "pronouns",
]

# rows where all POS columns are 0
no_pos = words[words[pos_cols].eq(0).all(axis=1)]

print(no_pos)

# optionally save them
no_pos.to_csv("data/unclassified_words.csv", index=False)
        #print("Dem:", len(dems))
    #elif rep_num < 100 and row['Party'] == 'Republican':
    #    reps.append(row)
    #    print('Rep:', len(reps))
#print(optimal_string_alignment_distance("geeks", "forgeeks"))

