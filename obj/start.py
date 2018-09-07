import redis
import sqlite3
import botogram
from .jsonr import p
dat = sqlite3.connect('data/dat1.db')
d = dat.cursor()
d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
dat.commit()
# core database of the bot, it has in it all the requests and useful informations
# stage=0(ready to do a request) stage=1(just typed /request) stage=2(gave the name of the apk) stage=3(he have to confirm all) stage=4(examinating) stage=5(voting) stage=6(approved) stage=7(soddisfacted and to delete) stage=13(BANNED)
d.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY, username TEXT, type INTEGER)")
dat.commit()
# database that stores in it all the ids, the admins, the groups
# type=0(global admin bot) type=1(staff group) type=2(log channel) type=3(public group)
d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER)')
# database useful to check who already voted the poll
dat.commit()

try:
    r = redis.StrictRedis(host=p["values"]["redisHost"], port=6379, db=0, password=p["values"]["redisPass"], socket_connect_timeout=10)
except redis.exceptions.TimeoutError:
    print('WARNING - Redis not connected')
r.ping()

# For the first thing when booting up, the bot will ask you if the requests are open
req = (input('Are requests open?[Y,N,X] ')).lower()
if req == 'y':
    r.set('door', 20)
    print('Ok the Bot is open to 20 requests')
elif req == 'x':
    while True:
        n = input('How many requests? ')
        try:
            r.set('door', int(n))
            break
        except ValueError:
            print('Insert a valid Number')
else:
    print('the Bot isn\'t open to any request')
    r.set('door', 0)

r.set('votes', 5)
# set the votes that a request needs to be approved $

d.execute('SELECT type, username FROM ids')
i = d.fetchall()
try:
    # check if there are admins
    for x in i:
        if 0 == x[0]:
            break
    else:
        print("WARNING - No admins found!")
    # check if there is a staff group
    for x in i:
        if 1 == x[0]:
            break
    else:
        print("WARNING - void Staff Group")
    # check if there is a log channel
    for x in i:
        if 2 == x[0]:
            chn = x[1]
            logch = botogram.channel(chn, p["values"]["token"])
            break
    else:
        print("WARNING - void Log Channel")
        logch = None
    # check if there is a public group
    for x in i:
        if 3 == x[0]:
            break
    else:
        print("WARNING - void Public Group")
except TypeError:
    print('WARNING - everything is missing!')

'''End of Starting processes'''
