# IMPORTANT: CHANGE ALL ELEMENTS WITH '$'
# REMEMBER THAT YOU HAVE TO CHANGE ALSO THE JSON FILE


import botogram
import sqlite3
import os
from obj.jsonr import p
from obj.visualizers import visualizer, staffvis, verdict
from obj.checks import checklink, check2, knowit, checkperm
bot = botogram.create(p["values"]["token"])
# Set your token in the json $
dat = sqlite3.connect('data/dat1.db', timeout=0)
d = dat.cursor()

d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
d.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY, type INTEGER)")
d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER PRIMARY KEY)')
dat.commit()
# type=0(global admin bot) type=1(staff group) type2=(log channel) type=3(public group) type=4(channel)
# stage=0(ready to do a request) stage=1(just typed /request) stage=2(gave the name of the apk) stage=3(he have to confirm all) stage=4(examinating) stage=5(voting) stage=6(approved) stage=7(soddisfacted and to delete)
bot.owner = "@Mamiglia & https://github.com/Mamiglia/Requester-Bot"
# $

req = (input('Are requests open?[Y,N,X] ')).lower()
if req == 'y':
    print('Ok the Bot is open to 20 requests')
    global door
    door = 20
elif req == 'x':
    while True:
        n = input('How many requests? ')
        try:
            door = int(n)
            break
        except ValueError:
            print('Insert a valid Number')
else:
    print('the Bot isn\'t open to any request')
    door = 0


def checkreq(prim, typ):
    if door > 0:
        try:
            d.execute("INSERT INTO request (userid, type) VALUES (?,?)", (prim.id, typ))
            dat.commit()
            return True
        except sqlite3.IntegrityError:
            prim.send(p["checkreq"][0])
            return False
    else:
        prim.send(p["checkreq"][1])


@bot.command('start')
def start(chat, message):
    chat.send(p["start"] % (message.sender.first_name))


@bot.command('help')
def help(chat, message):
    chat.send(p["help"])


@bot.command('rules')
def rules(chat, message):
    chat.send(p["rules"])


@bot.command('adminhelp')
def adminhelp(message, chat):
    if checkperm(message.sender.id):
        chat.send("these are the commands that only an admin can perform:\
-/delete @username: delete the user's request\
-/cleanreq : delete all the requests\
-/door : change the number of requests that the bot can have\
-/newadmin Your_password : set you as a new admin\
-/setstaff : type in the staff group to set the staff group\
-/setgroup : type in your group to set it\
-/setlogchannel : type in your log group to set it")

        
@bot.command("delete")
def deletereq(message, chat):
    if checkperm(message.sender.id):
        username = message.text[8::]
        d.execute("DELETE FROM request WHERE username=?", (username, ))
        dat.commit()
        chat.send("Deleted >:c")
        #add a check feature


@bot.command("cleanreq", hidden=True)
def cleanreq(message, chat):
    if checkperm(message.sender.id):
        chat.send('cleaning..')
        d.execute("DROP TABLE IF EXISTS request")
        d.execute("DROP TABLE IF EXISTS mess")
        d.execute("VACUUM")
        d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
        d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER PRIMARY KEY)')
        chat.send('Done!')
        dat.commit()


@bot.command("cleanall", hidden=True)
def ooo(message, chat):
    if checkperm(message.sender.id):
        chat.send('cleaning..')
        d.execute("DROP TABLE IF EXISTS request")
        d.execute("DROP TABLE IF EXISTS mess")
        d.execute("DROP TABLE IF EXISTS ids")
        d.execute("VACUUM")
        d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
        d.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY, type INTEGER)")
        d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER PRIMARY KEY)')
        dat.commit()
        chat.send('all proofs cleared ;)')


@bot.command("door", hidden=True)
def hhh(message, chat):
    if checkperm(message.sender.id):
        try:
            door = int(message.text[5::])
            chat.send('Now I\'m open to %s requests' % (door))
        except ValueError:
            chat.send('Insert a valid number')


@bot.command("oliodipalmas", hidden=True)
def easteregg(chat, message):
    # $ Put at least one easter egg or you're dead to me
    chat.send(p["easteregg"])


@bot.command("newadmin", hidden=True)
def newadmin(chat, message):
    # remember to set your password
    if p["values"]["password"] in message.text:
        d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (message.sender.id, 0))
        chat.send("W-welcome home S-Senpai!")
        dat.commit()
    else:
        chat.send("Who is this CONSOLE-PEASANT??")


