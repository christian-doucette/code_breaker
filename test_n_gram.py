import math
import json
import encrypt
import sqlite3


# gets the ids for a word
# assumes text is just uppercase letters
def to_ids_uppercase(text: str, n: int):
    start_tokens       = (n-1) * [26]
    text_letter_tokens = [ord(letter) - 65 for letter in text]
    end_tokens         = [27]
    return start_tokens + text_letter_tokens + end_tokens




# calculates perplexity of a text, with laplacian smoothing
# assumes it is all uppercase letters
def calculate_score(text: str, n: int, cur):
    perplexity_log = 0

    text_words = text.split()
    for word in text_words:
        #print(f"word: {word}")
        letter_ids = to_ids_uppercase(word, n)
        print(letter_ids)
        #print(f"ids: {letter_ids}")

        for i in range(0, len(word) + 1):
            letter1, letter2, letter3, letter4, letter5 = tuple(letter_ids[i:i+5])
            #cur.execute("SELECT * FROM frequencies WHERE letter1 = 18 AND letter2 = 19 AND letter3 = 20 AND letter4 = 3 AND letter5 = 4")
            if not all(map(lambda x: 0 <= x and x < 28, letter_ids[i:i+5])):
                perplexity_log += math.log(.000001, 10)

            else:
                rows = cur.execute("SELECT frequency FROM frequencies WHERE letter1 = ? AND letter2 = ? AND letter3 = ? AND letter4 = ? AND letter5 = ?", (letter1, letter2, letter3, letter4, letter5)).fetchall()
                if len(rows) == 0:
                    letter_ids_freq = 0
                else:
                    letter_ids_freq = rows[0][0]

                perplexity_log += math.log(letter_ids_freq + .000001, 10)

    return perplexity_log


calculate_score("THI_ I_ _OME TE_T TEXT", 5, sqlite3.connect('frequencies_database.db').cursor())

# finds and returns rotation of cipher text with best perplexity value
# assumes text only includes uppercase letters and spaces
def break_caesar(cipher_text: str, n: int) -> str:
    # Gets database connection and cursor
    conn = sqlite3.connect('frequencies_database.db')
    cur  = conn.cursor()

    best_guess = cipher_text
    best_guess_score = calculate_score(cipher_text, n, cur)

    for i in range(1, 26):
        this_rot = encrypt.encrypt_caesar(cipher_text, i)
        this_rot_score = calculate_score(this_rot, n, cur)
        #print(f"this: {this_rot}, with score {this_rot_score}")

        #print(f'Test: {test_rot}, perplexity: {this_rot_perplexity}')
        if best_guess_score < this_rot_score:
            best_guess_score = this_rot_score
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
                        for i in range(0, len(word) + 1):
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
    conn = sqlite3.connect('frequencies_database.db')
    cur  = conn.cursor()

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
                    partial_func_with_extra_letter = partial_func.copy()
                    partial_func_with_extra_letter[ciphertext_letter_to_try] = plaintext_letter_to_try



                    # currently recalculating score, but would be easier to only add the new ones
                    partial_func_with_extra_letter_score = calculate_score(encrypt.encrypt_substitution_partial(cipher_text, partial_func_with_extra_letter), 5, cur)

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
#with open('trained_model/trained_ngram.json') as json_file:
#    n_grams = json.load(json_file)


# gets n_val for n gram - getting from model metadata
# should raise error here if its not a tuple, although that should never happen
n_val = 5 #len(eval(next(iter(n_grams))))
#print(f'n_val: {n_val}')

