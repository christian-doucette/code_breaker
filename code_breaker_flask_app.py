from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home_page.html')


@app.route('/caesar')
def caesar_page():
    return render_template('caesar_page.html')



@app.route('/substitution')
def substitution_page():
    return render_template('substitution_page.html')


@app.route('/vignere')
def vignere_page():
    return render_template('vignere_page.html')
