import sqlite3
con = sqlite3.connect("baby.db")

cur = con.cursor()

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())