#letters = "PA QB EMCO HAF RMLB PA RMLB M LBOH RCVR CS PA FUWBODPMUW OCNX MUW ZAOPH PRB RFZAO CD BKPOBZBYH DFQPYB MUW GCPRAFP M DAYCW VOMDI AE PRBAOBPCNMY IRHDCND ZADP AE PRB TAXBD GCYY VA ALBO M PHICNMY LCBGBOD RBMW PRBOBD MYDA OCNXD UCRCYCDPCN AFPYAAX GRCNR CD WBEPYH GALBU CUPA RCD NRMOMNPBOCDMPCAU  RCD IBODAUMY IRCYADAIRH WOMGD RBMLCYH EOAZ UMOAWUMHM LAYHM YCPBOMPFOB EAO CUDPMUNB PRB EMUD FUWBODPMUW PRCD DPFEE PRBH RMLB PRB CUPBYYBNPFMY NMIMNCPH PA POFYH MIIOBNCMPB PRB WBIPRD AE PRBDB TAXBD PA OBMYCJB PRMP PRBHOB UAP TFDP EFUUH PRBH DMH DAZBPRCUV WBBI MQAFP YCEB MD M NAUDBSFBUNB IBAIYB GRA WCDYCXB OCNX MUW ZAOPH POFYH MOB CWCAPD AE NAFODB PRBH GAFYWUP MIIOBNCMPB EAO CUDPMUNB PRB RFZAFO CU OCNXD BKCDPBUNCMY NMPNRIROMDB GFQQM YFQQM WFQ WFQ GRCNR CPDBYE CD M NOHIPCN OBEBOBUNB PA PFOVBUBLD OFDDCMU BICN EMPRBOD MUW DAUD CZ DZCOXCUV OCVRP UAG TFDP CZMVCUCUV AUB AE PRADB MWWYBIMPBW DCZIYBPAUD DNOMPNRCUV PRBCO RBMWD CU NAUEFDCAU MD WMU RMOZAUD VBUCFD FUEAYWD CPDBYE AU PRBCO PBYBLCDCAU DNOBBUD GRMP EAAYD RAG C ICPH PRBZ MUW HBD QH PRB GMH C WA RMLB M OCNX MUW ZAOPH PMPPAA MUW UA HAF NMUUAP DBB CP CPD EAO PRB YMWCBD BHBD AUYH MUW BLBU PRBH RMLB PA WBZAUDPOMPB PRMP PRBHOB GCPRCU CS IACUPD AE ZH AGU IOBEBOMQYH YAGBO QBEAOBRMUW"
my_cipher_text = encrypt.encrypt_substitution("I GOT A LETTER THIS MORNING WHAT DO YOU RECKON IT READ I READ IT AND IT SAID THE GIRL YOU LOVE IS DEAD WHEN I HEAR MY NAME I WANT TO DISAPPEAR YES IM BUSTED BUT MY HEART WONT LET ME DIE WHEN I FEEL ALRIGHT DARLING WONT YOU COME AROUND", encrypt.get_random_substitution())
#print(my_cipher_text)
#print(break_substitution("IA TK MIMFL OIJK JKFLUBYUDOR ZOUNHIFS LCK TIOM SYXL GR LCK GKXBM XFM LBKWGOIFS YJKB ZBKNIZINKD TK DCYUOM FKJKB GK IA TK MIMFL OIJK JKFLUBYUDOR ZOUNHIFS LCK TIOM SYXL GR LCK GKXBM XFM LBKWGOIFS YJKB ZBKNIZINKD TK DCYUOM FKJKB GK MKZBKDDKM IJK FY MYUGL GUL XOBKXMR DCYUOM GK AXMKM AXLXOIDLIN XFM XSKM JIBSIFIX TYYOA MKZBKDDKM IJK FY MYUGL GUL XOBKXMR DCYUOM GK AXMKM AXLXOIDLIN XFM XSKM JIBSIFIX TYYOA", 5))
#print(break_substitution("B TWD Y OFDDFV DABI XWVUBUT NAYD ZW CWS VFJGWU BD VFYZ B VFYZ BD YUZ BD IYBZ DAF TBVO CWS OWEF BI ZFYZ NAFU B AFYV XC UYXF B NYUD DW ZBIYHHFYV CFI BX PSIDFZ PSD XC AFYVD NWUD OFD XF ZBF NAFU B LFFO YOVBTAD ZYVOBUT NWUD CWS JWXF YVWSUZ", 5))

# Tests it by attempting to break a caesar cipher
# print(f'BEST GUESS: {break_caesar("QFC QYYYYYYYYYYGB", n_val)}')
