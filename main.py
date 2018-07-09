'''CODE UNDER APACHE 2.0 LICENSE'''
# IMPORTANT: CHANGE ALL ELEMENTS WITH '$'
# REMEMBER THAT YOU HAVE TO CHANGE ALSO THE JSON FILE
# Set your password, Set your Api token


import botogram
import sqlite3
import os
import time
from obj.start import r, d, dat, logch
from obj.jsonr import p
from obj.visualizers import visualizer, staffvis, verdict
from obj.checks import checklink, check2, knowit, checkperm
bot = botogram.create(p["values"]["token"])
# Set your api token in the json file (data/lang.json)$
bot.owner = "@Mamiglia & https://github.com/Mamiglia/Requester-Bot"
# Set yourself as the owner$

d.execute("SELECT id FROM ids WHERE type=3")
bot.chat(int(d.fetchone()[0])).send('Admins, press /refreshpin!')


def checkreq(cht, typ):
    '''Check if the user can make a request, the users can have only one request at time'''
    if int(r.get('door')) > 0:
        try:
            d.execute("INSERT INTO request (userid, type) VALUES (?,?)", (cht.id, typ))
            dat.commit()
            return True
        except sqlite3.IntegrityError:
            dat.rollback()
            d.execute("SELECT stage FROM request WHERE userid=?", (cht.id, ))
            if d.fetchone()[0] == 0:
                cht.send(p["checkreq"][2])
            else:
                cht.send(p["checkreq"][0])
    else:
        cht.send(p["checkreq"][1])
    return False


@bot.command('start')
def start(chat, message):
    '''Say Hello to the user'''
    if chat.type == 'private':
        chat.send(p["start"] % (message.sender.first_name))


@bot.command('help')
def help(chat):
    '''Instructions: How do I make a request?'''
    if chat.type == 'private':
        chat.send(p["help"])


@bot.command('rules')
def rules(chat):
    '''Specific rules, remember to set yours in lang.json'''
    if chat.type == 'private':
        chat.send(p["rules"])


@bot.command("newadmin", hidden=True)
def newadmin(chat, message):
    '''Insert a new admin in the admins list, remember to set your password in lang.json $$'''
    if p["values"]["password"] in message.text:
        d.execute("SELECT id FROM ids WHERE type=0")
        if d.fetchone() is None:
            d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (bot.itself.id, 0))
            dat.commit()
        try:
            d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (message.sender.id, 0))
            chat.send("W-welcome home S-Senpai!")
            chat.send("You already know what you what to do with me, right?\nIn any case, if you don't have any idea check it here /adminhelp")
            dat.commit()
        except sqlite3.IntegrityError:
            dat.rollback()
            chat.send("You are already an admin UwU, you can't become adminer than this")
    else:
        chat.send("Who is this CONSOLE-PEASANT??")


@bot.command('adminhelp', hidden=True)
def adminhelp(message, chat):
    '''command only for Admins, help admins to understand what actions they can do'''
    if checkperm(message.sender.id):
        chat.send("These are the commands that only an admin can perform:\n\
-/newadmin Your_password : set you as a new admin\n\
-/refreshpin : refresh and pin the message in public group, if you reply to a message: the text of the messagge will be included in the pin\n\
\n\
-/door N : change the number of requests that the bot can have\n\
-/resizevotes N : resize the number of votes that a request needs to have to be accepted\n\
\n\
-/setstaff : type in the staff group to set the staff group\n\
-/setgroup : type in your group to set it\n\
-/setlog @(your channel username): set your log channel, reboot is needed\n\
\n\
-/block : block an user, first send this command, and then forward a message of the user\n\
-/unblock : a list of the blocked users, click one to unblock\n\
-/delete @username: delete the user's request\n\
\n\
-/cleanreq : delete all the requests\n\
-/sqldb : execute a command on the SQL tables (SQLite3)\n\
-/backup : backup the actual requester db (SQLite3)")


