# returns True if a given character is an uppercase letter
def is_uppercase_letter(c: str) -> bool:
    return (65 <= ord(c)) and (ord(c) < 91)



# maps letters to uppercase
def clean_text(input_text: str) -> str:
    cleaned_text = input_text.upper()                    # maps to uppercase
    return cleaned_text



# rotates an uppercase letter by n places
# if the input is not an uppercase, just returns the input
def rotate_letter(letter: str, n: int) -> str:
    if is_uppercase_letter(letter):
        n = n % 26
        place_in_alphabet = ord(letter) - 65
        rotated_place = (place_in_alphabet + n) % 26
        return chr(rotated_place + 65)

    else:
        return letter




def encrypt_caesar(plain_text: str, rot: int) -> str:
    cleaned_plain_text = clean_text(plain_text)
    cipher_text = ''.join([rotate_letter(letter, rot) for letter in cleaned_plain_text])
    return cipher_text




def encrypt_substitution(plain_text: str, substitutions) -> str:
    cleaned_plain_text = clean_text(plain_text)
    cleaned_plain_text = "HI THERE"
    cipher_text = ''.join([substitutions.get(letter, letter) for letter in cleaned_plain_text])
    return cipher_text

substitutions_dict = {letter: letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

print(encrypt_caesar("Hello there", 25))
print(encrypt_substitution("Test message", substitutions_dict))
