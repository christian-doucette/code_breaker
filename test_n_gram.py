import math
import json
import encrypt


# gets the ids for a word
# assumes text is just uppercase letters
def to_ids_uppercase(text: str, n: int):
    start_tokens       = (n-1) * [26]
    text_letter_tokens = [ord(letter) - 65 for letter in text]
    end_tokens         = (n-1) * [27]
    return start_tokens + text_letter_tokens + end_tokens



# calculates perplexity of a text
# assumes it is all uppercase letters
def calculate_perplexity(text: str, n: int):
    perplexity_log = 0

    text_words = text.split()
    for word in text_words:
        #print(f"word: {word}")
        letter_ids = to_ids_uppercase(word, n)
        #print(f"ids: {letter_ids}")

        for i in range(0, len(word) + n - 1):
            this_ids = str(tuple(letter_ids[i:i+5]))
            perplexity_log += math.log(n_grams.get(this_ids, 0) + 1, 10)
            #print(f'Checking {i} to {i+5} in {word}: {this_ids}')

    return perplexity_log




# finds and returns rotation of cipher text with best perplexity value
# assumes text only includes uppercase letters and spaces
def break_caesar(cipher_text: str, n: int) -> str:
    best_guess = ""
    best_guess_perplex = 0
    for i in range(26):
        this_rot = encrypt.encrypt_caesar(cipher_text, i)
        this_rot_perplexity = calculate_perplexity(this_rot, n)

        #print(f'Test: {test_rot}, perplexity: {this_rot_perplexity}')
        if best_guess_perplex < this_rot_perplexity:
            best_guess_perplex = this_rot_perplexity
            best_guess = this_rot

    return best_guess




# Loads trained n_gram model
with open('trained_model/trained_ngram.json') as json_file:
    n_grams = json.load(json_file)


# gets n_val for n gram - getting from model metadata
n_val = n_grams['n_val']

# Tests it by attempting to break a caesar cipher
print(f'BEST GUESS: {break_caesar("LJSBO CBBLLPOFO", n_val)}')
