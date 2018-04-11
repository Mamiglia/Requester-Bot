import sqlite3
from .jsonr import p
dat = sqlite3.connect('data/dat1.db', timeout=0)
d = dat.cursor()


def checklink(lnk):
    '''Check if the link is valid, set your specific link if needed (data/lang.json)'''
    if p["values"]["link"] in lnk:
        return True
    else:
        return False


def check2(userlist, usr):
    '''Check if the user is in a list of users, useful to know if that user alreday make a request'''
    for row in userlist:
        if usr in row:
            return False
            break
    else:
        return True


def knowit(r):
    '''check if requests are open'''
    if r > 0:
        return p["knowit"][0]
    elif r <= 0:
        return p["knowit"][1]


def checkperm(i):
    '''Check if the user is in the admins list'''
    d.execute("SELECT id FROM ids WHERE type=0")
    admins = d.fetchall()
    for adm in admins:
        if i in adm:
            return True
            break
    else:
        return False