@bot.command("setstaff", hidden=True)
def staff(chat, message):
    if chat.type == "supergroup":
        if checkperm(message.sender.id):
            d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (chat.id, 1))
            chat.send("Staff Group correctly set!")
            dat.commit()
        else:
            chat.send("I need to receive the command from an important guy, not a console peasant as you")
    else:
        chat.send("I should be in a Supergroup, wrong chat!")


@bot.command("setgroup", hidden=True)
def setgroup(chat, message):
    if chat.type == "supergroup":
        if checkperm(message.sender.id):
            d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (chat.id, 3))
            chat.send("Group correctly set!")
            dat.commit()
        else:
            chat.send("I need to receive the command from an important guy, not a console peasant as you")
    else:
        chat.send("I should be in a Supergroup, wrong chat!")


@bot.command("setlogchannel", hidden=True)
def setilogchannel(chat, message):
    if chat.type == "supergroup":
        if checkperm(message.sender.id):
            d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (chat.id, 2))
            chat.send("Log Channel correctly set!")
            dat.commit()
        else:
            chat.send("I need to receive the command from an important guy, not a console peasant as you")
    else:
        chat.send("I should be in a Supergroup, wrong chat!")
# one day this will be a Channel


@bot.command("request")
def first(message, chat):
    """Make Your Request!"""
    if chat.type == "private":
        if checkreq(chat, 'request') is True:
            bt = botogram.Buttons()
            bt[0].callback(p["request"][0], "zero")
            chat.send(p["request"][1], attach=bt)


@bot.command(p["values"]["request2"])
def second(message, chat):
    '''Request something different'''
    if chat.type == "private":
        if checkreq(chat, p["values"]["request2"]) is True:
            bt = botogram.Buttons()
            bt[0].callback(p["request"][0], "zero")
            chat.send(p["request"][2], attach=bt)


@bot.process_message
def stager(chat, message):
    if chat.type == "private":
        d.execute("SELECT stage FROM request WHERE userid=?", (chat.id, ))
        try:
            stage = int(d.fetchone()[0])
            if stage == 1:
                bt = botogram.Buttons()
                chat.send(p["stager"]["1"][0])
                d.execute("UPDATE request SET stage=2, name=? WHERE userid=?", (message.text, chat.id))
                bt[0].callback(p["stager"]["1"][1], "rename")
                bt[1].callback(p["stager"]["1"][2], 'void')
                chat.send(p["stager"]["1"][3], attach=bt)
            elif stage == 2:
                try:
                    d.execute("SELECT link FROM request WHERE userid=?", (chat.id, ))
                    if d.fetchone()[0] is None:
                        chat.send(p["stager"]["2"][0])
                        applink = str(message.parsed_text.filter("link")[0])
                        res = checklink(applink)
                    else:
                        applink = 'No link'
                        res = True
                    if res:
                        bt = botogram.Buttons()
                        d.execute("UPDATE request SET link=?, username=?, nameuser=?, userid=?, stage=3 WHERE userid=?", (applink, message.sender.username, message.sender.name, message.sender.id, chat.id))
                        bt[0].callback(p["stager"]["2"][1], "relink", str(message.sender.id))
                        bt[1].callback(p["stager"]["2"][2], "zero", str(message.sender.id))
                        bt[1].callback(p["stager"]["2"][3], 'confirm', str(message.sender.id))
                        chat.send(visualizer(chat), syntax="markdown", attach=bt)
                        dat.commit()
                    else:
                        chat.send(p["stager"]["2"][4])
                except IndexError:
                    chat.send(p["stager"]["2"][4])
            elif stage == 3:
                chat.send(p["stager"]["3"][0])
            elif stage == 4:
                chat.send(p["stager"]["4"][0])
            elif stage == 5:
                chat.send(p["stager"]["5"][0])
            elif stage == 6:
                chat.send(p["stager"]["6"][0])
            else:
                chat.send(p["stager"]["err"][0])
        except TypeError:
            chat.send(knowit(door))
        dat.commit()
        return True


@bot.callback("rename")
def rename(chat, message):
    d.execute("UPDATE request SET stage=1 WHERE userid=?", (chat.id, ))
    dat.commit()
    chat.send(p["rename"])


@bot.callback("relink")
def relink(chat, message, data):
    d.execute("UPDATE request SET stage=2 WHERE userid=?", (chat.id, ))
    dat.commit()
    message.edit(p["relink"])