@bot.command("delete", hidden=True)
def deletereq(message, chat):
    '''command for Admins only, delete the request of a user. Type: /delete @username'''
    if checkperm(message.sender.id):
        username = message.text[9::].lower()
        print(username)
        d.execute("SELECT name FROM request WHERE username=?", (username, ))
        b = d.fetchone()
        if b is not None:
            d.execute("DELETE FROM request WHERE username=?", (username, ))
            dat.commit()
            chat.send("Deleted >:c")
        else:
            chat.send("Invalid Username")


@bot.command("refreshpin", hidden=True)
def refreshpin(chat, message):
    if message.sender in chat.admins:
        if chat.type == 'supergroup':
            d.execute("SELECT mesid, name FROM request WHERE stage=5")
            reqs = d.fetchall()
            bt = botogram.Buttons()
            for n, x in enumerate(reqs):
                lnk = "t.me/" + chat.username + "/" + str(x[0])
                bt[n].url(x[1], lnk)
            if message.sender.id != bot.itself.id:
                try:
                    additional_text = "\n\n_%s_\n\n" % (message.reply_to_message.text)
                except AttributeError:
                    additional_text = "\n"
                tosend = (p['refreshpin'] % (additional_text))
                chat.send(tosend, attach=bt, syntax="markdown", preview=False)
                bot.api.call("pinChatMessage", {"chat_id": chat.id, "message_id": (message.id + 1)})
                r.set('pinned', message.id + 1)
            else:
                additional_text = "\n"
                tosend = p['refreshpin'] % (additional_text)
                mex = r.get('pinned')
                bot.edit_message(chat.id, mex, tosend, attach=bt, syntax="markdown", preview=False)


@bot.command("resizevotes", hidden=True)
def resizevotes(message, chat):
    '''command for Admins only, resize the number of votes that a request need to be approved'''
    if checkperm(message.sender.id):
        try:
            r.set('votes', int(message.text[12::]))
            chat.send("Votes that a request needs to be approved are now %s" % (int(r.get('votes'))))
        except ValueError:
            chat.send("Insert a valid number!")


@bot.command("cleanreq", hidden=True)
def cleanreq(message, chat):
    '''command for Admins only, clean all the requests'''
    if checkperm(message.sender.id):
        chat.send('cleaning..')
        d.execute("DROP TABLE IF EXISTS request")
        d.execute("DROP TABLE IF EXISTS mess")
        d.execute("VACUUM")
        d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
        d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER)')
        chat.send('Done!')
        dat.commit()


@bot.command("cleanall", hidden=True)
def cleanall(message, chat):
    '''command for Admins only, clean everything (also the database with the admins and groups)'''
    if checkperm(message.sender.id):
        chat.send('cleaning..')
        d.execute("DROP TABLE IF EXISTS request")
        d.execute("DROP TABLE IF EXISTS mess")
        d.execute("DROP TABLE IF EXISTS ids")
        d.execute("VACUUM")
        d.execute("CREATE TABLE IF NOT EXISTS request (name TEXT, link TEXT, userid INTEGER PRIMARY KEY, username TEXT, nameuser TEXT, stage INTEGER DEFAULT 1, type TEXT, votes INTEGER DEFAULT 0, mesid INTEGER)")
        d.execute("CREATE TABLE IF NOT EXISTS ids (id INTEGER PRIMARY KEY, username TEXT, type INTEGER)")
        d.execute('CREATE TABLE IF NOT EXISTS mess (mesid INTEGER, user INTEGER)')
        dat.commit()
        chat.send('all proofs cleared ;)')


@bot.command('sqldb', hidden=True)
def executesql(chat, message):
    if chat.type == 'private':
        if checkperm(message.sender.id):
            comm = message.text[6::]
            print("\nINFO - This command was executed by %s:" % (message.sender.name), comm, "\n")
            try:
                d.execute(comm)
                chat.send(str(d.fetchall()))
                dat.commit()
            except sqlite3.OperationalError:
                dat.rollback()
                chat.send("Can't accept this command")


