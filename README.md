# Requester-Bot  
This bot lets users to makes requests to the admins of a channel, its most powerful feature is that allows admins to let the users vote about that request, in order to know what requests are more appreciated by the users, in any case this bot has really a lot of other features   

## FEATURES: 

This bot is not a common make-a-request bot, it allows admins to refuse, accept or vote a request by users.  
>Wait, What?  
* When a User makes a request the bot sends the message to the staff group and then the admins can decide:  
  * Refusing the request (maybe is a request too stupid, or whatever)  
  * Accepting a Request (maybe is really an intelligent request)  
  * _Send the request to the public group of your channel, so the request will be voted by users_  
* Complete (and quite simple) customization: all the fields that have a '$' in them have to be customized (Just translate and customize the json file)  
* Up to 2 different types of requests  
* Bugfree (AT THE MOMENT)  
* A powerful host isn't needed  
* Supports Log Channel, so everything is registred  
* Resize Number of votes requested  
* After a number N of requests the bot will automatically close itself too any further request to avoid an ocerflow of request  
* Block annoying users  
* **Manage all the requests easily**
* Pin a message in your group with some useful informations and the link to all the past requests that are being voted  
* Backup your DB in order to don't lose your datas

### These are the commands that only an admin can perform:  
-`/newadmin Your_password` : set you as a new admin  
-`/refreshpin` : refresh and pin the message in public group, if you reply to a message: the text of the messagge will be included in the pin  
-`/door N` : change the number of requests that the bot can have  
-`/resizevotes N` : resize the number of votes that a request needs to have to be accepted  
-`/setstaff` : type in the staff group to set the staff group  
-`/setgroup` : type in your group to set it  
-`/setlog @your_channel_username`: set your log channel, reboot is needed  
-`/block` : block an user, first send this command, and then forward a message of the user  
-`/unblock` : a list of the blocked users, click one to unblock  
-`/delete @username`: delete the user's request  
-`/cleanreq` : delete all the requests  
-`/cleanall` : drop every table on the DB   
-`/sqldb` : execute a command on the SQL tables (SQLite3)  
-`/backup` : backup the actual requester db (SQLite3)  


This is not only the first bot in Python I create, but it's also the first working, complex and totally new code that i write in Python, so it's my first work at all in the programming world  
Now, that you are aware of the fact that I'm a noob, I deeply apologize for all the horrible mistakes that I could do in this bot, for the bad translations, and the amount of meaningless names of definitions  

Of course I have to thank all the fantastic people that helped me: starting from @matteb99, @fef0h, @Frank1907, @pietroalbini (for his fantastic Botogram), codecademy, and last but not least @OlioDiPalmas for the emotional assistance, and encouragement   

built with Botogram (https://github.com/pietroalbini/botogram)  

## Tell me about any issue, because i'm the worst noob ever
