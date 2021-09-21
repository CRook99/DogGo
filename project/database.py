import sqlite3

from flask import current_app, g

def get_db():
    if 'db' not in g:
        return sqlite3.connect('schema.sql')

def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as data_file:
        db.executescript(data_file.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db())

