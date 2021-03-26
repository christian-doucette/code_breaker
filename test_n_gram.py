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



# calculates perplexity of a text, with laplacian smoothing
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
        print(f"this: {this_rot}, with score {this_rot_perplexity}")

        #print(f'Test: {test_rot}, perplexity: {this_rot_perplexity}')
        if best_guess_perplex < this_rot_perplexity:
            best_guess_perplex = this_rot_perplexity
            best_guess = this_rot

    return best_guess



# assumes text only includes uppercase letters and spaces
def break_substitution(cipher_text: str, n: int, n_keep: int = 4) -> str:
    # number of letters in the guesses so far
    cardinality = 0

    # lists, each entry is a tuple of (partial decipherment function, score for that function)
    H_s = [(dict(), 0)]
    H_t = []

    # ext_order is the order in which letter substitutions will be guessed,
    # for now just sorting by letter frequency in ciphertext
    letter_counts = {alphabet_letter: 0 for alphabet_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    for letter in cipher_text:
        if letter in letter_counts:
            letter_counts[letter] += 1

    sorted_letter_counts = sorted(letter_counts.items(), key = lambda k_v: -k_v[1])
    ext_order = [key for key,val in sorted_letter_counts]



    while cardinality < 26:
        print(f'\n\nH_s at start of step {cardinality}: {H_s}')

        ciphertext_letter_to_try = ext_order[cardinality]
        for partial_func, partial_func_score in H_s:

            for plaintext_letter_to_try in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            # since I am only attempting to break 1:1 substitution ciphers, only need to check if letter not already mapped to
                if plaintext_letter_to_try not in partial_func.values():
                    # deep copies function then adds the test extra letter, and adds it to H_t with score
                    partial_func_with_extra_letter = {key: val for (key, val) in partial_func.items()}
                    partial_func_with_extra_letter[ciphertext_letter_to_try] = plaintext_letter_to_try

                    # NEED TO UPDATE SCORE HERE, USING METHOD IN PAPER
                    partial_func_with_extra_letter_score = partial_func_score
                    H_t.append((partial_func_with_extra_letter, partial_func_with_extra_letter_score))


        # removes all but n_keep best scoring partial decipherments
        H_t.sort(key = lambda func_score: -func_score[1])
        H_t = H_t[0:n_keep]

        # preparing for next cycle
        H_s = H_t
        H_t = []
        print(f'H_s at end of step {cardinality}: {H_s}')

        cardinality += 1


    best_substitution, best_score = H_s[0]
    return encrypt.encrypt_substitution(cipher_text, best_substitution)



print(break_substitution("TEST STRING TO SEE HOW THIS WORKS", 5))


# Loads trained n_gram model
with open('trained_model/trained_ngram.json') as json_file:
    n_grams = json.load(json_file)


# gets n_val for n gram - getting from model metadata
# should raise error here if its not a tuple, although that should never happen
n_val = len(eval(next(iter(n_grams))))
print(f'n_val: {n_val}')

# Tests it by attempting to break a caesar cipher
print(f'BEST GUESS: {break_caesar("QFC QYYYYYYYYYYGB", n_val)}')
