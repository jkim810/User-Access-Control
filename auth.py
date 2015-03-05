#author: Junbum Kim
from getpass import getpass

#Account List
accounts = []
#Login attempt counter
login_count = 0
#Login success
login_success = False
#username to keep track
username = ""
#---------------------------------------------------------------------#
# Account Object - SETUP FOR ACCOUNT
class account:
	def __init__(self, user, pwd):
		self.username = user
		self.password = pwd
	def get_username(self):
		return self.username
	def get_password(self):
		return self.password

# Open user login database
login_db = open("users.txt", "rw+")
login_db_string = login_db.read()
login_db.close()

# STORE ACCOUNTS
# Tokenize newline character
accounts_list = login_db_string.split()
# Tokenize with delimiter : and store into a list of account object
for x in accounts_list:
	user_pass_list = x.split(":")
	account_to_add = account(user_pass_list[0], user_pass_list[1])
	accounts.append(account_to_add)

# LOG IN CHECK
def login_correct(username, password):
	result = False
	for x in accounts:
		if username == x.get_username() and password == x.get_password():
			result = True
			break
	return result

#---------------------------------------------------------------------#
#ATTEMP LOGIN - LOGIN PROCEDURE
print "---------------------"
while login_count < 3 and not login_success:
	#prompt user for username and password (echo off)
	username = raw_input("User name: ")
	password = getpass()

	#prompt username again if longer than 8 characters
	if len(username) > 8:
		print "***User name cannot be longer than 8 alphanumerica characters***"

	#username or password does not match
	elif login_correct(username, password) == False:
		print "***Incorrect username or password.***"
	#username and password matches
	else:
		login_success = True
		print "Login Success!"
		print "---------------------"
		break

	#LOGIN FAIL
	#increment login count and indicate left login attemps
	login_count = login_count + 1
	print "---------------------"
	print str(3 - login_count) + " login attemp(s) left."

	#if no login attempts left and login is unsuccessful, exit program
	if login_count == 3 and login_success == False:
		print "LOGIN FAIL. EXIT PROGRAM"
		print "---------------------"
		exit(0)

#---------------------------------------------------------------------#
#LOGGED IN - SETUP FOR AUTH
#Authentication Object
class auth:
	def __init__(self, action, user, file_name):
		self.action = action
		self.user = user
		self.file = file_name
	def get_action(self):
		return self.action
	def get_user(self):
		return self.user
	def get_file(self):
		return self.file

#authentication list
auth_list = []
# Open user login database
auth_db = open("auth.txt", "rw+")
auth_db_string = auth_db.read()
auth_db.close()

# STORE ACTIONS
# Tokenize newline character
action_list = auth_db_string.split()
# Tokenize with delimiter : and store into a list of auth object
for x in action_list:
	actions_list = x.split(":")
	auth_to_add = auth(actions_list[0], actions_list[1], actions_list[2])
	auth_list.append(auth_to_add)

#list of files
files = []
for x in auth_list:
	if x.get_file() not in files:
		files.append(x.get_file())
files.remove("")
files = sorted(files)

#list of files with denied files
global_permit = []
permitted_files = []
permit_all = []
global_deny = []
denied_files = []
deny_all = []
#----------------------------------------------------------------------#
#AUTHENTICATION
print "Authentication Information:"
for x in auth_list:
	if x.get_action() == "PERMIT":
		if x.get_user() == '':
			if x.get_file() == '':
				print "Format Error"
			else:
				global_permit.append(x.get_file())
				files.remove(x.get_file())
		elif x.get_user() == username:
			if x.get_file() == "":
				permit_all = files
			else:
				permitted_files.append(x.get_file())
	if x.get_action() == "DENY":
		if x.get_user() == '':
			if x.get_file() == '':
				print "Format Error"
			else:
				global_deny.append(x.get_file())
				files.remove(x.get_file())
		elif x.get_user() == username:
			if x.get_file() == "":
				deny_all = files
			else:
				denied_files.append(x.get_file())

#Get Rid of files that are both permitted and denied from the permitted files
for x in denied_files:
	for y in permit_all:
		if x==y:
			permit_all.remove(y)
	for y in global_permit:
		if x==y:
			global_permit.remove(y)
for x in permitted_files:
	for y in deny_all:
		if x == y:
			deny_all.remove(y)
	for y in global_deny:
		if x==y:
			global_deny.remove(y)

#Add files
permitted_files = global_permit + permitted_files + permit_all
denied_files = global_deny + denied_files + deny_all

#sort files and get rid of duplicates
permitted_files = list(set(permitted_files)) 
denied_files = list(set(denied_files))
permitted_files = sorted(permitted_files)
denied_files = sorted(denied_files)

#echo permitted files
for x in permitted_files:
	fo = open(x,"r")
	print fo.read()
	fo.close()

#print denied files
for x in denied_files:
	print "Access to file <" + x + "> denied."
