from flask import Flask, render_template, request, url_for, redirect, g
from werkzeug.security import check_password_hash, generate_password_hash
from database import get_db
import sqlite3
import os
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
        if request.form.get("login_button") == "login":
            con = sqlite3.connect('database.db')
            con.execute("INSERT INTO user (email, telephoneNo, password) VALUES (?, ?, ?)", (email, telephoneNo, generate_password_hash(password)))
    return render_template('auth/register.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)