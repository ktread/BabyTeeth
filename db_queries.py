import sqlite3
import config as c
import datetime as dt


def write_row(screen_state, **kwargs):
    con = sqlite3.connect("baby.db")
    cur = con.cursor()
    if screen_state == c.PAGE_HOW:
        write_how(cur, **kwargs)
    if screen_state == c.PAGE_HOW_MUCH:
        write_how_much(cur, **kwargs)
    if screen_state == c.PAGE_INITIAL:
        write_how(cur, **kwargs)
    con.commit()
    con.close()


def write_how(cur, **kwargs):
    for k,v in kwargs.items():
        print(k,v)
    # data = [(sleep_type, wake_type, dt.datetime.now())]
    # cur.executemany("""INSERT INTO sleep VALUES (?, ?, ?)""",data)

def write_how_much(cur, **kwargs):
    for k,v in kwargs.items():
        print(k,v)
    # data = [(feed_type, side, dt.datetime.now(), amount)]
    # cur.executemany("""INSERT INTO eating VALUES (?, ?, ?, ?)""", data)

def write_diaper(cur, **kwargs):
    for k,v in kwargs.items():
        print(k,v)
    # data = [(diaper_type, dt.datetime.now())]
    # cur.execute("""INSERT INTO diaper VALUES (?, ?)""",data)
