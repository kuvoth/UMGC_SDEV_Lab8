"""Main python application used to run a web server locally using Flask"""
# Devin Bulawa
# SDEV 300 6381
# 7/2/2024
from datetime import datetime
import re

from flask import Flask, render_template, flash, request, session, url_for, redirect
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key='12345'


@app.route('/')
def index():
    """Displays the template for the index page"""

    return render_template("index.html", datetime=str(datetime.now().strftime("%B %d, %Y %I:%M%p")))


@app.route('/parts')
def home():
    """Displays the template for the parts page"""

    return render_template("parts.html", datetime=str(datetime.now().strftime("%B %d, %Y %I:%M%p")))


@app.route('/FAQ')
def faq():
    """Displays the template for the FAQ page"""

    return render_template("FAQ.html", datetime=str(datetime.now().strftime("%B %d, %Y %I:%M%p")))


@app.route('/register', methods=["GET", "POST"])
def register():
    """Displays the template for the register page as well as
    provides the code for writing info to a passfile and error checking"""
    error = None
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "" and password == "":
            error = "Please enter a username and a password".split('\n')
        elif username == "":
            error = "Please enter a username".split('\n')
        elif password == "":
            error = "Please enter a password".split('\n')
        elif password_check(password) is not None:
            error = ("Password must be at least 12 characters in length and must include:"
                     "\nAt least 1 digit"
                     "\nAt least 1 uppercase letter"
                     "\nAt least 1 lowercase letter"
                     "\nAt least 1 special character").split('\n')
        else:
            with open('passfile.txt', "a", encoding='UTF-8') as f:
                hash_pass = sha256_crypt.hash(password)
                f.write(username + "," + hash_pass + "\n")
            flash('Successfully registered!')
    return render_template("register.html", error=error)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Displays the template for the login page and reads info from
    a passfile to allow for logging in using registered info"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        index1 = 0
        index2 = 0

        with open('passfile.txt', 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                index1 += 1
        with open('passfile.txt','r', encoding='UTF-8') as f:
            for line in f.readlines():
                info = line.strip().split(',')
                hash_pass = info[1]
                if username == info[0] and not sha256_crypt.verify(password, hash_pass):
                    flash("Incorrect Password")
                elif username == info[0] and sha256_crypt.verify(password, hash_pass):
                    flash('Login successful')
                else:
                    index2 += 1
                    if index1 == index2:
                        flash('Incorrect username and password')
    return render_template("login.html")


@app.route('/pass_update', methods=["GET", "POST"])
def pass_update():
    if request.method == "POST":
        username = request.form.get('username')
        new_password = request.form.get('new_password')


def password_check(password):
    """Checks to see if the password entered meets the requirements
    for password complexity"""
    error = None
    length_error = len(password) < 12
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"\W", password) is None

    if length_error or digit_error or uppercase_error or lowercase_error or symbol_error:
        error = ""
    return error