@bot.callback('void')
def void(message, chat):
    d.execute('UPDATE request SET link=? WHERE userid=?', ('void', chat.id))
    chat.send(p["void"])
    dat.commit()


@bot.callback("zero")
def zero(chat, message, data):
    d.execute("DELETE FROM request WHERE userid=?", (chat.id, ))
    dat.commit()
    message.edit(p["zero"])


@bot.callback("zero2")
def zero2(chat, message, data):
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    dat.commit()
    message.delete()
    bot.chat(int(data)).send(p["zero2"])


@bot.callback("confirm")
def confirm(chat, message, data):
    global door
    door += -1
    bt = botogram.Buttons()
    d.execute('UPDATE request SET stage=4 WHERE userid=?', (chat.id, ))
    dat.commit()
    d.execute("SELECT id FROM ids WHERE type=1")
    staffs = d.fetchone()
    bt[0].callback(p["confirm"][0], "refuse", str(chat.id))
    bt[1].callback(p["confirm"][1], "good", str(chat.id))
    bt[2].callback(p["confirm"][2], "vote", str(chat.id))
    message.edit(p["confirm"][3])
    for group in staffs:
        bot.chat(group).send(staffvis(str(chat.id)), attach=bt)


@bot.callback("refuse")
def refuse(chat, message, data):
    message.edit(verdict(int(data), False))
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    bot.chat(int(data)).send(p["refuse"])
    dat.commit()


@bot.callback("vote")
def groupvote(chat, message, data):
    bot.chat(int(data)).send(p["vote"])
    message.edit(verdict(int(data), 'vote'))
    d.execute('UPDATE request SET stage=5 WHERE userid=?', (int(data), ))
    dat.commit()
    d.execute("SELECT id FROM ids WHERE type=3")
    groups = d.fetchone()
    bt = botogram.Buttons()
    bt[0].callback('start', 'startpoll', data)
    for group in groups:
        bot.chat(group).send("New Poll by %s" % (data), attach=bt)


@bot.callback("good")
def good(chat, message, data):
    message.edit(verdict(int(data), True))
    bot.chat(int(data)).send(p["good"][0])
    d.execute('UPDATE request SET stage=6 WHERE userid=?', (int(data), ))
    dat.commit()
    d.execute("SELECT id FROM ids WHERE type=2")
    ch = d.fetchone()
    bt = botogram.Buttons()
    bt[0].callback(p["good"][1], 'zero2', data)
    for channel in ch:
        bot.chat(channel).send(staffvis(data), attach=bt)


@bot.callback('op')
def operation(chat, message, query, data):
    d.execute('SELECT user FROM mess WHERE mesid=?', (message.message_id, ))
    users = d.fetchall()
    if users == [] or check2(users, query.sender.id):
        d.execute('SELECT votes, userid FROM request WHERE mesid=?', (message.message_id, ))
        ex = d.fetchone()
        vote = ex[0] + int(data)
        userid = ex[1]
        # set how many votes are needed for the request to be approved$
        if vote == 20:
            d.execute('DELETE FROM mess WHERE mesid=?', (message.message_id, ))
            good(chat, message, userid)
            message.edit(p["op"][0])
        elif vote == -20:
            message.edit(p["op"][1])
            zero(chat, message, userid)
            d.execute('DELETE FROM mess WHERE mesid=?', (message.message_id, ))
        else:
            d.execute('UPDATE request SET votes=? WHERE mesid=?', (vote, message.message_id))
            d.execute('INSERT INTO mess VALUES (?,?)', (message.message_id, query.sender.id))
            dat.commit()
            query.notify(p["op"][2])
            qtvis(chat, message, userid)
    else:
        query.notify(p["op"][3])


@bot.callback('startpoll')
def startpoll(chat, message, data):
    d.execute('UPDATE request SET mesid=? WHERE userid=?', (message.message_id, int(data)))
    dat.commit()
    qtvis(chat, message, data)


@bot.callback('qtvis')
def qtvis(chat, message, data):
    d.execute("SELECT * FROM request WHERE userid=?", (int(data), ))
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    userid = int(data)
    nameuser = ex[4]
    ur = ex[6]
    vote = ex[7]
    bt = botogram.Buttons()
    bt[0].callback('+1', 'op', str(+1))
    bt[0].callback('-1', 'op', str(-1))
    message.edit(p["qtvis"] % (ur, nameuser, userid, name, lnk, vote), preview=False, attach=bt)


works = os.cpu_count()
bot.run(workers=works)
dat.commit()

if __name__ == "__main__":
    bot.run()

# excel
