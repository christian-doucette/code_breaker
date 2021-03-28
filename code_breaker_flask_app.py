# flask imports
from flask import Flask, render_template, request

# sqlite3 for database
import sqlite3
import sys


# My code files
import encrypt



app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/caesar')
def caesar_page():
    print('This is standard output (page without form)', file=sys.stdout)

    return render_template('caesar_page.html', encrypted_text = None, decrypted_text = None)

@app.route('/caesar/encrypt/', methods=['GET', 'POST'])
def caesar_encrypt_input():
    print('This is standard output', file=sys.stdout)
    # Gets data from form
    input_text = request.form['input_text']
    input_rot  = int(request.form['input_rot'])

    encrypted_text = encrypt.encrypt_caesar(input_text, input_rot)
    return render_template('caesar_page.html', encrypted_text = encrypted_text, decrypted_text = None)



@app.route('/substitution')
def substitution_page():
    return render_template('substitution_page.html')


@app.route('/vignere')
def vignere_page():
    return render_template('vignere_page.html')
