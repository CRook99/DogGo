import sqlite3

from flask import current_app, g

def execute_query(query, params):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    fetch = cur.fetchall()
    con.close()
    return fetch
