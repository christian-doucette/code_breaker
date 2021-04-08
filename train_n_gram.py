import csv
import json
import sqlite3

# converts letters to ids (a->0, b->1, etc)
# assumes text is just lowercase letters
# puts n-1 26 tokens at start of word and 1 27 token at end of word
def to_ids(text, n_val):
    start_tokens       = (n_val-1) * [26]
    text_letter_tokens = [ord(letter) - 97 for letter in text]
    end_tokens         = [27]
    return start_tokens + text_letter_tokens + end_tokens




# runs the sql code in create_db.sql
# this drops and recreates the frequencies table
def recreate_database(db_conn):
        with open("create_db.sql", "r") as f:
            db_conn.executescript(f.read())




# trains n-gram on training data
# returns dictionary containing frequencies
def train_n_gram_from_file(data_filepath):
    n = 5            # number of letters being used in n-gram for prediction
    num_symbols = 28 # total number of symbols, 26 letters + start token (26) + end token (27)
    n_gram = dict()

    with open(data_filepath, newline='') as f:
        reader = csv.reader(f)
        parsed_csv = list(reader)[1:]


    for word, freq in parsed_csv:
        word_ids = to_ids(word, n)

        for i in range(0, len(word) + 1):
            this_ids = tuple(word_ids[i:i+n])
            n_gram[this_ids] = n_gram.get(this_ids, 0) + int(freq)


    # counts up frequencies and stores in n_gram dictionary
    for a in range(num_symbols):
        for b in range(num_symbols):
            for c in range(num_symbols):
                for d in range(num_symbols):
                    total_for_prefix = 0
                    for e in range(num_symbols):
                        this_key = (a,b,c,d,e)
                        total_for_prefix += n_gram.get(this_key, 0)

                    # divides by number of prefixes (sets of 4 letters)
                    # so frequencies table will hold probability for a letter given a prefix
                    for e in range(num_symbols):
                        this_key = (a,b,c,d,e)
                        if this_key in n_gram:
                            n_gram[this_key] = n_gram[this_key] / total_for_prefix

    # returns trained n_gram
    return n_gram




def save_n_gram_to_database(db_conn, n_gram):
    # gets cursor from database connection
    cursor = db_conn.cursor()
    sql_insert_frequency = "INSERT INTO frequencies (letter1, letter2, letter3, letter4, letter5, frequency) VALUES (?, ?, ?, ?, ?, ?)"

    # inserts each frequency into database
    for letters, frequency in n_gram.items():
        letter1, letter2, letter3, letter4, letter5 = letters
        cursor.execute(sql_insert_frequency, (letter1, letter2, letter3, letter4, letter5, frequency))







# ========================== #
#         Main Code          #
# ========================== #

# trains n_gram model from file, and saves in dictionary
n_gram_model = train_n_gram_from_file('data/unigram_freq.csv')
print("Successfully trained n gram model")

# connects to sqlite database
conn = sqlite3.connect('frequencies_database.db')

# drops and recreates frequencies database table
recreate_database(conn)
print("Successfully recreated frequencies database")

# adds all n-gram frequencies from dictionary to database
save_n_gram_to_database(conn, n_gram_model)
print("Successfully saved n gram model to database")


# commits transaction and closes connection
conn.commit()
conn.close()
