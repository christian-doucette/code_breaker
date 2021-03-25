import csv
import math
import numpy as np
import encrypt



# assumes text is just lowercase letters
def to_ids(text, n_val):
    start_tokens       = (n_val-1) * [26]
    text_letter_tokens = [ord(letter) - 97 for letter in text]
    end_tokens         = (n_val-1) * [27]
    return start_tokens + text_letter_tokens + end_tokens


# assumes text is just uppercase letters
def to_ids_uppercase(text, n_val):
    start_tokens       = (n_val-1) * [26]
    text_letter_tokens = [ord(letter) - 65 for letter in text]
    end_tokens         = (n_val-1) * [27]
    return start_tokens + text_letter_tokens + end_tokens



# For now using 5-gram
# should switch to numpy for speed, but fixed size may be issue, depending on how big the biggest is
# Letter is index (i.e. a is 0, b is 1, etc)
# 26 is start token, 27 is end token

n = 5
k = 28 # total number of symbols
n_grams = np.zeros(shape = n * (k,), dtype=int)

# Dataset has 333333 words with frequencies
with open('data/unigram_freq.csv', newline='') as f:
    reader = csv.reader(f)
    parsed_csv = list(reader)[1:]


for word, freq in parsed_csv:
    word_ids = to_ids(word, 5)

    for i in range(0, len(word) + 5 - 1):
        this_ids = tuple(word_ids[i:i+5])
        n_grams[this_ids] += int(freq)



print(f"Max value in ngrams: {np.amax(n_grams)}")


# assumes it is all uppercase letters
def calculate_perplexity(text, n_val):
    perplexity_log = 0

    text_words = text.split()
    for word in text_words:
        #print(f"word: {word}")
        letter_ids = to_ids_uppercase(word, n_val)
        #print(f"ids: {letter_ids}")

        for i in range(0, len(word) + n_val - 1):
            this_ids = tuple(letter_ids[i:i+5])
            perplexity_log += math.log(n_grams[this_ids] + 1, 10)
            #print(f'Checking {i} to {i+5} in {word}: {this_ids}')

    return perplexity_log


"""
print(calculate_perplexity("HELLO MY", 5))
print(calculate_perplexity("JELLO", 5))
print(calculate_perplexity("XXZXX", 5))
"""


best_guess = ""
best_guess_perplex = 0
for i in range(26):
    test_rot = encrypt.encrypt_caesar("YJXY RJXXFLJ YT XJJ NK RD RJYMTI NX BTWPNSL", i)
    print(f'Test: {test_rot}, perplexity: {calculate_perplexity(test_rot, 5)}')
    if best_guess_perplex < calculate_perplexity(test_rot, 5):
        best_guess_perplex = calculate_perplexity(test_rot, 5)
        best_guess = test_rot

print(f"BEST GUESS: {best_guess}")
