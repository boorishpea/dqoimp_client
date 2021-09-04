
from tkinter import *
from tkinter import messagebox
root=Tk()
root.withdraw()
import sys
from PIL import ImageTk,Image

class mainWindow(object):
	def __init__(self,master,filename):
		self.input=""
		self.master=master
		master.eval('tk::PlaceWindow . center')
		path = filename
		self.img = ImageTk.PhotoImage(Image.open(path))
		#print("self.img",self.img)
		self.panel = Label(master, image = self.img)
		self.panel.pack(side = "top", fill = "both", expand = "yes")
		self.e=Entry(master)
		self.e.pack()
		self.b=Button(master,text="Complete Captcha",command=self.click)
		self.b.pack()
	def click(self):
		self.input = self.e.get()
		#self.img.pack_forget()
		self.panel.pack_forget()
		self.e.pack_forget()
		self.b.pack_forget()
		self.master.quit()

#!/usr/bin/env python

version = "0.9.0"
auto_login = False

import traceback

###########################################################################################################################################################


def call_counter(func):
	def helper(*args, **kwargs):
		helper.calls += 1
		return func(*args, **kwargs)
	helper.calls = 0
	helper.__name__= func.__name__

	return helper

def memoize(func):
	mem = {}
	def memoizer(*args, **kwargs):
		key = str(args) + str(kwargs)
		if key not in mem:
			mem[key] = func(*args, **kwargs)
		return mem[key]
	return memoizer

@call_counter
@memoize    
def levenshtein(s, t):
	if s == "":
		return len(t)
	if t == "":
		return len(s)
	if s[-1] == t[-1]:
		cost = 0
	else:
		cost = 1
	
	res = min([levenshtein(s[:-1], t)+1,
			   levenshtein(s, t[:-1])+1, 
			   levenshtein(s[:-1], t[:-1]) + cost])

	return res

def levenshtein_percent(string_a,string_b):
	string_len = len(string_a)
	if len(string_b) > string_len:
		string_len = len(string_b)
	result = levenshtein(string_a, string_b)
	percent = float(string_len - result)/float(string_len)
	return percent

# import os
# if __name__ == "__main__":
	# string_a = "Python"
	# string_b = "Peithen"
	# print("percent: %s" % (float(levenshtein_percent(string_a,string_b))))
	# os._exit(0)
###########################################################################################################################################################

import operator
import collections

mail_per_page = 10

import colorama
from colorama import Fore, Back, Style
colorama.init(convert=True)

class Tutorial():
	def __init__(self):
		self.steps = [
			"Welcome to the Don't Quit, Own It! (DQOI) Tutorial. This tutorial will introduce you to DQOI and teach you the basic commands."
		]
		print(Fore.GREEN+Style.BRIGHT+"Tutorial Step 1/1 : "+self.steps[0])
		print("Which command set would you like to learn about?")
		print("Viewing Commands & Command Help")
		print("Gateways & File System")
		print("[press ENTER to continue]"+Style.RESET)

import os
import sys
import dqoi_client
import dqoi_client_config


# import only system from os 
from os import system, name 

# define our clear function 
def clear(): 
	# for windows 
	if name == 'nt': 
		_ = system('cls') 
	
	# for mac and linux(here, os.name is 'posix') 
	else: 
		_ = system('clear') 

config_colors_disabled = False

str_command_nslookup = "nslookup"
str_command_dir = "dir"

import argparse

from magic_base import IPv3Address
ipv3 = IPv3Address()
		

import client_class

client = client_class.Client()
client.allow_terminate = False
session = client_class.Dictionary()

def dp(f, d):
	return float(("%."+str(d)+"f") % float(f))

import math
def bytesToSize(bytes):
	bytes = int(bytes)
	base = 1024
	decimal_places = 2
	sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB',       'PB']
	if bytes == 0:
		return '0 Byte'
	log_a = math.log(float(bytes))
	log_b = math.log(float(base))
	floor = math.floor(log_a/log_b)
	i = int(floor)
	
	print(str(bytes / pow(base, i)))
	return str(dp(float(bytes / pow(base, i)), decimal_places)) + ' ' + sizes[i]

def intWithCommas(x):
	if type(x) not in [int]:
		raise TypeError("Parameter must be an integer.")
	if x < 0:
		return '-' + intWithCommas(-x)
	result = ''
	while x >= 1000:
		x, r = divmod(x, 1000)
		result = ",%03d%s" % (r, result)
	return "%d%s" % (x, result)

import signal
def signal_handler(signal, frame):
	global client
	client.disconnect()

	
def main_menu():
	
	print("[1] Login")
	print("[2] Register")
	print("[3] Recover")
	print("[4] Quit")

	userinput = ""
	if auto_login == False:
		userinput = client.get_input('>')
	else:
		userinput = '1'
	
	if userinput == '1':
		username = ""
		password = ""
		if auto_login == False:
			username = client.get_input('username>')
			password = client.get_input('password>')
		else:
			user_credentials = dqoi_client_config.get_user_credentials()
			username = user_credentials[0]
			password = user_credentials[1]
		#print("logging in as '"+username+"'...")
		global session
		session.clear()
		session.add('local_working_directory','/')
		session.add('remote_working_directory','/')
		session.add('username',username)
		result = client.user_login(username,password)
		
		if result['error'] == True:
			print('error: '+result['error_message'])
			main_menu()
		else:
			#print('successfully logged in.')
			#if result['is_admin']:
			#	print('you are using an administrator account')
			print("")
			#print(result)
			#global session
			session.add('is_admin',result['is_admin'])
			session.add('selected_gateway_id',result['selected_gateway_id'])
			session.add('selected_gateway_hostname',result['selected_gateway_hostname'])
			session.add('selected_gateway_dns_ip_address',result['selected_gateway_dns_ip_address'])
			session.add('selected_gateway_ip_address',result['selected_gateway_ip_address'])
			session.add('connected',False)
			session.add('local_or_remote','local')
			
			
			#latest_client_version = ""
			#if result['latest_client_version'] != None:
			#	latest_client_version = result['latest_client_version']
			#latest_client_version_parts = latest_client_version.split('.')
			#current_client_version_parts = version[1:len(version)].split('.')
			
			#if int(latest_client_version[0]) >= int(current_client_version_parts[0]) or int(latest_client_version[1]) >= int(current_client_version_parts[1])
			
			#print(result)
			
			#session.set('connection_route', result['connection_route'])
			#session.set('local_or_remote','remote')
			#session.set('connected_hostname',result['remote_host']['host_name'])
			#session.set('connected_ip_address',result['remote_host']['ip_address'])
			#session.set('remote_host_motd', result['remote_host']['motd'])
			#session.set('remote_host_is_dns_server', result['remote_host']['is_dns_server'])
			#session.set('has_bulletin_board', result['remote_host']['has_bulletin_board'])
			
			
			#if result['new_mail'] > 0:
			#	print("you have "+str(result['new_mail'])+" unread mail messages")
			print("run the 'help' command to see a list of commands or the 'tutorial' for a step by step guide")
			print("")
			console()
		
	elif userinput == '2':
		
		proceed = True
		username = ""
		while proceed:
			username = client.get_input('username>')
			min_length = 4
			max_length = 16
			#print(len(username))
			if len(username) < min_length or len(username) > max_length:
				print("username must be between 4 and 16 characters long")
			else:
				proceed = False
		
		proceed = True
		password = ""
		while proceed:
			password = client.get_input('password>')
			min_length = 4
			max_length = 100
			if len(password) < min_length or len(password) > max_length:
				print("password must be between 4 and 100 characters long")
			else:
				proceed = False
		
		proceed = True
		secretquestion = ""
		while proceed:
			secretquestion = client.get_input('secretquestion>')
			min_length = 4
			max_length = 32
			if len(secretquestion) < min_length or len(secretquestion) > max_length:
				print("secretquestion must be between 4 and 32 characters long")
			else:
				proceed = False
		
		proceed = True
		secretanswer = ""
		while proceed:
			secretanswer = client.get_input('secretanswer>')
			min_length = 4
			max_length = 32
			if len(secretanswer) < min_length or len(secretanswer) > max_length:
				print("secret_answer must be between 4 and 32 characters long")
			else:
				proceed = False
		
		proceed = True
		if proceed:
			retry = True
			retry_attempt = 0
			retry_max = 3
			while retry:
				
				retry_attempt+=1
				if retry_attempt > retry_max:
					print("3 failed captcha retries")
					retry = False
					continue
				
				result = client.get_captcha()
				if result['error'] == False:
					
					
					try:
						os.mkdir("captchas")
					except:
						pass
					
					key = result['captcha_key']
					image = result['captcha_image']
					
					path = "captchas/"+key+".png"
					data = image
					try:	
						mode="w"
						if type(data)==bytes:
							mode="b"+mode
							encoding=None
						with open(path, mode) as text_file:
							text_file.write(data)
					except:
						traceback.print_exc()
					
					
					m=mainWindow(root, path)
					root.mainloop()

					# root = Tk()
					# root.withdraw()
					# messagebox.showinfo("caption", str(m.input))

					result = client.user_register(username,password,secretanswer,secretquestion,key,m.input)
					if result['error'] == True:
						if result['error_message'] == 'invalid captcha':
							print(result['error_message'])
							#root = Tk()
							root.withdraw()
							messagebox.showinfo("error", result['error_message'])
							retry = True
						else:
							print(result['error_message'])
							#root = Tk()
							root.withdraw()
							messagebox.showinfo("error", result['error_message'])
							retry = False
					else:
						retry = False
						print("Success User Registered!")
						#root = Tk()
						root.withdraw()
						messagebox.showinfo("error", "Success User Registered!")
					
					#print(result)
					
		main_menu()
	elif userinput == '3':
		username = client.get_input('username>')
		result = client.secret_question_get(username)
		if result['error']:
			print(result['error'])
		else:
			print("secretquestion>"+result['secret_question'])
			secretanswer = client.get_input("secretanswer>")
			result = client.secret_answer_validate(username, secretanswer)
			if result['error']:
				print(result['error'])
			else:
				newpassword = client.get_input("newpassword>")
				result = client.recover(username, secretanswer, newpassword)
				if result['error']:
					print(result['error'])
				else:
					print("password successfully changed, you may now login")
		main_menu()
	elif userinput == '4':
		pass
	else:
		print("invalid option")
		main_menu()

