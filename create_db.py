import sqlite3

con = sqlite3.connect('site_bd.sqlite')
cur = con.cursor()
with open('create_db.sql', 'r') as f:
    text = f.read()
cur.executescript(text)
cur.close()
con.close()
