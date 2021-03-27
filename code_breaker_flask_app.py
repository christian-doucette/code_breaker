from flask import Flask
import sqlite3


app = Flask(__name__)

@app.route('/')
def home_page():
    return 'This is the home page!'


@app.route('/caesar')
def caesar_page():
    return 'Caesar cipher page'



@app.route('/substitution')
def substitution_page():
    return 'Substitution cipher page'


@app.route('/vignere')
def vignere_page():
    return 'Vignere cipher page'