@bot.command('backup', hidden=True)
def backup_db(chat):
    '''command for Admins only, send the request's db to backup it'''
    if checkperm(message.sender.id):
        chat.send_file(path="/data/dat1.db", caption=("Backup from %s" % (time.utcnow())))
        d.execute("SELECT count(*) FROM request")
        active_req = d.fetchone()
        d.execute("SELECT count(*) FROM mess")
        being_voted = d.fetchone()
        d.execute("SELECT count(*) FROM request WHERE stage=6")
        to_do_reqs = d.fetchone()
        chat.send("Active requests: %s\nBeing Voted Requests: %s\nApproved Request to do: %s" % (active_req, being_voted, to_do_reqs))


@bot.command("door", hidden=True)
def changereqnum(message, chat):
    '''command for Admins only, change the number of requests that will be accepted, set to 0 to close the requests'''
    if checkperm(message.sender.id):
        try:
            r.set('door', int(message.text[5::]))
            chat.send('Now I\'m open to %s requests' % (int(r.get('door'))))
        except ValueError:
            chat.send('Actually still open to %s requests, Insert a valid number' % (int(r.get('door'))))


@bot.command("block", hidden=True)
def blockuser(message, chat):
    '''command for Admins only, block an user'''
    if chat.type == "private" and checkperm(message.sender.id):
        bt = botogram.Buttons()
        bt[0].callback("Cancel", "delete")
        chat.send("Now forward a message from the user that you would like to block", attach=bt)
        try:
            d.execute("INSERT INTO request (userid, stage) VALUES (?, 99)", (message.sender.id, ))
            dat.commit()
        except sqlite3.IntegrityError:
            dat.rollback()
            d.execute("UPDATE request SET stage=99 WHERE userid=?", (message.sender.id, ))
            dat.commit()


@bot.command("unblock", hidden=True)
def unblock(message, chat):
    '''command for Admins only, unblock an user'''
    if chat.type == "private" and checkperm(message.sender.id):
        bt = botogram.Buttons()
        d.execute("SELECT userid, name FROM request WHERE stage=0")
        blocklist = d.fetchall()
        if blocklist == []:
            chat.send("There aren't blocked users")
        else:
            for index, user in enumerate(blocklist):
                bt[index].callback(str(user[1]), "unban", str(user[0]))
            chat.send("Who do you want to unblock?", attach=bt)


@bot.command("oliodipalmas", hidden=True)
def easteregg(chat, message):
    # $ Put at least one easter egg or you're dead to me
    chat.send(p["easteregg"])


@bot.command("info")
def info(chat):
    chat.send("You can find the source code of this bot on https://github.com/Mamiglia/Requester-Bot, bot created by @Mamiglia using botogram")


@bot.command("setstaff", hidden=True)
def setstaff(chat, message):
    '''command for Admins only, set the staff group'''
    if chat.type == "supergroup":
        if checkperm(message.sender.id):
            try:
                d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (chat.id, 1))
                chat.send("Staff Group correctly set!")
                dat.commit()
            except sqlite3.IntegrityError:
                dat.rollback()
                chat.send("This Chat is already been used for something else")
        else:
            chat.send("I need to receive the command from an important guy, not a console peasant as you")
    else:
        chat.send("I should be in a Supergroup, wrong chat!")


@bot.command("setgroup", hidden=True)
def setgroup(chat, message):
    '''command for Admins only, set the group where are the users, and the group where the requests will be voted'''
    if chat.type == "supergroup":
        if checkperm(message.sender.id):
            try:
                d.execute("INSERT INTO ids (id, type) VALUES (?,?)", (chat.id, 3))
                chat.send("Group correctly set!")
                dat.commit()
            except sqlite3.IntegrityError:
                dat.rollback()
                chat.send("This Chat is already been used for something else")
        else:
            chat.send("I need to receive the command from an important guy, not a console peasant as you")
    else:
        chat.send("I should be in a Supergroup, wrong chat!")


