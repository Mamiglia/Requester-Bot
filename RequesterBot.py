# IMPORTANT: CHANGE ALL ELEMENTS WITH '$'

import botogram
import sqlite3
bot = botogram.create("$YOUR-API-KEY")
dat = sqlite3.connect('dat1.db', timeout=0)
d = dat.cursor()
# d.execute("DROP TABLE IF EXISTS request")
# d.execute("DROP TABLE IF EXISTS mess")
# d.execute("DROP TABLE IF EXISTS ids")
# d.execute("VACUUM")
d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
d.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY, type INTEGER)")
d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER PRIMARY KEY)')
dat.commit()
# type=0(global admin bot) type=1(staff group) type2=(log channel) type=3(public group) type=4(channel)
# stage=0(ready to do a request) stage=1(just typed /request) stage=2(gave the name of the request) stage=3(he have to confirm all) stage=4(examinating) stage=5(voting) stage=6(approved) stage=7(soddisfacted and to delete)
bot.before_help = ['Welcome to the Request Bot of @$channel']
bot.after_help = ['Be sure to read the rules before requesting $something']
bot.about = "This Bot helps you to request $something to the $channel"
bot.owner = "@$yourusername & https://github.com/Mamiglia/Requester-Bot"

req = (input('Are requests open?[Y,N,X]  ')).lower()
if req == 'y':
    print('Ok the Bot is open to 20 requests')
    door = 20
elif req == 'x':
    while True:
        n = input('How many requests?  ')
        try:
            door = int(n)
            break
        except ValueError:
            print('Insert a valid Number')
else:
    print('the Bot isn\'t open to any request')
    door = 0
global door


def visualizer(ch):
    d.execute("SELECT * FROM request WHERE userid=?", [ch.id])
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    tosend = ("Are you sure? Do you wanna request [%s](%s)?" % (name, lnk))
    return tosend


def staffvis(userid):
    d.execute("SELECT * FROM request WHERE userid=?", (int(userid), ))
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    username = ex[3]
    nameuser = ex[4]
    ur = ex[6]
    if username is None:
        tosend = ("#%s\nThe user [%s](tg://user?id=%s) has requested:\n%s\n%s" % (ur, nameuser, userid, name, lnk))
    else:
        tosend = ("#%s\nThe user @%s has requested:\n%s\n%s" % (ur, username, name, lnk))
    return tosend


def verdict(userid, what):
    d.execute("SELECT * FROM request WHERE userid=?", (userid, ))
    ex = d.fetchone()
    name = ex[0]
    lnk = ex[1]
    nameuser = ex[4]
    if what is True:
        tosend = ("The request of the user [%s](tg://user?id=%s) has been accepted:\n[%s](%s)" % (nameuser, userid, name, lnk))
    elif what is False:
        tosend = ("The request of the user [%s](tg://user?id=%s) has been refused:\n[%s](%s)" % (nameuser, userid, name, lnk))
    else:
        tosend = ("The request of the user [%s](tg://user?id=%s) is being voted:\n[%s](%s)" % (nameuser, userid, name, lnk))
    return tosend


def checklink(lnk):
    # this checks the given link, you could not need this
    if "https://google.com/" in lnk:
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
        return 'Write /request or /$request2 to start'
    elif r <= 0:
        return 'Sorry, but at the moment the requests are closed'
    else:
        return 'Something went wrong, you found a motherfucking bug!'


def checkreq(prim, typ):
    if door > 0:
        try:
            d.execute("INSERT INTO request (userid, type) VALUES (?,?)", (prim.id, typ))
            dat.commit()
            return True
        except sqlite3.IntegrityError:
            prim.send('You have already requested something, wait until that request is solved')
            return False
    else:
        prim.send('Sorry, but at the moment request are closed')


def checkperm(i):
    d.execute("SELECT id FROM ids WHERE type=0")
    admins = d.fetchall()
    for adm in admins:
        if i in adm:
            return True
            break
    else:
        return False

