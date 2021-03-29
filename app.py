# flask imports
from flask import Flask, render_template, request

# sqlite3 for database
import sqlite3


# My code files
import encrypt      # encryption functions for caesar, substitution and vignere
import test_n_gram  # decryption functions for caesar and substitution


app = Flask(__name__)


#=================================#
#             Routes              #
#=================================#

# Loads Home Page, with brief description of the project
@app.route('/')
def home_page():
    return render_template('home_page.html')






#======== Caesar Cipher Routes =========#

# Loads the Caesar Cipher Page
@app.route('/caesar')
def caesar_page():
    return render_template('caesar_page.html', encrypted_text = None, decrypted_text = None)



# Loads the Caesar Cipher Page, when the user has entered text to be encrypted
@app.route('/caesar/encrypt/', methods=['GET', 'POST'])
def caesar_encrypt_input():
    # Gets data from form
    input_text = request.args['input_text']
    input_rot  = int(request.args['input_rot'])

    # runs encryption function
    encrypted_text = encrypt.encrypt_caesar(input_text, input_rot)
    return render_template('caesar_page.html', encrypted_text = encrypted_text, decrypted_text = None)



# Loads the Caesar Cipher Page, when the user has entered text to be decrypted
@app.route('/caesar/decrypt/', methods=['GET', 'POST'])
def caesar_decrypt_input():
    # Gets data from form
    input_text = request.args['input_text']

    # runs decryption function
    decrypted_text = test_n_gram.break_caesar(input_text, 5)
    return render_template('caesar_page.html', encrypted_text = None, decrypted_text = decrypted_text)





#======== Substitution Cipher Routes =========#

# Loads the Substitution Cipher Page
@app.route('/substitution')
def substitution_page():
    return render_template('substitution_page.html', encrypted_text = None, decrypted_text = None)



# Loads the Substitution Cipher Page, when the user has entered text to be encrypted
@app.route('/substitution/encrypt/', methods=['GET', 'POST'])
def substitution_encrypt_input():
    # Gets data from form
    input_text          = request.args['input_text']
    input_substitution  = request.args['input_substitution']
    substitution_func = {"ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]: input_substitution[i] for i in range(26)}

    # runs encryption function
    encrypted_text = encrypt.encrypt_substitution(input_text, substitution_func)
    return render_template('substitution_page.html', encrypted_text = encrypted_text, decrypted_text = None)



# Loads the Substitution Cipher Page, when the user has entered text to be encrypted
@app.route('/substitution/decrypt/', methods=['GET', 'POST'])
def substitution_decrypt_input():
    # Gets data from form
    input_text    = request.args['input_text']

    # runs decryption function
    decrypted_text = test_n_gram.break_substitution(input_text, 5)
    return render_template('substitution_page.html', encrypted_text = None, decrypted_text = decrypted_text)






#======== Vignere Cipher Routes =========#

# Loads the Vignere Cipher Page
@app.route('/vignere')
def vignere_page():
    return render_template('vignere_page.html', encrypted_text = None)



# Loads the Vignere Cipher Page, when the user has entered text to be encrypted
@app.route('/vignere/encrypt/', methods=['GET', 'POST'])
def vignere_encrypt_input():
    # Gets data from form
    input_text     = request.args['input_text']
    input_keyword  = request.args['input_keyword']

    # runs encryption function
    encrypted_text = encrypt.encrypt_vignere(input_text, input_keyword)
    return render_template('vignere_page.html', encrypted_text = encrypted_text)
