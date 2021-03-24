import csv
import numpy as np


# For now using 5-gram
# Letter is index (i.e. a is 0, b is 1, etc)
# 26 is start token, 27 is end token


# Dataset has 333333 words with frequencies
with open('data/unigram_freq.csv', newline='') as f:
    reader = csv.reader(f)
    parsed_csv = list(reader)[1:10]


for word, freq in parsed_csv:
    print(word)
