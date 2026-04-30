import matplotlib.pyplot as plt
from clean_data import pos
import csv
import numpy as np
#jittered_rating = reviews["Language_Status"] + np.random.uniform(-0.2, 0.2, len(reviews))
with open('data.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    plt.scatter(reader["Sentiment_Polarity"], reader["Language_Status"])
    plt.title("Sentiment vs. Language")
    plt.xlabel("Sentiment")
    plt.ylabel("Language")
    plt.show()