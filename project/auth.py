from flask import Flask, render_template, request, url_for, redirect, g, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import re

app = Flask(__name__)
app.config.from_mapping(DATABASE = os.path.join(app.instance_path, 'schema.sql'))
app.secret_key = 'dev'


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Log In"
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if request.form["login_button"] == "login":
            print("Opened db successfully")

            #con = sqlite3.connect('database.db')
            #user = con.execute("SELECT (email, password) FROM user WHERE email = ?", (email)).fetchone()

            #if check_password_hash(user['password'], password):
            #    print("Successful login")

    return render_template('auth/login.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        error = None
        email = request.form["email"]
        telephoneNo = request.form["telephoneNo"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        if request.form["register_button"] == "register":

            empty = False
            if not email:
                flash('Email required', 'empty')
                empty = True
            if not telephoneNo:
                flash('Telephone number required', 'empty')
                empty = True
            if not password:
                flash('Password required', 'empty')
                empty = True
            if not confirmPassword:
                flash('Re-enter password', 'empty')
                empty = True

            if not empty:
                print("Boxes filled")
                if not validateEmail(email):
                    error = 'Invalid email'
                elif not validateTel(telephoneNo):
                    error = 'Invalid telephone number'
                elif not validatePassword(password):
                    error = 'Invalid password - password must contain one capital letter, one digit, and be between 8-32 characters'
                elif not matchPasswords(password, confirmPassword):
                    error = 'Passwords do not match'

                if error is None:
                    con = sqlite3.connect('database.db')
                    con.execute("INSERT INTO user (email, telephoneNo, password) VALUES (?, ?, ?)", (email, telephoneNo, generate_password_hash(password)))
                    con.close()
                else:
                    flash(error, 'error')





    return render_template('auth/register.html')


@app.route('/')
def index():
    return redirect(url_for('login'))


def validateEmail(email):
    return not (re.search(r"[^@]{1,64}@[^@]{1,253}\.[^@]{2,}", email) is None)
    # Regex expression to check whether submitted email follows conventions
    # [^@]{1,64} finds a recipient name of maximum 64 characters
    # @ finds the required @ symbol that separates the name and domain
    # [^@]{1,253} finds a domain of maximum 253 characters
    # \. finds the required . symbol that separates the domain and top-level domain
    # [^@]{2,} finds the top-level domain of minimum 2 characters


def validatePassword(password):
    valid = True
    #if re.search(r"\d(?=.*[A-Z])(^.{8,32}$)", password) is None:
    #    valid = False
    if ((re.search(r"\d", password) is None) or (re.search(r"(?=.*[A-Z])", password) is None) or (re.search(r"^.{8,32}$", password) is None)):
        valid = False
    return valid

def validateTel(tel):
    tel = tel.replace(' ','') # Removes whitespace
    return not (re.search(r"^0[0-9]{10}$", tel) is None)


def matchPasswords(password, confirmPassword):
    return password == confirmPassword # Returns whether the first password and the confirmation password match


if __name__ == '__main__':
    print(validateTel("07465 400040"))
    print(validateTel("07465    400040"))
    print(validateTel("07465 40004"))
    print(validateTel("17465 400040"))
    app.run(debug = True)