def print_server_database_list(result):
	if result['error'] == True:
		print('error: '+result['error_message'])
	else:
		print("")
		client.print_table('id,gateway_name,gateway_domain,gateway_ip,is_owner,is_admin',result['result'])
		print("")
		#print('id,gateway_name,gateway_domain,gateway_ip,is_owner,is_admin')
		#for gateway in result['result']:
		#		print('%s,%s,%s,%s,%s,%s' % (gateway[0],gateway[1],gateway[2],gateway[3],gateway[4],gateway[5],))
	

def gateway_disconnect():
	result = client.gateway_disconnect()
	if result['error']:
		print(result['error_message'])
	else:
		print("disconnected.")
		session.set("connected",False)
		session.set("local_or_remote",'local')

def parse_connection_route(connection_route):

	local_or_remote = session.get('local_or_remote')
	
	output = ""
	for i in range(0,len(connection_route)):
		if i != 0:
			output += " > "
		if i == len(connection_route)-1 and local_or_remote == 'remote':
			output += "["+connection_route[i]+"]"
		elif i == 0 and local_or_remote == 'local':
			output += "["+connection_route[i]+"]"
		else:
			output += connection_route[i]
	return output

def log_view(page):
	result = client.log_view(10,page,session.get('local_or_remote')=='remote')
	if result['error'] == False:
		if len(result['result']) == 0:
			print("no logs to display")
		else:
			for i in range(0,len(result['result'])):
				if result['result'][i][1] == "":
					result['result'][i][1] = "<empty>"
				result['result'][i][2] = client.timestamp_to_str(result['result'][i][2])
			client.print_table('id,message,date_time', result['result'])
			print("")
			log_start = 10*(page-1)
			log_end = log_start +10
			print("Logs {}-{}".format(log_start,log_end))
			next = False
			previous = False
			if len(result['result']) == 10:
				next = True
			if page > 1:
				previous = True
			options_str = ""
			if next:
				options_str += "[N]ext "
			if previous:
				options_str += "[P]revious "
			if next or previous:
				options_str += "[C]ancel "
				print(options_str)
				option = client.get_input("option>").strip().upper()
				if option == 'N':
					log_view(page+1)
				if option == 'P':
					log_view(page-1)

clean_exit = False
logout = False