@bot.command("setlog", hidden=True)
def setlogchannel(chat, message):
    '''command for Admins only, set the log channel'''
    if chat.type == "private":
        if checkperm(message.sender.id):
            chn = message.text[8::]
            try:
                global logch
                logch = botogram.channel(chn, p["values"]["token"])
                d.execute("INSERT INTO ids (username, type) VALUES (?,?)", (chn, 2))
                chat.send("Log Channel correctly set! Reboot me")
                dat.commit()
            except botogram.api.ChatUnavailableError:
                dat.rollback()
                chat.send('Username invalid')
        else:
            chat.send("I need to receive the command from an important guy, not a console peasant as you")
    else:
        chat.send("I should be in a private chat, wrong chat!")


@bot.command("request")
def first(message, chat):
    """Make Your Request!"""
    if chat.type == "private":
        if checkreq(chat, 'request'):
            bt = botogram.Buttons()
            bt[0].callback(p["request"][0], "zero", str(chat.id))
            chat.send(p["request"][1], attach=bt)


@bot.command(p["values"]["request2"], hidden=False)
def second(message, chat):
    '''Request something different'''
    # You can have different types of request, or just set hidden=True if you don't want to use this feature
    if chat.type == "private":
        if checkreq(chat, p["values"]["request2"]) is True:
            bt = botogram.Buttons()
            bt[0].callback(p["request"][0], "zero", str(chat.id))
            chat.send(p["request"][2], attach=bt)


@bot.command("cancel")
def deletemine(message, chat):
    '''self-delete the request of the user'''
    if chat.type == "private":
        d.execute("SELECT stage FROM request WHERE userid=?", (message.sender.id, ))
        try:
            stage = d.fetchone()[0]
        except TypeError:
            chat.send(p["deletemine"][0])
            return
        if stage == 0:
            return
        elif stage < 5:
            d.execute("DELETE FROM request WHERE userid=?", (message.sender.id, ))
            dat.commit()
        elif stage == 5:
            d.execute("SELECT id FROM ids WHERE type=3")
            group = d.fetchone()[0]
            d.execute("SELECT mesid FROM request WHERE userid=?", (message.sender.id, ))
            mesid = d.fetchone()[0]
            try:
                bot.edit_message(group, mesid, "Request canceled by user")
            except (TypeError, botogram.api.APIError):
                print("WARNING - You shall not delete the voting messages of an user")
            d.execute("DELETE FROM request WHERE userid=?", (message.sender.id, ))
            d.execute("DELETE FROM mess WHERE user=?", (message.sender.id, ))
            dat.commit()
        elif stage > 5:
            chat.send(p["deletemine"][1])
            return
        chat.send(p["deletemine"][2])
        refreshpin(chat, message)


