Different types of ids (stored in the ids table)
-
type0 = global admins bot  
type1 = staff group  
type2 = log channel   
type3 = public group  
type4 = channel  

Set a new admin by typing "/newadmin YOURPASSWORD" (set a password in the langEN.json file at line 84)
-

The bots divide the request action in different stages:
stage0 = ready to do a request (never used)
stage1 = just typed /request, the user has to give the name of the request
stage2 = gave the name of the request, the user has to give the link of the request
stage3 = he have to confirm all 
stage4 = examinating in staff
stage5 = voting in public group
stage6 = approved 
stage7 = soddisfacted and to delete (never used)

REMEMBER TO MODIFY ALL '$' ELEMENTS also in langEN.json
- 
