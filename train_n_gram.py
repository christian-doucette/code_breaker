import csv
import json


# assumes text is just lowercase letters
def to_ids(text, n_val):
    start_tokens       = (n_val-1) * [26]
    text_letter_tokens = [ord(letter) - 97 for letter in text]
    end_tokens         = (n_val-1) * [27]
    return start_tokens + text_letter_tokens + end_tokens






# For now using 5-gram
# should switch to numpy for speed, but fixed size may be issue, depending on how big the biggest is
# Letter is index (i.e. a is 0, b is 1, etc)
# 26 is start token, 27 is end token

n = 5
k = 28 # total number of symbols
n_grams = dict()

# Dataset has 333333 words with frequencies
with open('data/unigram_freq.csv', newline='') as f:
    reader = csv.reader(f)
    parsed_csv = list(reader)[1:]


for word, freq in parsed_csv:
    word_ids = to_ids(word, 5)

    for i in range(0, len(word) + 5 - 1):
        this_ids = str(tuple(word_ids[i:i+5]))
        n_grams[this_ids] = n_grams.get(this_ids, 0) + int(freq)



# Saves dict to file
with open('trained_model/trained_ngram.json', 'w') as fp:
    json.dump(n_grams, fp, indent=4)
