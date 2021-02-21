import random
import re


#======================#
#   General Functions  #
#======================#

# returns True if a given character is an uppercase letter
def is_uppercase_letter(c: str) -> bool:
    return (65 <= ord(c)) and (ord(c) < 91)



# the function for cleaning input text
# for now just maps letters to uppercase
def clean_text(input_text: str) -> str:
    cleaned_text = input_text.upper()  # maps to uppercase
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
    cleaned_plain_text = clean_text(plain_text)
    cipher_text = ''.join([rotate_letter(letter, rot) for letter in cleaned_plain_text])
    return cipher_text





#======================#
# Substitution Cipher  #
#======================#

# gets a random substitution of uppercase letters
def get_random_subsititution():
    letters = [letter for letter in "ABCDEFGHIJKLMNOPQRSTUVQXYZ"]
    random_letters_permutation = random.sample(letters, k=26)
    random_substitution = {letters[i]: random_letters_permutation[i] for i in range(0, 26)}
    return random_substitution


# encrypts text using Substitution Cipher
def encrypt_substitution(plain_text: str, substitutions) -> str:
    cleaned_plain_text = clean_text(plain_text)
    cipher_text = ''.join([substitutions.get(letter, letter) for letter in cleaned_plain_text])
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





#======================#
#   Tests for funcs    #
#======================#

substitutions_dict = get_random_subsititution()
print(substitutions_dict)


print(encrypt_caesar("Hello there", 25))
print(encrypt_substitution("Test message", substitutions_dict))
print(encrypt_vignere("the sun and the man in the moon", "king"))
