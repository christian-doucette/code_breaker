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
def calculate_score(text: str, n: int):
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
        this_rot_perplexity = calculate_score(this_rot, n)
        print(f"this: {this_rot}, with score {this_rot_perplexity}")

        #print(f'Test: {test_rot}, perplexity: {this_rot_perplexity}')
        if best_guess_perplex < this_rot_perplexity:
            best_guess_perplex = this_rot_perplexity
            best_guess = this_rot

    return best_guess



# helper function for break_substitution
def get_ext_order(cipher_text: str, n: int):
        # ext_order is the order in which letter substitutions will be guessed,
        # for now just sorting by letter frequency in ciphertext

        ext_order = []
        while len(ext_order) < 26:
            # greedily chooses letter in most valid n-grams at each step
            max_letter = ""
            max_letter_num_grams = -1

            for alphabet_letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if alphabet_letter not in ext_order:
                    num_grams_for_this_letter = 0

                    text_words = cipher_text.split()
                    for word in text_words:
                        letter_ids = to_ids_uppercase(word, n)
                        for i in range(0, len(word) + n - 1):
                            this_ids = tuple(letter_ids[i:i+5])
                            is_valid_gram = True
                            for id in this_ids:
                                if id not in [ord(ext_letter) - 65 for ext_letter in ext_order] and id != 26 and id != 27 and id != ord(alphabet_letter) - 65:
                                     is_valid_gram = False

                            if is_valid_gram:
                                num_grams_for_this_letter += 1




                    if max_letter_num_grams < num_grams_for_this_letter:
                        max_letter_num_grams = num_grams_for_this_letter
                        max_letter           = alphabet_letter


            ext_order.append(max_letter)

        return ext_order


# implentation of beam search algorithm from this paper: https://www.aclweb.org/anthology/P13-1154.pdf
# assumes text only includes uppercase letters and spaces
def break_substitution(cipher_text: str, n: int, n_keep: int = 4) -> str:
    # number of letters in the guesses so far
    cardinality = 0

    # lists, each entry is a tuple of (partial decipherment function, score for that function)
    H_s = [(dict(), 0)]
    H_t = []

    # ext_order is the order in which letter substitutions will be guessed,
    ext_order = get_ext_order(cipher_text, n)



    while cardinality < 26:
        #print(f'\n\nH_s at start of step {cardinality}: {H_s}')

        ciphertext_letter_to_try = ext_order[cardinality]
        for partial_func, partial_func_score in H_s:

            for plaintext_letter_to_try in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":

            # since I am only attempting to break 1:1 substitution ciphers, only need to check if letter not already mapped to
                if plaintext_letter_to_try not in partial_func.values():
                    # deep copies function then adds the test extra letter, and adds it to H_t with score
                    partial_func_with_extra_letter = {key: val for (key, val) in partial_func.items()}
                    partial_func_with_extra_letter[ciphertext_letter_to_try] = plaintext_letter_to_try

                    dict_to_pass = partial_func_with_extra_letter.copy()
                    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        if letter not in dict_to_pass:
                            dict_to_pass[letter] = '_'



                    # NEED TO UPDATE SCORE HERE, USING METHOD IN PAPER
                    partial_func_with_extra_letter_score = calculate_score(encrypt.encrypt_substitution(cipher_text, dict_to_pass), 5)

                    H_t.append((partial_func_with_extra_letter, partial_func_with_extra_letter_score))


        # removes all but n_keep best scoring partial decipherments
        H_t.sort(key = lambda func_score: -func_score[1])
        H_t = H_t[0:n_keep]

        # preparing for next cycle
        H_s = H_t
        H_t = []
        #print(f'H_s at end of step {cardinality}: {H_s}')

        cardinality += 1


    best_substitution, best_substitution_score = H_s[0]
    return encrypt.encrypt_substitution(cipher_text, best_substitution)





# Loads trained n_gram model
with open('trained_model/trained_ngram.json') as json_file:
    n_grams = json.load(json_file)


# gets n_val for n gram - getting from model metadata
# should raise error here if its not a tuple, although that should never happen
n_val = len(eval(next(iter(n_grams))))
print(f'n_val: {n_val}')


my_cipher_text = encrypt.encrypt_substitution("PA QB EMCO HAF RMLB PA RMLB M LBOH RCVR CS PA FUWBODPMUW OCNX MUW ZAOPH PRB RFZAO CD BKPOBZBYH DFQPYB MUW GCPRAFP M DAYCW VOMDI AE PRBAOBPCNMY IRHDCND ZADP AE PRB TAXBD GCYY VA ALBO M PHICNMY LCBGBOD RBMW PRBOBD MYDA OCNXD UCRCYCDPCN AFPYAAX GRCNR CD WBEPYH GALBU CUPA RCD NRMOMNPBOCDMPCAU  RCD IBODAUMY IRCYADAIRH WOMGD RBMLCYH EOAZ UMOAWUMHM LAYHM YCPBOMPFOB EAO CUDPMUNB PRB EMUD FUWBODPMUW PRCD DPFEE PRBH RMLB PRB CUPBYYBNPFMY NMIMNCPH PA POFYH MIIOBNCMPB PRB WBIPRD AE PRBDB TAXBD PA OBMYCJB PRMP PRBHOB UAP TFDP EFUUH PRBH DMH DAZBPRCUV WBBI MQAFP YCEB MD M NAUDBSFBUNB IBAIYB GRA WCDYCXB OCNX MUW ZAOPH POFYH MOB CWCAPD AE NAFODB PRBH GAFYWUP MIIOBNCMPB EAO CUDPMUNB PRB RFZAFO CU OCNXD BKCDPBUNCMY NMPNRIROMDB GFQQM YFQQM WFQ WFQ GRCNR CPDBYE CD M NOHIPCN OBEBOBUNB PA PFOVBUBLD OFDDCMU BICN EMPRBOD MUW DAUD CZ DZCOXCUV OCVRP UAG TFDP CZMVCUCUV AUB AE PRADB MWWYBIMPBW DCZIYBPAUD DNOMPNRCUV PRBCO RBMWD CU NAUEFDCAU MD WMU RMOZAUD VBUCFD FUEAYWD CPDBYE AU PRBCO PBYBLCDCAU DNOBBUD GRMP EAAYD RAG C ICPH PRBZ MUW HBD QH PRB GMH C WA RMLB M OCNX MUW ZAOPH PMPPAA MUW UA HAF NMUUAP DBB CP CPD EAO PRB YMWCBD BHBD AUYH MUW BLBU PRBH RMLB PA WBZAUDPOMPB PRMP PRBHOB GCPRCU CS IACUPD AE ZH AGU IOBEBOMQYH YAGBO QBEAOBRMUW", encrypt.get_random_substitution())
#print(my_cipher_text)
print(break_substitution(my_cipher_text, 5))
# Tests it by attempting to break a caesar cipher
# print(f'BEST GUESS: {break_caesar("QFC QYYYYYYYYYYGB", n_val)}')
