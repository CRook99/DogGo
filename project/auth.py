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
        email = request.form.get("email")
        password = request.form.get("password")
        if request.form.get("login_button") == "login":
            con = sqlite3.connect('database.db')
            print("Opened db successfully")
            user = con.execute("SELECT (email, password) FROM user WHERE email = ?", (email)).fetchone()

            if check_password_hash(user['password'], password):
                print("Successful login")

    return render_template('auth/login.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        telephoneNo = request.form.get("telephoneNo")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")
        if request.form.get("login_button") == "login":
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
    return not (re.search(r"[^@]+@[^@]+\.[^@]+", email) == None) # Regex expression to check whether submitted email follows conventions


def validatePassword(password):
    return not (re.search(r"/(.*[A-Z].*)(.*\d.*)(^.{8,32})/", password) == None) # TODO fix


def matchPasswords(password, confirmPassword):
    return password == confirmPassword # Returns whether the first password and the confirmation password match


if __name__ == '__main__':
    print(validateEmail("test@test.com"))
    print(validatePassword("Short1"))
    print(validatePassword("Longlonglonglonglonglonglonglong1"))
    print(validatePassword("capitalletter1"))
    print(validatePassword("Nonumber"))
    print(validatePassword("Validpass1"))
    app.run(debug = True)