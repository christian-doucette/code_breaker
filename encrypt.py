import random
import re
import unicodedata


#======================#
#   General Functions  #
#======================#

# returns True if a given character is an uppercase letter
def is_uppercase_letter(c: str) -> bool:
    return (65 <= ord(c)) and (ord(c) < 91)



# the function for cleaning input text
# for now just maps letters to uppercase
def clean_text(input_text: str) -> str:
    cleaned_text = input_text.upper()                           # maps to uppercase
    cleaned_text = re.sub("[\']", "", cleaned_text)             # removes ', so contractions will still be one word
    cleaned_text = unicodedata.normalize("NFKD", cleaned_text)  # normalizes with unicode
    cleaned_text = re.sub("[^A-Z\s]", " ", cleaned_text)        # maps all non-letter, non-space characters to spaces
    cleaned_text = ' '.join(cleaned_text.split())               # puts exactly one space between words

    return cleaned_text



# rotates an uppercase letter by n places
# if the input is not an uppercase letter, just returns the input
def rotate_letter(letter: str, n: int) -> str:
    if is_uppercase_letter(letter):
        n = n % 26
        place_in_alphabet = ord(letter) - 65
        rotated_place = (place_in_alphabet + n) % 26
        return chr(rotated_place + 65)

    else:
        return letter





#======================#
#     Caesar Cipher    #
#======================#

# gets a random number in [0, 25]
def get_random_rot():
    return random.choice(range(0,26))


# encrypts text using Caesar Cipher
def encrypt_caesar(plain_text: str, rot: int) -> str:
    rot = rot % 26
    cleaned_plain_text = clean_text(plain_text)
    cipher_text = ''.join([rotate_letter(letter, rot) for letter in cleaned_plain_text])
    return cipher_text





#======================#
# Substitution Cipher  #
#======================#

# gets a random substitution of uppercase letters
def get_random_substitution():
    letters = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
    random_letters_permutation = random.sample(letters, k=26)
    random_substitution = {letters[i]: random_letters_permutation[i] for i in range(0, 26)}
    return random_substitution


# encrypts text using Substitution Cipher
def encrypt_substitution(plain_text: str, substitutions) -> str:
    cleaned_plain_text = clean_text(plain_text)
    cipher_text = ''.join([substitutions.get(letter, letter) for letter in cleaned_plain_text])
    return cipher_text

# encrypts text using Substitution Cipher, where the substitutions dictionary can be partial
def encrypt_substitution_partial(plain_text: str, substitutions) -> str:
    def map_character(character: str, partial_dict) -> str:
        if character not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ_ ":
            raise Exception(f"Character {character} is not valid")
        elif character == ' ':
            return ' '
        elif character in partial_dict:
            return partial_dict[character]
        else:
            return '_'

    cleaned_plain_text = clean_text(plain_text)
    cipher_text = ''.join([map_character(letter, substitutions) for letter in cleaned_plain_text])
    return cipher_text






#======================#
#    Vignere Cipher    #
#======================#


# encrypts text using Vignere Cipher
def encrypt_vignere(plain_text: str, keyword: str) -> str:
    cleaned_plain_text = clean_text(plain_text)

    keyword = keyword.upper()                 # maps keyword to uppercase
    keyword = re.sub("[^A-Z]", "", keyword)   # removes all non letter characters
    offsets = [ord(letter) - 65 for letter in keyword]

    loc_in_keyword = 0
    cipher_text    = ""

    for character in cleaned_plain_text:
        if is_uppercase_letter(character):
            offset = offsets[loc_in_keyword]
            cipher_text += rotate_letter(character, offset)
            loc_in_keyword = (loc_in_keyword + 1) % len(keyword)

        else:
            cipher_text += character

    return cipher_text
