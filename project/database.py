import sqlite3

from flask import current_app, g

def execute_query(query, params = None, type = 'multi'):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    if params is not None:
        cur.execute(query, params)
    else:
        cur.execute(query)
    con.commit()
    if type == 'single':
        fetch = cur.fetchone()
    elif type == 'multi':
        fetch = cur.fetchall()
    else:
        fetch = 'Bad type param'
    con.close()
    return fetch