def console(userinput = ""):
	
	new_mail = False
	if client.new_mail == True:
		new_mail = True
		client.new_mail = False
	
	global logout
	# logout = False
	skip = False
	
	if session.get('connected') == True:
		print(parse_connection_route(session.get('connection_route')))
	
	local_or_remote = session.get('local_or_remote')
	if local_or_remote == 'local':
		if config_colors_disabled:
			cmd_text = session.get("username")+"@"+session.get('selected_gateway_hostname')+"["+session.get('selected_gateway_ip_address')+"]"+session.get('local_working_directory')+">"
		else:
			cmd_text = Fore.GREEN+session.get("username")+Fore.GREEN+"@"+Fore.GREEN+session.get('selected_gateway_hostname')+Fore.GREEN+"["+Fore.GREEN+session.get('selected_gateway_ip_address')+Fore.GREEN+"]"+Fore.CYAN+session.get('local_working_directory')+Fore.WHITE+">"
	else:
		if session.get("remote_admin") == True:
			if config_colors_disabled == False:
				cmd_text = Fore.RED+"root"+Fore.RED+"@"+Fore.RED+session.get('connected_hostname')+Fore.RED+"["+Fore.RED+session.get('connected_ip_address')+"]"+Fore.CYAN+session.get('remote_working_directory')+Fore.WHITE+">"
			else:
				cmd_text = "root"+"@"+session.get('connected_hostname')+"["+session.get('connected_ip_address')+"]"+session.get('local_working_directory')+">"
		else:
			if config_colors_disabled == False:
				cmd_text = Fore.YELLOW+"guest"+Fore.YELLOW+"@"+Fore.YELLOW+session.get('connected_hostname')+Fore.YELLOW+"["+Fore.YELLOW+session.get('connected_ip_address')+Fore.YELLOW+"]"+Fore.WHITE+">"
			else:
				cmd_text = "guest"+"@"+session.get('connected_hostname')+"["+session.get('connected_ip_address')+"]>"
	
	if new_mail:
		#print("")
		print("You have a new mail message!")
		print("")
	
	if userinput == "" and logout == False:
		userinput = client.get_input(cmd_text)
		userinput = userinput.strip()

	options_list = []
	if session.get("is_admin") == True:
		options_list.append("sqlquery")
		options_list.append("connlist")
		options_list.append("stats")
	options_list.append("time")
	options_list.append("help")
	options_list.append("mail")
	options_list.append("userranks")
	options_list.append("ranks")
	options_list.append("logview")
	options_list.append("logs")
	options_list.append("logdelete")
	options_list.append("logmodify")
	options_list.append("hostname")
	options_list.append("motd")
	options_list.append("setmotd")
	options_list.append("netconfig")
	options_list.append("bankloan")
	options_list.append("loan")
	options_list.append(str_command_nslookup)
	options_list.append("ping")
	#options_list.append("pingscan")
	options_list.append("serverping")
	options_list.append(str_command_dir)
	options_list.append("ls")
	options_list.append("destroy") # todo destroy installed software
	options_list.append("mkdir")
	options_list.append("rm")
	options_list.append("delete")
	options_list.append("cd")
	options_list.append("connect")
	options_list.append("remote")
	options_list.append("serverdb")
	options_list.append("serverdbdelete")
	options_list.append("bankbalance")
	options_list.append("balance")
	options_list.append("bank")
	options_list.append("banktransactions")
	options_list.append("transactions")
	options_list.append("transfers")
	options_list.append("banktransfer")
	options_list.append("transfer")
	options_list.append("userlist")
	options_list.append("users")
	options_list.append("changepassword")
	options_list.append("changeip")
	options_list.append("accountsettings")
	options_list.append("gatewaylist")
	options_list.append("gateways")
	options_list.append("gatewayselect")
	options_list.append("gatewaybuy")
	options_list.append("gatewayupgrade")
	options_list.append("upgrade")
	options_list.append("processlist")
	options_list.append("ps")
	options_list.append("processstart")
	options_list.append("run")
	options_list.append("processcomplete")
	options_list.append("complete")
	options_list.append("processkill")
	options_list.append("pkill")
	options_list.append("kill")
	options_list.append("quit")
	options_list.append("exit")
	options_list.append("missioncomplete")
	options_list.append("fileperms")
	options_list.append("filetransfers")
	options_list.append("transferbw")
	options_list.append("install")
	options_list.append("software")
	options_list.append("collectall")
	options_list.append("collect")
	options_list.append("copy")
	options_list.append("cp")
	options_list.append("cls")
	options_list.append("clear")
	options_list.append("version")
	options_list.append("research")
	options_list.append("missionlist")
	options_list.append("missiondetails")
	options_list.append("stockmarket")
	options_list.append("stocks")
	options_list.append("stockbuy")
	options_list.append("hide")
	options_list.append("unhide")
	options_list.append("servertime")
	options_list.append("portscan")

	
	# if userinput == 'help' or userinput == '?':
		# print("")
		# print("available commands:")
		# localRemote = session.get('local_or_remote')
		# options = ""
		# if localRemote == 'local':
			# #admin_options = ""
			
			
			
			# options_list = sorted(options_list)
			
			# for i in range(0, len(options_list)):
				# options = options + options_list[i]
				# if i < len(options_list)-1:
					# options = options + ", "
		
		# elif localRemote == 'remote':
			# if session.get("remote_admin") == True:
				# options = "?, help, disconnect, dc, local, logview, logdelete, logmodify, dir, processlist*";
			# else:
				# options = "?, help, disconnect, dc, local, serverdbadd, crack, login, missionaccept, missionlist, missiondetails, ftplist, ftpdownload, upload, download";
				# if session.get("has_bulletin_board") == True:
					# options+=", bulletinboard"
				# if session.get("remote_host_is_dns_server") == True:
					# options+=", domainlist, domainregister, domaindelete"
		# print(options)
		# print("")
	if userinput.lower() == "bulletinboard":
		print("")
		if session.get('local_or_remote') == "local":
			print("Bulletinboard can only be viewed from the remote shell")
		else:
			result = client.bulletin_board()
			if not result['error']:
				if len(result['result']) == 0:
					print("No new missions currently available on this server")
				else:
					for i in range(0, len(result['result'])):
						#print(result)
						result['result'][i]['date_time'] = client.timestamp_to_str(result['result'][i]['date_time'])
						result['result'][i]['reward'] = client.credits(result['result'][i]['reward'])
					client.print_table_dictionary("mission_id,type,mission_type,reward,createdate",result['result'])
			else:
				print(result['error_message'])
		print("")
	elif userinput == "domainlist" or userinput == "domainregister" or userinput == "domaindelete":
		print("")
		print("program not implemented")
		print("")
	else:
		if 1==2:
			pass
		else:
			parts = userinput.split(' ')
			parts[0] = parts[0].lower()
			##################################################################################################################################
			if parts[0] == "example":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This is an example program')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "rm" or parts[0] == "delete":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Remove a file or directory')
				parser.add_argument('file_id', metavar="FILE_ID", nargs=1,type=int, default=-1)
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					file_id = None
					if args.file_id != None:
						file_id = args.file_id[0]
					else:
						file_id = client.get_input("file_id>").strip()
					file_id = int(file_id)
					
					result = client.file_delete(file_id)
					if result['error'] == False:
						print("file/directory deleted.")
					
				except:
					#traceback.print_exc()
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "help" or parts[0] == "?":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Show program help')
				parser.add_argument('program', metavar="PROGRAM", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					program = ""
					if args.program[0] != None:
						program = args.program[0]
					if program != "":
						console(program+" -h")
					else:
						print("available commands:")
						localRemote = session.get('local_or_remote')
						options = ""
						if localRemote == 'local':
							#admin_options = ""
							options_list = sorted(options_list)
							for i in range(0, len(options_list)):
								options = options + options_list[i]
								if i < len(options_list)-1:
									options = options + ", "
						elif localRemote == 'remote':
							if session.get("remote_admin") == True:
								options = "?, help, disconnect, dc, local, logview, logdelete, logmodify, dir, processlist*";
							else:
								options = "?, help, disconnect, dc, local, serverdbadd, crack, login, missionaccept, missionlist, missiondetails, ftplist, ftpdownload, upload, download";
								if session.get("has_bulletin_board") == True:
									options+=", bulletinboard"
								if session.get("remote_host_is_dns_server") == True:
									options+=", domainlist, domainregister, domaindelete"
						print(options)
						print("")
				except:
					print("")
			##################################################################################################################################
			elif parts[0] == "quit" or parts[0] == "exit" or parts[0] == "bye" or  parts[0] == "cya":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Exit DQOI')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					global clean_exit
					clean_exit = True
					logout = True
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "portscan":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Scan TCP ports on a target machine')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					print(" Scanning international-academic-database.org ...")
					print(" FTP  21   CLOSED")
					print(" SSH  22   OPEN")
					print(" HTTP 80   OPEN")
					print(" DB   3306 OPEN")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "tutorial":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='DQOI Tutorials')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					Tutorial()
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "serverping":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Displays ping to server time.')
				parser.add_argument('-r','--repeat', type=int, default=0,help='Repeat')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					repeat = False
					if args.repeat > 0:
						repeat = True
					
					global ping
					
					print(str(int(ping*1000))+"ms")
					
					# print("repeat:"+str(repeat))
					
					if repeat:
						while True:
							client.sleepsec()
							print(str(int(ping*1000))+"ms")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "servertime":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program reports the game servers time.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.server_time()
					if result['error'] == False:
						print("Server time is: "+result['server_time'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "hide":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will hide a file.')
				parser.add_argument('fileid', metavar="FILEID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					file_id = -1
					if args.fileid[0] != None:
						file_id = int(args.fileid[0])
					else:
						file_id = int(client.get_input("file_id>").strip())
					
					result = client.file_hide(file_id)
					if result['error'] == False:
						print("Started file hide process")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "unhide":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will unhide a file.')
				parser.add_argument('fileid', metavar="FILEID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					file_id = -1
					if args.fileid[0] != None:
						file_id = int(args.fileid[0])
					else:
						file_id = int(client.get_input("file_id>").strip())
					
					result = client.file_unhide(file_id)
					if result['error'] == False:
						print("Started file unhide process")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "stockbuy":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to buy bonds from the stock market.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					stock_id = int(client.get_input('stock_id>'))
					units = int(client.get_input('units>'))
					
					result = client.stock_buy(stock_id,units)
					if result['error'] == False:
						print("Successfully bought stock")
					
					# print(result)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "stocksell":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to sell your stock market bonds.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					stock_id = int(client.get_input('stock_id>'))
					units = int(client.get_input('units>'))
								
					result = client.stock_sell(stock_id,units)
					
					if result['error'] == False:
						print("Successfully sold stock")
						
					# print(result)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "stockmarket" or parts[0] == "stocks":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will display the bonds market.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					stock_value = 0
					result = client.bonds_market()
					if result['error'] == False:
						for stock in result['result']:
							stock_value += int(str(stock[6]).replace(".",""))
						client.print_table("stock_id,name,price,last_price,interest_rate,units_owned,market_value", result['result'])
						print("")
						print("Portfolio net worth: "+client.credits(stock_value))
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "research":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will research software updates.')
				parser.add_argument('-f','--file-id', type=int, default=0,help='File ID')
				parser.add_argument('-H','--hours', type=int, default=0,help='Number of hours per task')
				parser.add_argument('-t','--tasks', type=int, default=0,help='Number of tasks')
				
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					file_id = 0
					hours = 0
					tasks = 0
					
					if args.file_id > 0 or args.hours > 0 or args.tasks > 0:
						file_id = args.file_id
						hours = args.hours
						tasks = args.tasks
					else:
						file_id = int(client.get_input("file_id>"))
						hours = int(client.get_input("hours>"))
						tasks = int(client.get_input("tasks>"))
					
					result = client.research(file_id,hours,tasks)
					# print(result)
					tasks = result['result']
					for task in tasks:
						if task['error']:
							print(task['error_message'])
						else:
							print("created process id %s" % (task['process_id'],))
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "cls" or parts[0] == "clear":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program clears the console.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					clear()
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "time":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program displays how much time you have.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					print("You have "+str(client.get_time()['time'])+" time")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "copy" or parts[0] == "cp":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program copies a file.\n\nSource can be file id but destination must be a path')
				parser.add_argument('source', metavar="SOURCE", nargs=1,action='append')
				parser.add_argument('destination', metavar="DESTINATION", nargs=1,action='append')
				
				del parts[0]
				#print(parts)
				## CODE TO HANDLE QUOTES ##
				tmp_str = " ".join(parts)
				#print(tmp_str)
				partsIndex = -1
				parts = []
				open_quotes = False
				for char in tmp_str:
					if char == "\"":
						open_quotes = not open_quotes
					else:
						if partsIndex == -1:
							parts.append("")
							partsIndex = partsIndex + 1 
						if char == " " and open_quotes == False:
							parts.append("")
							partsIndex = partsIndex + 1
						else:
							parts[partsIndex] = parts[partsIndex] + char
				#print(parts)
				## CODE TO HANDLE QUOTES ##
				
				try:
					args = parser.parse_args(parts)
					
					pathFrom = ""
					pathTo = ""
					
					#print(args)
					
					if args.source != None:
						pathFrom = args.source[0][0]
					else:
						pathFrom = client.get_input("pathfrom>")
					
					if args.destination != None:
						pathTo = args.destination[0][0]
					else:
						pathTo = client.get_input("pathto>")
					
					#print("source="+pathFrom)
					#print("destination="+pathTo)
					
					result = client.file_copy(pathFrom,pathTo)
					
					if result['error'] == False:
						print("Started file copy process")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "collectall":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program collects profits from all your software.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.collect_all()
					#print(result)
					if result['error']:
						print(result['error_message'])
						#print("")
					else:
						print(result['output'])
						print("total profit: "+str(result['total_profit']))
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "collect":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program collects profits from one process.')
				parser.add_argument('processid', metavar="PROCESSID", nargs='?',action='append')
				
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
						
					processid = -1
					if args.processid[0] != None:
						processid = long(args.processid[0])
					else:
						processid = long(client.get_input("processid>").strip())
				
					
					result = client.collect(processid)
					#print(result)
					if result['error']:
						print(result['error_message'])
						#print("")
					else:
						print(result['output'])
						print("total profit: "+str(result['total_profit']))
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "software":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program lists all your installed virii.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.software()
					if len(result['result'])==0:
						print("you havent installed any software")
					else:
						client.print_table("process_id,file_id,type,details,version,run_hours",result['result'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "transferbw":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to adjust the bandwidth rate of a file transfer.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					processid = int(client.get_input("processid>"))
					bandwidth = float(client.get_input("bandwidth>"))
					
					result = client.adjust_bandwidth(processid,bandwidth)
					if result['error']:
						print(result['error_message'])
					else:
						print("Process bandwidth successfully adjusted")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "upload":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program uploads files to the remote server.')
				parser.add_argument('fileid', metavar="FILEID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					file_id = -1
					if args.fileid[0] != None:
						file_id = int(args.fileid[0])
					else:
						file_id = int(client.get_input("file_id>").strip())
					
					result = client.file_upload(file_id)
					if result['error'] == False:
						print("Successfully started uploading file to remote server")
					
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "filetransfers" or parts[0] == "transfers":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program displays active file transfers')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.file_transfers()
					
					#print(result)
					
					if len(result['result']) == 0:
						print("You do not have any active file transfers")
					else:
						client.print_table("id,type,bandwidth,details",result['result'])
					
					print("")
					print("%s/%s Kbs Bandwidth %s%%" % (result['net_used'],result['net_total'],int(result['net_load'])))
				
					if result['net_used'] > result['net_total']:
						print("")
						print("Hardware overload!")
				
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "fileperms":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to set a file to public or private. Public files will appear in your public FTP.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					file_id = int(client.get_input("file_id>").strip())
					print("[1] Public [2] Private")
					option = int(client.get_input("permission>").strip())
					if option == 1:
						result = client.file_permissions(file_id, True)
						if result['error']:
							print(result['error_message'])
						else:
							print("File successfully made public")
					elif option == 2:
						result = client.file_permissions(file_id, False)
						if result['error']:
							print(result['error_message'])
						else:
							print("File successfully made private")
					else:
						print("Invalid option selected")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "ftpdownload" or parts[0] == "download":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program downloads files from a remote server.')
				#parser.add_argument('bandwidth', metavar="BANDWIDTH", nargs='?',action='append')
				parser.add_argument('fileid', metavar="FILEID", nargs='?',action='append')
				del parts[0]
				#try:
				args = parser.parse_args(parts)
				
				file_id = -1
				if args.fileid[0] != None:
					file_id = int(args.fileid[0])
				else:
					file_id = int(client.get_input("file_id>").strip())
				result = client.file_download(file_id)
				if result['error'] == False:
					print("Successfully started file download from remote server")
				else:
					print(result['error_message'])
				
				#except:
				#	pass
				print("")
			##################################################################################################################################
			elif parts[0] == "ftplist":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program lists files on the remote public FTP.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.public_ftp()
					
					if len(result['result'])==0:
						print("There are no files available on the remote servers public FTP")
					else:
						for file in result['result']:
							file[4]=str(client.bytesto(file[4],'m'))+"mb"
							# file[4]=bytesToSize(file[4])
						client.print_table("id,type,name,version,size",result['result'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "missioncomplete":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Use this program to complete a mission')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					mission_id = int(client.get_input("mission_id>").strip())
					code = client.get_input("code>")
					print("")
					
					result = client.mission_complete(mission_id,code)
					if result['error']:
						print(result['error_message'])
					else:
						if config_colors_disabled:
							print("Mission successfully completed!")
							print("You have been awarded "+client.credits(result['reward'])+" credits")
						else:
							print(Fore.YELLOW+"Mission successfully completed!"+Fore.WHITE)
							print(Fore.GREEN+"You have been awarded "+client.credits(result['reward'])+" credits"+Fore.WHITE)
						
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "bankloan" or parts[0] == "loan":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='Take or repay a bank loan')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.bank_loan_taken()
					if result['loan_taken'] == False:
						print("Would you like to take out a loan of 0.07500000 credits for a 10% fee?")
						#print("Warning: This may affect your power adversely until the loan is repaid.")
						print("[Y]es [N]o")
						input = client.get_input(">").strip().upper()
						if input == "Y":
							result = client.bank_loan_take()
							if result['error']:
								print(result['error_message'])
							else:
								print("Loan application successfull.")
								print("Your bank has been credited with 0.07500000 credits")
					else:
						print("Are you ready to repay your loan of 0.07500000 credits at a 10% expense?")
						print("The total amount to repay is 0.08250000 credits.")
						print("[Y]es [N]o")
						input = client.get_input(">").strip().upper()
						if input == "Y":
							result = client.bank_loan_repay()
							if result['error']:
								print(result['error_message'])
							else:
								print("0.082500000 credits has been withdrawn from your account.")
								print("You have successfully payed off your loan.")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "missiondetails":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='View mission details')
				parser.add_argument('missionid', metavar="MISSIONID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					mission_id = -1
					if args.missionid[0] != None:
						mission_id = int(args.missionid[0])
					else:
						mission_id = int(client.get_input("mission_id>").strip())
					
					result = client.mission_details(mission_id)
					
					if result['error']:
						print(result['error_message'])
					else:
						print(result['details'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "missionlist":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will list accepted missions.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.mission_list()
					
					if result['missions_completed_by_other_users'] != 0:
						print(str(result['missions_completed_by_other_users'])+" mission(s) have been removed having been completed by someone else!")
						print("")
					
					if len(result['result']) == 0:
						print("You havent any missions")
					else:
						client.print_table("id,target_ip,type,reward",result['result'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "missionaccept":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will accept a mission from the remote server.')
				parser.add_argument('missionid', metavar="MISSIONID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					mission_id = -1
					if args.missionid != None:
						mission_id = int(args.missionid[0])
					else:
						mission_id = client.get_input("mission_id>")
					
					result = client.mission_accept(int(mission_id))
					if result['error']:
						print(result['error_message'])
					else:
						print("Mission successfully accepted")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "userranks" or parts[0] == "ranks":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will display the user rankings.')
				del parts[0]
				# try:
				args = parser.parse_args(parts)
				
				result = client.user_ranks()
				
				print("There are "+str(len(result['result']))+" players in the world")
				print("")
				
				for i in range(0,len(result['result'])):
					# print(result['result'][i])
					result['result'][i] = [result['result'][i][0],result['result'][i][1],result['result'][i][2],intWithCommas(int(result['result'][i][3]))]
				
				max_width = 0
				for i in range(0,len(result['result'])):
					if len(str(result['result'][i][3])) > max_width:
						max_width = len(str(result['result'][i][3]))
				
				for i in range(0,len(result['result'])):
					while len(result['result'][i][3]) < max_width:
						result['result'][i][3] = " "+result['result'][i][3]
				
				client.print_table("rank,user,servers,power",result['result'])
				
				# except:
					# pass
				print("")
			##################################################################################################################################
			elif parts[0] == "logrecover":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='A program for recovering a deleted or modified log record.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					logid = client.get_input("logid>")
					remote = session.get("local_or_remote")=="remote"
					result = client.log_recover(int(logid),remote)
					print(result)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "gatewayupgrade" or parts[0] == "upgrade":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program provides upgrades to your gateways.')
				parser.add_argument('-c','--cpu', type=int, default=0,help='CPU Mhz')
				parser.add_argument('-m','--mem', type=int, default=0,help='MEM Mb')
				parser.add_argument('-d','--hdd', type=int, default=0,help='HDD Gb')
				parser.add_argument('-n','--net', type=int, default=0,help='NET Kb')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = []
					cpu = 0
					mem = 0
					hdd = 0
					net = 0
					
					if args.cpu > 0 or args.mem > 0 or args.hdd > 0 or args.net > 0:
						cpu = args.cpu
						mem = args.mem
						hdd = args.hdd
						net = args.net
					else:						
						print(client.credits("300")+" per CPU Mhz")
						cpu = int(client.get_input("mhz>"))
						print(client.credits("5000")+" per MEM Mb")
						mem = int(client.get_input("mb>"))
						print(client.credits("30000")+" per HDD Gb")
						hdd = int(client.get_input("gb>"))
						print(client.credits("30000")+" per NET Kb")
						net = int(client.get_input("kb>"))
						
					total_cost = (300 * cpu) + (5000 * mem) + (30000 * hdd) + (30000 * net)
					
					if cpu > 0:
						print("Upgrading CPU by "+str(cpu)+" Mhz ...")
					if mem > 0:
						print("Upgrading MEM by "+str(mem)+" Mb ...")
					if hdd > 0:
						print("Upgrading HDD by "+str(hdd)+" Gb ...")
					if net > 0:
						print("Upgrading NET by "+str(net)+" Kb ...")
					
					result = client.gateway_upgrade(session.get("selected_gateway_id"), cpu, mem, hdd, net)
					if result['error'] == False:
						print("Gateway successfully upgraded. "+client.credits(str(total_cost))+" deducted from your bank.")
					# else:
						# print(result['error_message'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "gatewaybuy":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to purchase a new gateway.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.gateway_list()
					gateway_count = len(result['result'])
					cost = 2000000
					for i in range(1,gateway_count):
						cost = cost * 2
					print("A new gateway will cost "+client.credits(str(cost)))
					print("Are you sure you wish to purchase a new gateway?")
					print("[Y]es [N]o")
					answer = client.get_input(">")
					if answer.strip().upper() == "Y":
						result = client.gateway_buy()
						if result['error'] == False:
							print("A new gateway has been purchased for "+client.credits(str(cost))+" credits!")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "processkill" or parts[0] == "pkill" or parts[0] == "kill":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will kill a process.')
				parser.add_argument('processid', metavar="PROCESSID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
						
					processid = -1
					
					if args.processid[0] != None:
						processid = int(args.processid[0])
					else:
						processid = int(client.get_input("pid>"))
					
					result = client.process_kill(processid)
					# print("")
					if result['error'] == False:
						print("process "+str(processid)+" stopped.")
					# print("")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "logmodify":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program can delete or modify a log.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					logid = int(client.get_input("logid>"))
					logmessage=client.get_input("logmessage>")
					result = client.log_delete(logid, logmessage,session.get("local_or_remote")=="remote")
					# print(result)
					if result['error']:
						print(result['error_message'])
					else:
						print("log successfully modified")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "logdelete":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program can delete or modify a log.')
				parser.add_argument('logid', metavar="LOGID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					logid = -1
					if args.logid[0] != None:
						logid = int(args.logid[0])
					else:
						logid = int(client.get_input("logid>").strip())
					
					result = client.log_delete(logid, "",session.get("local_or_remote")=="remote")
					if result['error'] == False:
						print("log deleted.")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "processcomplete" or parts[0] == "complete":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will complete a process.')
				parser.add_argument('processid', metavar="PROCESSID", nargs='?',action='append')
				del parts[0]
				# try:
				args = parser.parse_args(parts)
				
				
				pid = -1
				if args.processid[0] != None:
					pid = args.processid[0]
				else:
					pid = client.get_input("pid>")
				# if str(pid) == str(int(pid)):
					# pid = int(pid)
				result = client.process_complete(pid,session.get("local_or_remote")=="remote")
				if result['error']:
					print(result['error_message'])
				else:
					for process in result['result']:
						message = "success (-"+str(process['time'])+" time)"
						if process['error']:
							message = process['error_message']
						print("pid "+str(process['process_id'])+": "+message)
						if not process['error']:
							# print(process)
							if process['new_ip'] != None and process['new_ip'] != "":
								session.set('selected_gateway_ip_address',process['new_ip'])
							if process['gateway_ip_address'] != None and process['gateway_ip_address']!="":
								print("Password for "+process['gateway_ip_address']+" acquired. Server database updated.")
								if process['mission_completed'] == True:
									print("Mission successfully completed! Your bank balance has been credited.")
				# except:
					# pass
				print("")
			##################################################################################################################################
			elif parts[0] == "logview" or parts[0] == "logs":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program displays local or remote logs.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					log_view(1)
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "serverdbdelete":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program deletes a server database entry.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					id = int(client.get_input("id>"))
					result = client.server_database_delete(id)
					print(result)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "stats":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This is an admin program.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.server_stats_onetime()
					print(result)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "connlist":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This is an admin program.')
				del parts[0]
				try:
					args = parser.parse_args(parts)

					result = client.admin_connection_list()
					if not result['error']:
						columns = 'sid,authenticated,user_id,handle,is_admin,subscribed_to_server_stats,ip_address,last_action'
						rows = []
						for connection in result['result']:
							rows.append([connection['sid'],connection['authenticated'],connection['user_id'],connection['handle'],connection['is_admin'],connection['subscribed_to_server_stats'],connection['ip_address'],client.timestamp_to_str(connection['last_action'])])
						
						client.print_table(columns, rows)
						
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "sqlquery":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This is an admin program.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
								
					query = client.get_input("sql>")
					result = client.admin_sql_query(query)
					if result['error']:
						print('error: '+result['error_message'])
					else:
						columns = result['columns']
						rows = result['rows']
						client.print_table(client.list_to_str(columns),rows)
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "install":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program installs another program.')
				parser.add_argument('fileid', metavar="FILEID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					fileid = -1
					
					if args.fileid[0] != None:
						fileid = int(args.fileid[0])
					else:
						fileid = int(client.get_input("fileid>"))
					
					result = client.install(fileid)
					if result['error'] == True:
						#print(result['error_message'])
						pass
					else:
						print("program installing...")
					
				except:
					print("an error occured")
				print("")
			##################################################################################################################################
			elif parts[0] == "processstart" or parts[0] == "run":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program starts a process.')
				parser.add_argument('fileid', metavar="FILEID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					fileid = -1
					
					if args.fileid[0] != None:
						fileid = int(args.fileid[0])
					else:
						fileid = int(client.get_input("fileid>"))
					
					result = client.process_create(fileid)
					if result['error'] == True:
						# print(result['error_message'])
						pass
					else:
						print("process started.")
					
				except:
					print("an error occured")
				print("")
			##################################################################################################################################
			elif parts[0] == "serverdbadd":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program adds the connected gateway to your server database.')
				parser.add_argument('-a','--addr',help='ip address')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					result = []
					if args.addr != None and args.addr != "":
						print("adding "+args.addr+" to server database...")
						result = client.server_database_add(args.addr)
					else:
						result = client.server_database_add()
					if result['error'] == False:
						print("ip address added to server database.")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "processlist" or parts[0] == "ps":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program lists running processes.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = []
					if session.get("local_or_remote") == "remote":
						print("getting remote process list...")
						print("")
						result = client.process_list(True)
					else:
						print("getting local process list...")
						print("")
						result = client.process_list(False)
						
					if result['error']:
						print(result['error_message'])
						
					if len(result['result']) == 0:
						print("no processes running")
					else:
						for process in result['result']:
							if process[3] == -1:
								process[3] = "idle"
							elif process[3] == 0:
								process[3] = "complete"
							else:
								process[3] = client.seconds_to_time_str(process[3])
						client.print_table('process_id,software_type,details,remaining_time,version,cpu(mhz),mem(kb),net(kbps)', result['result'])
					print("")
					#print((result['cpu_used'],result['cpu_total'],int(result['cpu_load']),result['mem_used'],result['mem_total'],int(result['mem_load']),result['net_used'],result['net_total'],int(result['net_load'])))
					print("load average %s/%s Mhz CPU %s%%, %s/%s Kb Mem %s%%, %s/%s Kbs Bandwidth %s%%" % (result['cpu_used'],result['cpu_total'],int(result['cpu_load']),result['mem_used'],result['mem_total'],int(result['mem_load']),result['net_used'],result['net_total'],int(result['net_load'])))
				
					if result['cpu_used'] > result['cpu_total'] or int(result['mem_used']) > result['mem_total'] or result['net_used'] > result['net_total']:
						print("")
						print("Hardware overload!")
				
				except:
					pass
				#	e = sys.exc_info()[0]
				#	print( "<p>Error: %s</p>" % e )
				#	pass
				print("")
			##################################################################################################################################
			elif parts[0] == "gatewayselect":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to switch the active gateway.')
				parser.add_argument('gateway_id', metavar="GATEWAY_ID", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
								
					gateway_id = ""
					if args.gateway_id[0] != None:
						gateway_id = int(args.gateway_id[0])
					else:
						gateway_id = int(client.get_input('gateway_id>'))
					
					result = client.gateway_select(int(gateway_id))
					if result['error']:
						print(result['error_message'])
					else:
						print("gateway changed.")
						# print(result)
						session.set('selected_gateway_id',gateway_id)
						session.set('selected_gateway_hostname',result['gateway_hostname'])
						session.set('selected_gateway_ip_address',result['gateway_ip_address'])
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "gatewaylist" or parts[0] == "gateways":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will list the gateways that you own.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.gateway_list()
					client.print_table_dictionary('id,host_name,ip_address,cpu,mem,hdd,bw',result['result'])
		
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "changepassword":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to change the gateway password.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					result = client.gateway_change_password()
					if result['error']:
						print(result['error_message'])
					else:
						print(" Gateway password change in progress...")
						print(" 60 minutes remaining... kernel running software...")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "changeip":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to change the gateway ip address.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					print("WARNING! It costs 0.00100000 Credits to change gateway IP!")
					print("All remote connections on this server will be dropped.")
					print("All un-owned virii on this server will be disabled but not neutralized!")
					print("Time and Credit cost is deducted when the IP Change process starts.")
					print("")
					print("[1] 24 hours no time cost")
					print("[2] 20 hours 600 time cost")
					print("[3] 16 hours 1500 time cost")
					print("[4] 12 hours 2500 time cost")
					print("[5] 6 hours 4500 time cost")
					input = int(client.get_input(">"))
					if input >= 1 and input <= 5:
						result = client.gateway_change_ip(input)
						if result['error']:
							print(result['error_message'])
						else:
							print(" Gateway change ip process successfully started...")
						# print(result)
					else:
						print("invalid option")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "accountsettings":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to change your account settings.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					print("[1] Change Password")
					print("[2] Cancel")
					option = int(client.get_input(">"))
					if option == 1:
						cp = client.get_input("currentpassword>")
						np = client.get_input("newpassword>")
						rp = client.get_input("repeatpassword>")
						if np != rp:
							print("repeated password did not match, try again")
						else:
							result = client.user_change_password(currentPassword=cp, newPassword=np)
							print(result)
							

				
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "disconnect" or parts[0] == "dc":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will disconnect from the remote host.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					if session.get("connected") == True:
						gateway_disconnect()
					else:
						print("not connected")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "userlist" or parts[0] == "users":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program lists all the users.')
				parser.add_argument('-s','--search', type=str, default='',help='Search criteria')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.user_list(pageSize = 100, pageNumber = 1, searchCriteria = args.search)
					client.print_table_dictionary('id,handle',result['result'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "banktransfer" or parts[0] == "transfer":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program performs a bank transfer.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					to = client.get_input('to>')
					amount = client.get_input('amount>')
					result = client.bank_transfer(to,amount)
					# print(result)
					if result['error'] == False:
						print("Successfully sent monies to recipient")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "banktransactions" or parts[0] == "transactions":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program lists your bank transactions.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					page_number = 1
					page_size = 20 # max 100 
					
					running = True
					while running:
						
						result = client.bank_transactions(pageSize=page_size,pageNumber=page_number)
						if len(result['result']) == 0:
							print('there are no bank transactions to display')
							running = False
						else:
							for row in result['result']:
								#print(row)
								row['original'] = client.credits(str(row['original']))
								row['amount'] = client.credits(str(row['amount']))
								row['remaining'] = client.credits(str(row['remaining']))
								row['date_time'] = client.timestamp_to_str(row['date_time'])
							client.print_table_dictionary('type,original,amount,remaining,date_time',result['result'])
							if len(result['result']) == page_size:
								print("Page: "+str(page_number))
								print("[P]revious [N]ext [Q]uit")
							input = client.get_input(">").strip().lower()
							if input == 'n':
								page_number += 1
							elif input == 'p':
								page_number -= 1
							else:
								running = False
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "destroy":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program destroys installed software')
				parser.add_argument('process_id', metavar="PROCESS_ID", nargs=1,type=int, default=-1)
				#parser.add_argument('host', metavar="HOST", nargs='?',action='append')
				
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					process_id = None
					if args.process_id != None:
						process_id = args.process_id[0]
					else:
						process_id = client.get_input("process_id>").strip()
					process_id = int(process_id)
					
					result = client.destroy(process_id)
					if result['error'] == False:
						print("software destroyed.")
					
					# print("function not implemented")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "bankbalance" or  parts[0] == "balance" or  parts[0] == "bank":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program displays your bank balance')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.bank_balance()
					balance = str(result['balance'])
					print("credits: "+client.credits(balance))
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "login":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will login to the remote gateway as root.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result = client.admin_login()
					if result['error'] == False:
						session.set("remote_admin", True)
						print("successfully logged in")
						session.set('local_or_remote','remote')
					else:
						print(result['error_message'])
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "cd":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program changes the working directory.')
				#parser.add_argument('-d', '--dmp', nargs='+', ...)
				parser.add_argument('path', metavar="PATH", nargs='+')
				#path = userinput[len(parts[0])+1:len(userinput)]
				del parts[0]
				try:
					args = parser.parse_args(parts)
					path = ' '.join(args.path)
					if path.strip() == "":
						path = client.get_input("path>").strip()
					#print("path:"+path)
					remote = session.get("local_or_remote") == "remote"
					result = client.directory_change(path,remote)
					#print(str(result))
					if not result['error']:
						#print("directory changed")
						if not remote:
							session.set("local_working_directory", result['working_directory'])
						else:
							session.set("remote_working_directory", result['working_directory'])
				except:
					#traceback.print_exc()
					print("")
					pass
				#print("")
			##################################################################################################################################
			elif parts[0] == "mkdir":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program creates directory folders.')
				parser.add_argument('path', metavar="PATH", nargs='+')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					path = ' '.join(args.path)
					if path.strip() == "":
						path = client.get_input("path>").strip()			
					result = client.directory_create(path)
					if result['error']:
						print('error: '+result['error_message'])
					else:
						print('directory created')
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "crack":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program cracks the admin password of the remote computer.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					local_or_remote = session.get("local_or_remote")
					if False: #local_or_remote == 'remote':
						#print("you already have root access")
						pass
					else:
						result = client.admin_crack()
						#print(result)
						if result['error']:
							print('error: '+result['error_message'])
							if result['error_message'] == 'select a password breaker to use to crack the password':
								password_breakers = len(result['password_breakers'])
								if password_breakers == 0:
									print("no password breakers running.")
								else:
									print("select password breaker to run")
									print("")
									client.print_table("process_id,details,version,associated_file_id",result['password_breakers'])
									print("")
									password_breaker_id = int(client.get_input("crackerid>"))
									print('attempting to crack password using pwb #'+str(password_breaker_id))
									result = client.admin_crack(password_breaker_id)
									if result['error'] == False:
										print("successfully started to crack sever login")
									#print(result)
						else:
							print('successfully started to crack admin')
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == str_command_dir or parts[0] == "ls":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program prints a directory contents.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					
					result=[]
					if session.get("local_or_remote") == "local":
						result = client.directory_list()
					else:
						result = client.directory_list_remote()
					if len(result['result']) == 0:
						print("directory empty")
					else:
						for file in result['result']:
							file[3]=str(client.bytesto(file[3],'m'))+"mb"
							# file[3]=bytesToSize(file[3])
						client.print_table('id,type,name,size_mb,version,is_folder,public',result['result'])
						print("")
						print("load average HDD %s/%s Gb (%s%%)" % ("%.2f" % float(result['hdd_used']),result['hdd_total'],int(result['hdd_load']),))
					
					if result['hdd_load'] > 100:
						print("")
						print("Warning! HDD Space Overloaded!")
					
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "serverdb":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program prints the server database.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					print_server_database_list(client.server_database_list(pageSize = 100, pageNumber = 1))
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "setmotd":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will set the motd.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					motd = client.get_input('motd>')
					if motd.strip() == '':
						motd = session.get("username")+"'s Dedicated Server\nA dedicated server used to connect to the world wide network."
					result = client.motd_set(motd)
					if result['error']:
						print(result['error_message'])
					print(result)
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "motd":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will print the motd.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					result = client.motd_get()
					motd = result['motd'].replace("\\n","\n")
					print(motd)
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "pingscan":
				print("")
				#parser = argparse.ArgumentParser(prog=parts[0], description='This program will ping scan a wide range of ip addresses.')
				#parser.add_argument('--start', type=int, default=0,help='integer to start from')
				#parser.add_argument('--count', type=int, default=10,help='count to scan')
				#del parts[0]
				#try:
				#	args = parser.parse_args(parts)
				
				print("starting pingscan1")
				
				start = 0
				count = 1000000
				
				#args = {'count':1000000,'start':0}
				
				#if args.count > 21474836:
				#	print("count size too large")
				#elif args.start > 21474836:
				#	print("start size too large")
				#else:
				print("starting pingscan")
				begin = ipv3.find_start_combination(256,3)
				#total = ipv3.find_total_combinations(256,3)
				l = []
				begin+=start
				for i in range(0,256):
					l.append(str(i))
				for i in range(0,count):
					ip = ipv3.inttostr(begin+i,l,".")
					print("pinging...")
					result = client.gateway_ping(ip)
					if result['error'] == False:
						print(ip+" SUCCESS")
					else:
						print(ip+" FAIL")
				#except:
				#	pass
				print("")
			##################################################################################################################################
			elif parts[0] == "local":
				#print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will switch to the local shell.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
				
					if session.get('local_or_remote') == "local":
						print("You are already using the local shell")
					else:
						session.set('local_or_remote','local')
				except:
					pass
				#print("")
			##################################################################################################################################
			elif parts[0] == "remote":
				#print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will switch to the remote shell.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					if session.get('connected') == True:
						if session.get('local_or_remote') == "remote":
							print("You are already using the remote shell")
						else:
							session.set('local_or_remote','remote')
					else:
						print("You are not connected to a remote shell")
				except:
					pass
				#print("")
			##################################################################################################################################
			elif parts[0] == "connect":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will connect to the specified host.')
				parser.add_argument('host', metavar="HOST", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					host = ""
					if args.host[0] != None:
						host = args.host[0]
					else:
						host = client.get_input('host>')
					
					if host.strip().upper()=="LOCALHOST":
						host = session.get('selected_gateway_ip_address')
					
					session.set("remote_admin", False)
					ip_or_domain = host
					result = client.gateway_connect(ip_or_domain)
					#print(result)
					if result['error']:
						print('error: '+result['error_message'])
						print("")
					else:
						print('connected.')
						session.set('connected',True)
						#session.set('is_admin', result['is_admin'])
						session.set('connection_route', result['connection_route'])
						session.set('local_or_remote','remote')
						session.set('connected_hostname',result['remote_host']['host_name'])
						session.set('connected_ip_address',result['remote_host']['ip_address'])
						session.set('remote_host_motd', result['remote_host']['motd'])
						session.set('remote_host_is_dns_server', result['remote_host']['is_dns_server'])
						session.set('has_bulletin_board', result['remote_host']['has_bulletin_board'])
						#print(result)
						print("")
						print(session.get("remote_host_motd").replace("\\n","\n"))
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "ping":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program will ping the specified host.')
				parser.add_argument('host', metavar="HOST", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					host = ""
					if args.host[0] != None:
						host = args.host[0]
					else:
						host = client.get_input('host>')
					result = client.gateway_ping(host)
					if result['error'] == False:
						print("Pinging {} with 16 bytes of data:".format(result['ip_address']))
						for i in range(0,4):
							time = 68
							if i == 1: time = 67
							elif i == 2: time = 65
							print("Reply from {}: bytes=16 time={}ms TTL=56".format(result['ip_address'], time))
							client.sleepsec()
						print("Ping statistics for {}:".format(result['ip_address']))
						print("Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),")
						print("Approximate round trip times in milli-seconds:")
						print("Minimum = 65ms, Maximum = 68ms, Average = 67ms")
					else:
						print("Ping request could not find host '{}'. Please check the name and try again.".format(host))
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "hostname":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program prints or sets the gateway hostname.')
				parser.add_argument('hostname', metavar="HOSTNAME", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					hostname = ""
					if args.hostname[0] != None:
						hostname = args.hostname[0]
					else:
						hostname = client.get_input('hostname>')
					result = client.gateway_hostname(hostname)
					if result['error'] == False:
						session.set('selected_gateway_hostname',hostname)
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == str_command_nslookup:
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program looks up a host on the configured name server.')
				parser.add_argument('host', metavar="HOST", nargs='?',action='append')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					#print(args)
								
					host = ""
					if args.host[0] != None:
						host = args.host[0]
					else:
						host = client.get_input('host>')
					print("looking up '{}'...".format(host))
					result = client.dns_lookup(host)
					if result['error'] == True:
						#print(result['error_message'])
						pass
					else:
						print("")
						print("    IP Address. . . . . . : "+result['ip'])
						print("    Domain. . . . . . . . : "+result['domain'])
						if result['can_add_to_server_database'] == True:
							print("")
							print("Ip address not in database, add it?")
							print("[Y]es [N]]o")
							response = client.get_input(">").strip().upper()
							if response == 'Y':
								result = client.server_database_add(result['ip'])
								if result['error'] == False:
									print("ip address added to server database.")
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "netconfig":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program displays network adapter configurations.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					print("    Description . . . . . : LightSpeed Network Adapter")
					print("    Physical Address. . . : "+client.randmac2(6*session.get('selected_gateway_id')))
					print("    IPv3 Address. . . . . : "+session.get('selected_gateway_ip_address'))
					print("    DNS Server. . . . . . : "+session.get('selected_gateway_dns_ip_address'))
					print("    Host Name . . . . . . : "+session.get('selected_gateway_hostname'))
				except:
					pass
				print("")
			##################################################################################################################################
			elif parts[0] == "mail":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program allows you to view and send mail.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
					mail_inbox(1)
					skip = True
				except:
					pass
				print("")
			##################################################################################################################################
			#elif parts[0] == 'example':
			#	print("")
			#	parser = argparse.ArgumentParser(prog=parts[0], description='This is an example program.')
			#	parser.add_argument('--foo', help='foo of the %(prog)s program')
			#	del parts[0]
			#	#print(parts)
			#	try:
			#		args = parser.parse_args(parts)
			#		print(args)
			#	except:
			#		#parser.print_help()
			#		pass
			#	print("")
			##################################################################################################################################
			elif parts[0] == "version":
				print("")
				parser = argparse.ArgumentParser(prog=parts[0], description='This program displays the dqoimp client version.')
				del parts[0]
				try:
					args = parser.parse_args(parts)
									
					print(" ____  _____ _____ _____ ")
					print("|    \|     |     |     |")
					print("|  |  |  |  |  |  |-   -|")
					print("|____/|__  _|_____|_____|")
					print("         |__|            ")
					print("v"+version)
					print("")
					print("Don't Quit, Own It! (DQOI) is a multiplayer computer hacking simulation game.")
					print("Copyright (C) 2020 boorishpea")
					print("")
					print("This program is free software: you can redistribute it and/or modify")
					print("it under the terms of the GNU General Public License as published by")
					print("the Free Software Foundation, either version 3 of the License, or")
					print("(at your option) any later version.")
					print("")
					print("This program is distributed in the hope that it will be useful,")
					print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
					print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
					print("GNU General Public License for more details.")
					print("")
					print("You should have received a copy of the GNU General Public License")
					print("along with this program.  If not, see <https://www.gnu.org/licenses/>.")
				except:
					pass
				print("")
			##################################################################################################################################
			elif userinput.strip() != "":
				print("")
				print("invalid command")
				dict = {}
				for command in options_list:
					dict[command] = levenshtein_percent(command,userinput.strip())
				sorted_dict = sorted(dict.items(), key=operator.itemgetter(1))
				sorted_dict = collections.OrderedDict(sorted_dict)
				keys = list(sorted_dict.keys())
				if sorted_dict[keys[len(keys)-1]] > 0.5:
					print("did you mean "+keys[len(keys)-1]+"?")
				#print(str(sorted_dict))
				print("")
	
	if logout:
		dqoi_client.user_logout()
	elif not skip:
		console()
	

def mail_send(*args):
	#print("mail_send")
	
	#user_id, subject, message
	
	user_id = ""
	if len(args)>=1:
		user_id = str(args[0])
	else:
		user_id = client.get_input('user_id_or_handle>')
	
	subject = ""
	if len(args)>= 2:
		subject = args[1]
	else:
		subject = client.get_input('subject>')
	
	message = ""
	if len(args)>= 3:
		message = args[2]
		message_addition = client.get_input('message>')
		message = message_addition + "\r\n---------------------\r\n"+ message
		print("done")
	else:
		message = client.get_input('message>')

	#print("user_id = "+str(user_id))
	#print("subject = "+str(subject))
	#print("message = "+str(message))



	print("")
	result = client.mail_send(user_id, subject, message)
	if result['error'] == False:
		print("Mail message successfully sent!")
	else:
		print(result['error_message'])
	print("")

def mail_inbox(page):
	
	result = client.mail_inbox(mail_per_page,page)
	
	print("result",result)
	
	next = False
	previous = False
	read = True
	send = True
	delete = True
	
	if page>1:
		previous = True
	
	print(result)
	
	if len(result['result']) == 0:
		print("")
		print('no mail to display')
		read = False
		delete = False
	else:
		print("sponge")
		count = len(result['result'])
		for row in result['result']:
			if row['has_read'] == 0:
				row['has_read'] = "unread"
			else:
				row['has_read'] = "read"
			row['date_time'] = client.timestamp_to_str(row['date_time'])
		
		print("sponge")
		
		client.print_table_dictionary('id,from,subject,status,date_time',result['result'])
			
		next = False
		if count == mail_per_page:
			next = True
	
	options = ""
	if next: options+="[N]ext "
	if previous: options+="[P]revious "
	if read: options+="[R]ead "
	if send: options+="[S]end "
	if delete: options+="[D]elete "
	options+= "[Q]uit ";
	print("")
	print(options)
		
	userinput = client.get_input('option>')
	userinput = userinput.upper().strip()
	if userinput == 'N':
		print("")
		mail_inbox(page+1)
	elif userinput == 'P':
		print("")
		mail_inbox(page-1)
	elif delete and userinput == 'D':
		print("")
		mail_id = int(client.get_input("mailid>"))
		result = client.mail_delete(mail_id)
		if result['error'] == False:
			print("message deleted")
		mail_inbox(page)
	elif userinput == 'R':
		print("")
		mail_id = client.get_input('mail_id>')
		result = client.mail_read(mail_id)
		if result['error'] == True:
			print('error: '+result['error_message'])
			console()
		else:
			print("")
			mail_id = result['result']['id']
			print('Mail ID. . . . . : '+str(mail_id))
			print('From User. . . . : '+str(result['result'][2])+" (#"+str(result['result'][1])+")")
			print('Date Time. . . . : '+client.timestamp_to_str(int(result['result'][3])))
			print('Subject. . . . . : '+str(result['result'][4]))
			print('Message. . . . . : \r\n'+str(result['result'][5]))
			print("")
			print("[I]nbox [D]elete             [R]eply")
			option = client.get_input("option>").upper().strip()
			if option == 'D':
				result = client.mail_delete(mail_id)
				if result['error'] == False:
					print("message deleted")
				print("")
				mail_inbox(page)
			elif option == 'R':
				#print("R is option to mail reply")
				#user_id, subject, message
				mail_send(result['result'][1], result['result'][4], str(result['result'][5]))
				print("")
				console()
				#print("mail send done")
			elif option == 'I':
				# menu
				print("")
				mail_inbox(page)
			else:
				console()
	elif userinput == 'S':
		mail_send()
		mail_inbox(1)
	elif userinput == 'Q':
		print("")
		console()
		pass
	else:
		#print("")
		#print("invalid option")
		print("")
		console()
		
def client_version_check(data):
	
	recommended_parts = dqoi_client.recommended_client_version.split(".")
	current_parts = version.split(".")
	
	#print("recommended_parts",recommended_parts)
	
	if int(recommended_parts[0]) > int(current_parts[0]):
		print("this client version is out of date, please download the new version from the website")
		print("current version = "+version)
		print("recommended version = "+dqoi_client.recommended_client_version)
	elif int(recommended_parts[0]) == int(current_parts[0]) and int(recommended_parts[1]) > int(current_parts[1]):
		print("this client version is out of date, please download the new version from the website")
		print("current version = "+version)
		print("recommended version = "+dqoi_client.recommended_client_version)
	elif int(recommended_parts[0]) == int(current_parts[0]) and int(recommended_parts[1]) == int(current_parts[1]) and int(recommended_parts[2]) > int(current_parts[2]):
		print("this client version is out of date, please download the new version from the website")
		print("current version = "+version)
		print("recommended version = "+dqoi_client.recommended_client_version)
		
		
		
ping = -1
def on_pong(latency):
	global ping
	ping = latency
	pass

if __name__ == "__main__":
	print(" ____  _____ _____ _____ ")
	print("|    \|     |     |     |")
	print("|  |  |  |  |  |  |-   -|")
	print("|____/|__  _|_____|_____|")
	print("         |__|            ")
	parser = argparse.ArgumentParser(description='DQOI Client '+version)
	parser.add_argument('-d', '--disable-colors', action='store_true',help='this option will disable console colors')
	parser.add_argument('--live', action='store_true',help='force to connect to live server')
	run = False
	try:
		args = parser.parse_args()
		config_colors_disabled = args.disable_colors
		
		if args.live:
			dqoi_client_config.force_live = True
			auto_login = False
		
		run = True
	except:
		pass
	if run:
		print("dqoimp_client_"+version)
		dqoi_client.on_client_version(client_version_check)
		if client.connect():
			dqoi_client.ping_enable()
			dqoi_client.on_pong(on_pong)
			main_menu()
		client.disconnect()
		# client.terminate()
		if not clean_exit:
			client.get_input("FIN. PRESS ENTER TO CLOSE")
		