# flask imports
from flask import Flask, render_template, request

# sqlite3 for database
import sqlite3


# My code files
import encrypt
import test_n_gram



app = Flask(__name__)


#=================================#
#             Routes              #
#=================================#

# Loads Home Page, with brief description of the project
@app.route('/')
def home_page():
    return render_template('home_page.html')




# Loads the Caesar Cipher Page
@app.route('/caesar')
def caesar_page():
    return render_template('caesar_page.html', encrypted_text = None, decrypted_text = None)




# Loads the Caesar Cipher Page, when the user has entered text to be encrypted
@app.route('/caesar/encrypt/', methods=['GET', 'POST'])
def caesar_encrypt_input():
    # Gets data from form
    input_text = request.form['input_text']
    input_rot  = int(request.form['input_rot'])

    encrypted_text = encrypt.encrypt_caesar(input_text, input_rot)
    return render_template('caesar_page.html', encrypted_text = encrypted_text, decrypted_text = None)




# Loads the Caesar Cipher Page, when the user has entered text to be decrypted
@app.route('/caesar/decrypt/', methods=['GET', 'POST'])
def caesar_decrypt_input():
    # Gets data from form
    input_text = request.form['input_text']

    decrypted_text = test_n_gram.break_caesar(input_text, 5)
    return render_template('caesar_page.html', encrypted_text = None, decrypted_text = decrypted_text)




@app.route('/substitution')
def substitution_page():
    return render_template('substitution_page.html')


@app.route('/vignere')
def vignere_page():
    return render_template('vignere_page.html')