@bot.command("cleanreq", hidden=True)
def cleanreq(message, chat):
    if checkperm(message.sender.id):
        chat.send('CLeaning requests...')
        d.execute("DROP TABLE IF EXISTS request")
        d.execute("VACUUM")
        d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
        chat.send('Done')
        dat.commit()    
    
    
@bot.command("cleanall", hidden=True)
def cleanall(message, chat):
    if checkperm(message.sender.id):
        chat.send('Cleaning All..')
        d.execute("DROP TABLE IF EXISTS request")
        d.execute("DROP TABLE IF EXISTS mess")
        d.execute("DROP TABLE IF EXISTS ids")
        d.execute("VACUUM")
        d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
        d.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY, type INTEGER)")
        d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER PRIMARY KEY)')
        chat.send('Done! You have deleted all the proofs')
        dat.commit()


@bot.command("door", hidden=True)
def hhh(message, chat):
    if checkperm(message.sender.id):
        try:
            door = int(message.text[5::])
            chat.send('Ok, now i\'m opened to %s requests' % (door))
        except ValueError:
            chat.send('Insert a valid number')


@bot.command("easteregg", hidden=True)
def oliodipalmas(chat, message):
    # $ Put at least one easter egg or you're dead to me
    chat.send('')


@bot.command("newadmin", hidden=True)
def newadmin(chat, message):
    # remember to set your password
    if "$password" in message.text:
        d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (message.sender.id, 0))
        chat.send("Welcome home my lord")
        dat.commit()
    else:
        chat.send("Go away dirty peasant")


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


@bot.command("setinfochannel", hidden=True)
def setinfochannel(chat, message):
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
    """Do your request"""
    if chat.type == "private":
        if checkreq(chat, 'request') is True:
            bt = botogram.Buttons()
            bt[0].callback("Cancel", "zero")
            chat.send("Send me the name of your $request", attach=bt)


@bot.command("$request2")
def second(message, chat):
    '''A different type of request'''
    # instead of request2 put the other type of your request
    if chat.type == "private":
        if checkreq(chat, '$request2') is True:
            bt = botogram.Buttons()
            bt[0].callback("Cancel", "zero")
            chat.send("Send me the name of your $request2", attach=bt)


@bot.process_message
def stager(chat, message):
    if chat.type == "private":
        d.execute("SELECT stage FROM request WHERE userid=?", (chat.id, ))
        try:
            stage = int(d.fetchone()[0])
            if stage == 1:
                bt = botogram.Buttons()
                chat.send("Name received")
                d.execute("UPDATE request SET stage=2, name=? WHERE userid=?", (message.text, chat.id))
                bt[0].callback("Back", "rename")
                bt[1].callback('There aren\'t any links', 'void')
                chat.send("Now send me the link", attach=bt)
            elif stage == 2:
                try:
                    d.execute("SELECT link FROM request WHERE userid=?", (chat.id, ))
                    if d.fetchone()[0] is None:
                        chat.send("Link received")
                        applink = str(message.parsed_text.filter("link")[0])
                        res = checklink(applink)
                    else:
                        applink = 'No link'
                        res = True
                    if res:
                        bt = botogram.Buttons()
                        d.execute("UPDATE request SET link=?, username=?, nameuser=?, userid=?, stage=3 WHERE userid=?", (applink, message.sender.username, message.sender.name, message.sender.id, chat.id))
                        bt[0].callback("Back", "relink", str(message.sender.id))
                        bt[1].callback("Cancel", "zero", str(message.sender.id))
                        bt[1].callback("Send", 'confirm', str(message.sender.id))
                        chat.send(visualizer(chat), syntax="markdown", attach=bt)
                        dat.commit()
                    else:
                        chat.send("The link is not correct!\nSend now the correct one")
                except IndexError:
                    chat.send("The link is not correct!\nSend now the correct one")
            elif stage == 3:
                chat.send('Do you wanna confirm the request?')
            elif stage == 4:
                chat.send('We are examinating your request')
            elif stage == 5:
                chat.send('At the moment your request is being voted on @$yourpublicgroup')
            elif stage == 6:
                chat.send('Your request has been approved, give us the time to publish it!')
            else:
                chat.send("GREAT, A BUG")
        except TypeError:
            chat.send(knowit(door))
        dat.commit()
        return True


