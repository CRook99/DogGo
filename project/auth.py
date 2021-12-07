from flask import Flask, render_template, request, url_for, redirect, g, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import re
import database as db
from dog_class import Dog

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
            try:
                user = db.execute_query("SELECT email, password FROM user WHERE email = ?", (email,))[0] # Tries to find a user with given email
                if check_password_hash(user[1], password):  # 1 = index of password value // Evaluates hashed given password against hashed stored password
                    print("Successful login")
                    return render_template('dogs/list.html') # Will redirect to feed
                else:
                    flash("Incorrect password")
            except:
                flash(f"User with email {email} not found")



    return render_template('auth/login.html', title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = "Register"
    if request.method == "POST":
        email = request.form["email"]
        telephoneNo = request.form["telephoneNo"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        error = None
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
                    db.execute_query("INSERT INTO user VALUES (NULL, ?, ?, ?)", (email, generate_password_hash(password), telephoneNo))
                    return render_template('auth/login.html')
                else:
                    flash(error, 'error')

    return render_template('auth/register.html')


@app.route('/')
def index():
    return redirect(url_for('editDog'))

@app.route('/dogs', methods=['GET', 'POST'])
def dogList():
    title = "My Dogs"
    dogs = []
    dog = Dog('Scout', 7, 'M', 'Chocolate Labrador', False, '01/01/11', 'East Sussex')
    dogs.append(dog)
    #dog = Dog('Fooge', 11, 'M', 'Bonzai!', True, '02/02/22', 'Sussey')
    #dogs.append(dog)
    return render_template('dogs/list.html', dogs=dogs)

@app.route('/edit', methods=['GET', 'POST'])
def editDog():
    title = "Editing"
    return render_template('dogs/edit.html')


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
    app.run(debug = True)