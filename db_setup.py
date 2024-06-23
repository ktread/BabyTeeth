import sqlite3
con = sqlite3.connect("baby.db")

cur = con.cursor()

#type = pee/poo/both
cur.execute("CREATE TABLE diaper(type, timestamp)")
#side = left or right breast, amount pumped = ounces (weight) #type= breast/bottle
cur.execute("CREATE TABLE eating(type, side, start_timestamp, amount)")
# sleep = sleep_type = asleep/awake, wake_type = how woken up
cur.execute("CREATE TABLE sleep(sleep_type, wake_type, timestamp)")

con.commit()