@bot.process_message
def stager(chat, message):
    '''The core of this code, it just checks at what moment the request is, and ask the specific information to the user'''
    if chat.type == "private":
        d.execute("SELECT stage FROM request WHERE userid=?", (chat.id, ))
        try:
            stage = int(d.fetchone()[0])
            if stage == 1:
                bot.edit_message(chat, int(message.id - 1), p["request"][1])
                bt = botogram.Buttons()
                d.execute("UPDATE request SET stage=2, name=?, username=?, nameuser=? WHERE userid=?", (message.text, (message.sender.username).lower(), message.sender.name, chat.id,))
                dat.commit()
                bt[0].callback(p["stager"]["1"][1], "rename")
                bt[1].callback(p["stager"]["1"][2], 'void')
                chat.send(p["stager"]["1"][3], attach=bt)
            elif stage == 2:
                try:
                    d.execute("SELECT link FROM request WHERE userid=?", (chat.id, ))
                    # selection due to the fact that i use the same stager() function also in the 'No Link' event
                    lnk = d.fetchone()[0]
                    if lnk is None:
                        lnk = str(message.parsed_text.filter("link")[0])
                        res = checklink(lnk)
                        bot.edit_message(chat, int(message.id - 1), p["stager"]["1"][3])
                    else:
                        lnk = 'No link'
                        res = True
                        message.edit(p["stager"]["1"][3])
                        chat.send(p["stager"]["2"][5])
                    if res:
                        bt = botogram.Buttons()
                        d.execute("UPDATE request SET link=?, stage=3 WHERE userid=?", (lnk, chat.id))
                        dat.commit()
                        bt[0].callback(p["stager"]["2"][1], "relink", str(chat.id))
                        bt[1].callback(p["stager"]["2"][2], "zero", str(chat.id))
                        bt[1].callback(p["stager"]["2"][3], 'confirm', str(chat.id))
                        chat.send(visualizer(chat), syntax="markdown", attach=bt)
                    else:
                        chat.send(p["stager"]["2"][4])
                except IndexError:
                    dat.rollback()
                    chat.send(p["stager"]["2"][4])
            elif stage == 3:
                chat.send(p["stager"]["3"][0])
            elif stage == 4:
                chat.send(p["stager"]["4"][0])
            elif stage == 5:
                chat.send(p["stager"]["5"][0])
            elif stage == 6:
                chat.send(p["stager"]["6"][0])
            elif stage == 0:
                chat.send(p["stager"]["0"][0])
            elif stage == 99:
                blocking = message.forward_from
                print(blocking.name)
                try:
                    d.execute("INSERT INTO request (userid, name, stage) VALUES (?,?,0)", (blocking.id, blocking.name))
                except sqlite3.IntegrityError:
                    dat.rollback()
                    d.execute("UPDATE request SET stage=0 WHERE userid=?", (blocking.id, ))
                d.execute("DELETE FROM request WHERE userid=?", (message.sender.id, ))
                dat.commit()
                chat.send("BLOCKED, type /unblock to unblock ")
            else:
                chat.send(p["stager"]["err"][0])
        except TypeError:
            chat.send(knowit(int(r.get('door'))))
        dat.commit()
        return True


@bot.callback("delete")
def dele(query):
    query.message.delete()


@bot.callback("rename")
def rename(chat, message):
    '''rename the the request'''
    d.execute("UPDATE request SET stage=1 WHERE userid=?", (chat.id, ))
    dat.commit()
    message.edit(p['rename'])


@bot.callback("relink")
def relink(chat, message, data):
    '''change the provided link'''
    d.execute("UPDATE request SET stage=2, link=NULL WHERE userid=?", (chat.id, ))
    dat.commit()
    bt = botogram.Buttons()
    bt[0].callback(p['stager']['1'][2], 'void')
    message.edit(p["relink"], attach=bt)


@bot.callback('void')
def void(message, chat):
    '''set null link'''
    d.execute('UPDATE request SET link=? WHERE userid=?', ('NULL', chat.id))
    dat.commit()
    stager(chat, message)


@bot.callback("zero")
def zero(chat, message, data):
    '''delete the request'''
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    dat.commit()
    message.edit(p["zero"])


@bot.callback("zero2")
def zero2(chat, message, data):
    '''delete the request after that it is solved'''
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    dat.commit()
    message.delete()
    bot.chat(int(data)).send(p["zero2"])


@bot.callback("confirm")
def confirm(chat, message, data):
    '''confirm the request, and send it to the staff group'''
    door = int(r.get('door')) - 1
    r.set('door', door)
    bt = botogram.Buttons()
    d.execute('UPDATE request SET stage=4 WHERE userid=?', (chat.id, ))
    dat.commit()
    d.execute("SELECT id FROM ids WHERE type=1")
    staffs = d.fetchone()
    bt[0].callback(p["confirm"][0], "refuse", str(chat.id))
    bt[1].callback(p["confirm"][1], "good", str(chat.id))
    bt[2].callback(p["confirm"][2], "vote", str(chat.id))
    for group in staffs:
        bot.chat(group).send(staffvis(str(chat.id)), attach=bt)
    message.edit(p["confirm"][3])


@bot.callback("refuse")
def refuse(chat, message, query, data):
    '''refuse the request'''
    d.execute("SELECT stage FROM request WHERE userid=?", (int(data), ))
    try:
        if d.fetchone()[0] == 4:
            bot.chat(int(data)).send(p["refuse"])
            message.edit(verdict(int(data), False, query.sender.name, query.sender.id))
            d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
            dat.commit()
        else:
            message.edit("Already in another Stage baby")
    except TypeError:
        dat.rollback()
        message.edit(p["alreadydel"])


