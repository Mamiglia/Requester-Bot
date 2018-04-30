import sqlite3
from .jsonr import p
dat = sqlite3.connect('data/dat1.db')
d = dat.cursor()


def visualizer(ch):
    '''The message that will be sent to the user with a recap of what he requested'''
    d.execute("SELECT * FROM request WHERE userid=?", [ch.id])
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    tosend = (p["visualizer"] % (name, lnk))
    return tosend


def staffvis(userid):
    '''The message that will be sent to the staff group, it will include the name, and the id of the user'''
    d.execute("SELECT * FROM request WHERE userid=?", (int(userid), ))
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    nameuser = ex[4]
    ur = ex[6]
    tosend = (p["staffvis"][0] % (ur, nameuser, userid, name, lnk))
    return tosend


def verdict(userid, what):
    '''message that will be sent to the user to let him know wheter his request has been accepted'''
    d.execute("SELECT * FROM request WHERE userid=?", (userid, ))
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    nameuser = ex[4]
    if what is True:
        tosend = (p["verdict"][0] % (nameuser, userid, name, lnk))
    elif what is False:
        tosend = (p["verdict"][1] % (nameuser, userid, name, lnk))
    else:
        tosend = (p["verdict"][2] % (nameuser, userid, name, lnk))
    return tosend
