import sqlite3
con = sqlite3.connect("baby.db")

cur = con.cursor()

#type = pee/poo/both
cur.execute("CREATE TABLE diaper(type, timestamp)")
#side = left or right breast, amount pumped = ounces (weight)
cur.execute("CREATE TABLE pumping(side, start_timestamp,end_timestamp, amount_pumped)")
# type = breast/bottle, side = if breast - which side
cur.execute("CREATE TABLE feeding(type, side, start_timestamp, end_timestamp)")
# sleep
cur.execute("CREATE TABLE sleep(start_timestamp, end_timestamp)")

con.commit()