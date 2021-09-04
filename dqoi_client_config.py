# forces the client to connect to the live server instead of localhost
force_live = False

##########################################################

local_file = 'local.txt'
user_file = 'user.txt'

import os.path

# WebSocket Port
def get_host_port():
	return 1337

# WebSocket URL
def get_host_url():
	if os.path.isfile(local_file) and not force_live:
		return 'http://localhost:'+str(get_host_port())
	else:
		return 'http://dontquitownit.com:'+str(get_host_port())

def get_user_credentials():
	username = ''
	password = ''
	if os.path.isfile(user_file):
		f = open(user_file, "r")
		lines = f.read().splitlines()
		username = lines[0]
		password = lines[1]
	else:
		username = 'test'
		password = 'test'
	#print('username:'+username)
	#print('password:'+password)
	return (username,password)