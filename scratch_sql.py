import sqlite3
import config as c
import datetime as dt

con = sqlite3.connect("baby.db")
cur = con.cursor()
#
res = cur.execute("SELECT * FROM eating")
print(res.fetchall())

