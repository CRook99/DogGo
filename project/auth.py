from flask import Flask, render_template, request, url_for, redirect, g
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db
import sqlite3
import os
import re

app = Flask(__name__)
app.config.from_mapping(DATABASE = os.path.join(app.instance_path, 'schema.sql'))


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
        email = request.form["email"]
        telephoneNo = request.form["telephoneNo"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        if request.form["register_button"] == "register":
            if validateEmail(email):
                con = sqlite3.connect('database.db')
                con.execute("INSERT INTO user (email, telephoneNo, password) VALUES (?, ?, ?)", (email, telephoneNo, generate_password_hash(password)))
            else:
                pass
    return render_template('auth/register.html')


@app.route('/')
def index():
    #return render_template('auth/index.html')
    return redirect(url_for('login'))


def validateEmail(email):
    return not (re.search(r"[^@]{1,64}@[^@]{1,253}\.[^@]{2,}", email) == None)
    # Regex expression to check whether submitted email follows conventions
    # [^@]{1,64} finds a recipient name of maximum 64 characters
    # @ finds the required @ symbol that separates the name and domain
    # [^@]{1,253} finds a domain of maximum 253 characters
    # \. finds the required . symbol that separates the domain and top-level domain
    # [^@]{2,} finds the top-level domain of minimum 2 characters


def validatePassword(password):
    return not (re.search(r"\d[A-Z]{8,32}", password) == None) # TODO fix


def matchPasswords(password, confirmPassword):
    return password == confirmPassword # Returns whether the first password and the confirmation password match


if __name__ == '__main__':
    print(validateEmail("test@test.com"))
    print(validateEmail("test@test.co"))
    print(validateEmail("test@test.c"))
    print("\n")
    print(validatePassword("Password1")) # Valid
    print(validatePassword("Pass1")) # Short
    print(validatePassword("Passwordpasswordpasswordpassword1")) # Long
    print(validatePassword("password1")) # No cap
    print(validatePassword("Passwordpassword")) # No num
    app.run(debug = True)