@bot.callback("vote")
def groupvote(chat, message, data, query):
    '''the request will be voted in the group'''
    d.execute("SELECT stage FROM request WHERE userid=?", (int(data), ))
    x = d.fetchone()
    try:
        if x[0] == 4:
            bot.chat(int(data)).send(p["vote"])
        else:
            message.edit("Already in another Stage baby")
    except TypeError as ex:
        dat.rollback()
        message.edit(p["alreadydel"])
    else:
        d.execute('UPDATE request SET stage=5 WHERE userid=?', (int(data), ))
        dat.commit()
        message.edit(verdict(int(data), 'vote', query.sender.name, query.sender.id))
        d.execute("SELECT id FROM ids WHERE type=3")
        groups = d.fetchone()
        bt = botogram.Buttons()
        bt[0].callback('start', 'startpoll', data)
        for group in groups:
            bot.chat(group).send("New Poll by %s" % (data), attach=bt)


@bot.callback("good")
def good(chat, message, data, query):
    '''Accept the request without voting procedure'''
    d.execute("SELECT stage FROM request WHERE userid=?", (int(data), ))
    try:
        stage = d.fetchone()[0]
        if stage <= 5:
            bot.chat(int(data)).send(p["good"][0])
            d.execute('UPDATE request SET stage=6 WHERE userid=?', (int(data), ))
            dat.commit()
            bt = botogram.Buttons()
            bt[0].callback(p["good"][1], 'zero2', str(data))
            logch.send(staffvis(data), attach=bt)
            if stage == 4:
                message.edit(verdict(int(data), True, query.sender.name, query.sender.id))
        else:
            message.edit("Already in another Stage baby")
    except TypeError:
        dat.rollback()
        message.edit(p["alreadydel"])


@bot.callback('op')
def operation(chat, message, query, data):
    d.execute('SELECT user FROM mess WHERE mesid=?', (message.id, ))
    users = d.fetchall()
    if users == [] or check2(users, query.sender.id):
        d.execute('SELECT votes, userid, name, link FROM request WHERE mesid=?', (message.id, ))
        ex = d.fetchone()
        vote = ex[0] + int(data)
        userid = ex[1]
        # set how many votes are needed in default for the request to be approved up in line 52
        if vote >= int(r.get('votes')):
            good(chat, message, userid, None)
            message.edit(p["op"][0])
            d.execute('DELETE FROM mess WHERE mesid=?', (message.id, ))
            dat.commit()
            refreshpin(chat, message)
        elif vote <= -int(r.get('votes')):
            zero(chat, message, userid)
            message.edit(p["op"][1])
            d.execute('DELETE FROM mess WHERE mesid=?', (message.id, ))
            dat.commit()
            refreshpin(chat, message)
        else:
            d.execute('UPDATE request SET votes=? WHERE mesid=?', (vote, message.id))
            d.execute('INSERT INTO mess (mesid, user) VALUES (?,?)', (message.id, query.sender.id))
            dat.commit()
            query.notify(p["op"][2])
            qtvis(chat, message, userid)
    else:
        query.notify(p["op"][3])


@bot.callback('startpoll')
def startpoll(chat, message, data):
    '''start the poll in the group'''
    d.execute('UPDATE request SET mesid=? WHERE userid=?', (message.id, int(data)))
    dat.commit()
    refreshpin(chat, message)
    qtvis(chat, message, data)


@bot.callback('qtvis')
def qtvis(chat, message, data):
    '''a cute indentation for the message with the votes in the user's group'''
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


@bot.callback("unban")
def unban(chat, message, data):
    d.execute("DELETE FROM request WHERE userid=?", (int(data), ))
    dat.commit()
    message.edit("Unbanned!")


works = os.cpu_count()
bot.run(workers=works)
dat.commit()

if __name__ == "__main__":
    bot.run()
