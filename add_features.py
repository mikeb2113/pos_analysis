import pandas as pd
import numpy as np
from scipy.special import lambertw
from extract_words import pathing
from csir.document import Document
from csir.skeletons import Skeletons
from csir.pdf_extract import pdf_to_text,unstick_library_prefixes
import csir.skeletons
import json

for path in pathing:
    print(f"path: {path}")
    #data/dict/working_set/stats/ClassOverlapping_stats.csv
    input_file = "data/dict/working_set/stats/" + path + "_stats" + ".csv"
    #data/dict/working_set/stats_with_features
    output_file1 = "data/dict/working_set/stats_with_features" + path + ".csv"

    # Python code
    def inverse_ackermann(n):
        # Check if the input is small enough
        # to solve directly
        if n <= 4:
            return n

        # Divide the problem into
        # two smaller problems
        a = inverse_ackermann(n - 1)
        b = inverse_ackermann(n - 2)

        # Combine the solutions of the
        # two smaller problems
        return a + b

    # Define the input
    #n = 10

    # Solve the problem using the
    # inverse Ackermann algorithm
    #result = inverse_ackermann(n)

    # Print the result
    #print("Result:", result)

    # This code is contributed by lokeshmvs21.

    df = pd.read_csv(input_file)

    # 1) log(relative_frequency)
    total_frequency = df["frequency"].sum()
    df["relative_frequency"] = df["frequency"] / total_frequency


    # log(0) is invalid, so replace 0 with NaN before logging
    #df["log_relative_frequency"] = (np.log(df["relative_frequency"].replace(0, np.nan))/np.log(300))
    df["double_log_freq"] = np.log1p(np.log1p(np.log1p(np.log1p(df["frequency"]))))# 2) participation score across POS dimensions
    pos_columns = [
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

    df["participation_score"] = df[pos_columns].sum(axis=1)/15

    df.to_csv(output_file1, index=False)

    print(f"Saved updated CSV to {output_file1}")