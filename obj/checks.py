import sqlite3
from .jsonr import p
dat = sqlite3.connect('data/dat1.db', timeout=0)
d = dat.cursor()


def checklink(lnk):
    if p["values"]["link"] in lnk:
        return True
    else:
        return False


def check2(userlist, usr):
    for row in userlist:
        if usr in row:
            return False
            break
    else:
        return True


def knowit(r):
    if r > 0:
        return p["knowit"][0]
    elif r <= 0:
        return p["knowit"][1]


def checkperm(i):
    d.execute("SELECT id FROM ids WHERE type=0")
    admins = d.fetchall()
    for adm in admins:
        if i in adm:
            return True
            break
    else:
        return False