@bot.callback("rename")
def rename(chat, message):
    d.execute("UPDATE request SET stage=1 WHERE userid=?", (chat.id, ))
    dat.commit()
    chat.send("Send me the name!")


@bot.callback("relink")
def relink(chat, message, data):
    d.execute("UPDATE request SET stage=2 WHERE userid=?", (chat.id, ))
    dat.commit()
    message.edit("Send me the link!")


@bot.callback('void')
def void(message, chat):
    d.execute('UPDATE request SET link=? WHERE userid=?', ('void', chat.id))
    chat.send('Ok, so there aren\'t any links, send me another message to complete your request')
    dat.commit()


@bot.callback("zero")
def zero(chat, message, data):
    d.execute("DELETE FROM request WHERE userid=?", (chat.id, ))
    dat.commit()
    message.edit("Request cancelled")


@bot.callback("zero2")
def zero2(chat, message, data):
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    dat.commit()
    bot.chat(int(data)).send("Request Published!")


@bot.callback("confirm")
def confirm(chat, message, data):
    door += -1
    bt = botogram.Buttons()
    d.execute('UPDATE request SET stage=4 WHERE userid=?', (chat.id, ))
    dat.commit()
    d.execute("SELECT id FROM ids WHERE type=1")
    staffs = d.fetchone()
    bt[0].callback("Refuse", "refuse", str(chat.id))
    bt[1].callback("Accept", "good", str(chat.id))
    bt[2].callback("VOTE", "vote", str(chat.id))
    message.edit("Your request is being examinated")
    for group in staffs:
        bot.chat(group).send(staffvis(str(chat.id)), attach=bt)


@bot.callback("refuse")
def refuse(chat, message, data):
    message.edit(verdict(int(data), False))
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    bot.chat(int(data)).send("Your request has been refused by the admins$")
    # I strongly recommend you to customize this message
    dat.commit()


@bot.callback("vote")
def groupvote(chat, message, data):
    bot.chat(int(data)).send('Your request is being voted on @$yourpublicgroup')
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
    bot.chat(int(data)).send("Your request has been approved, we will soon (but not too soon) publish it")
    d.execute('UPDATE request SET stage=6 WHERE userid=?', (int(data), ))
    dat.commit()
    d.execute("SELECT id FROM ids WHERE type=2")
    ch = d.fetchone()
    bt = botogram.Buttons()
    bt[0].callback('Published', 'zero2', data)
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
        # $ You surely have to set the votes: how many votes in favor are needed for the request to be approved
        if vote == 20:
            d.execute('DELETE FROM mess WHERE mesid=?', (message.message_id, ))
            good(chat, message, userid)
            message.edit('The citizens have talked, We want this request!')
        elif vote == -20:
            message.edit('...this request is more negative than @mamiglia...')
            zero(chat, message, userid)
            d.execute('DELETE FROM mess WHERE mesid=?', (message.message_id, ))
        else:
            d.execute('UPDATE request SET votes=? WHERE mesid=?', (vote, message.message_id))
            d.execute('INSERT INTO mess VALUES (?,?)', (message.message_id, query.sender.id))
            dat.commit()
            query.notify('Vote added!')
            qtvis(chat, message, userid)
    else:
        query.notify('Already voted!')


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
    message.edit('#%s\nIn the opinion of [%s](tg://user?id=%s) will be really interesting if this $request would be published on the channel:\n[%s](%s)\nWhat does you think?\nVotes: %s' % (ur, nameuser, userid, name, lnk, vote), preview=False, attach=bt)


if __name__ == "__main__":
    bot.run()
