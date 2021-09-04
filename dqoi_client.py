debug_print_message_data = False

#import sys
#reload(sys)
#sys.setdefaultencoding('ascii')

import time
from threading import Thread
import socketio
import dqoi_client_config

import threading
lock = threading.Lock()

## POLLING QUEUE ###########################################################################

packet_cap_cycle_seconds = 2.0
packet_cap_per_cycle = 6
packet_cap_cycle_start = 0
packets_sent_this_cycle = 0

send_queue = []
def send(*args):
	command = args[0]
	data = {}
	if len(args) == 2:
		data = args[1]
	global send_queue
	#print({ 'command': command, 'data': data })
	send_queue.append({ 'command': command, 'data': data })

polling_thread_running = False
def polling_thread():
	global polling_thread_running
	polling_thread_running = True
	global packet_cap_cycle_start
	global packets_sent_this_cycle
	global sio
	global send_queue
	global packet_cap_cycle_seconds
	global packet_cap_per_cycle
	
	packet_cap_cycle_start = time.time()
	while polling_thread_running:
		if time.time() >= packet_cap_cycle_start + packet_cap_cycle_seconds:
			packet_cap_cycle_start = time.time()
			packets_sent_this_cycle = 0
		elif packets_sent_this_cycle < packet_cap_per_cycle:
			if len(send_queue) > 0:
				if is_connected:
					#print('sending packet: '+send_queue[0]['command'])
					if len(send_queue[0]['data']) == 0:
						sio.emit(send_queue[0]['command'])
					else:
						sio.emit(send_queue[0]['command'], send_queue[0]['data'])
					#print("sent")
					send_queue.pop(0)
					packets_sent_this_cycle = packets_sent_this_cycle + 1
		sio.sleep(0.001)

def polling_thread_start():
	t = Thread(target=polling_thread,args=())
	t.setDaemon(True) 
	t.daemon = True
	t.start()

def polling_thread_stop():
	global polling_thread_running
	polling_thread_running = False


## END OF POLLING QUEUE ####################################################################


#sio = socketio.Client(reconnection=False)
sio = socketio.Client(reconnection=True, reconnection_attempts=0, reconnection_delay=1, reconnection_delay_max=5)#, request_timeout = 7200)
sio_connect_complete = False
sio_connected = False

sio_ping_enabled = False
sio_ping_start_time = None

def main_thread(host_url):
	global sio_connect_complete
	try:
		sio.connect(host_url)
		#sio.wait()
	except:
		sio_connect_complete = True

client_thread = None
def connect(host_url):
	global client_thread
	if is_connected():
		return True
	global sio_connect_complete
	sio_connect_complete = False
	sio_connecting = False
	client_thread = Thread(target=main_thread,args=(host_url,))
	
	client_thread.setDaemon(True) 
	client_thread.daemon = True
	
	running = True
	while(running):
		if sio_connecting == False:
			sio_connecting = True
			print("connecting....")
			client_thread.start()
			polling_thread_start()
		elif sio_connect_complete == True:
			running = False
		sio.sleep(0.1)
		#print("waiting to connect...")
		#time.sleep(1)
	return sio_connected

def is_connected():
	global sio_connected
	return sio_connected

def safe_disconnect():
	sio.emit('bye')

def disconnect():
	if is_connected():
		#global client_thread
		#global sio
		#print('if client_thread.is_alive():'+str(client_thread.is_alive()))
		#print('stopping polling thread')
		polling_thread_stop()
		#global client_thread
		print('disconnecting...')
		safe_disconnect()
		#sio.disconnect()
		#print('disconnect sent')
		#if client_thread.is_alive():
		#	client_thread.join(1)
	else:
		print('is not connected')
	return

def ping_send():
	global sio_ping_start_time
	sio_ping_start_time = time.time()
	send('ping_from_client')

#################################################################################################################################################

def test():
	#print("sending test...")
	send('test')

def ping_enable():
	global sio_ping_enabled
	sio_ping_enabled = True
	ping_send()

def ping_disable():
	global sio_ping_enabled
	sio_ping_enabled = False

def subscribe_to_server_stats():
	send('subscribe_to_server_stats')

def unsubscribe_from_server_stats():
	send('unsubscribe_from_server_stats')

def user_register(username, password, secret_question, secret_answer, captcha_key, captcha_solution):
	send('user_register', 
	{
		'username':			username,
		'password':			password,
		'secret_question':	secret_question,
		'secret_answer':	secret_answer,
		'captcha_key':		captcha_key,
		'captcha_solution':	captcha_solution,
	})

def user_login(username, password):
	send('user_login',
	{
		'username': 		username,
		'password':			password,
	})

def user_logout(*args):
	send('user_logout', {})

def user_list(*args):
	page_size = 10
	page_number = 1
	searchCriteria = ""
	if len(args) >= 1:
		page_size = int(args[0])
	if len(args) >= 2:
		page_number = int(args[1])
	if len(args) >= 3:
		searchCriteria = args[2]
	send('user_list',
	{
		'page_size': page_size,
		'page_number': page_number,
		'searchCriteria': searchCriteria,
	})

def mail_inbox(*args):
	page_size = 10
	page_number = 1
	if len(args) >= 1:
		page_size = int(args[0])
	if len(args) >= 2:
		page_number = int(args[1])
	send('mail_inbox',
	{
		'page_size': page_size,
		'page_number': page_number,
	})

def mail_read(*args):
	mail_id = -1
	if len(args) >= 1:
		mail_id = int(args[0])
	send('mail_read',
	{
		'mail_id': mail_id
	})

def mail_delete(*args):
	mail_id = -1
	if len(args) >= 1:
		mail_id = int(args[0])
	send('mail_delete',
	{
		'mail_id': mail_id
	})

def mail_send(user_id_or_handle, subject, message):
	send('mail_send',
	{
		'user_id_or_handle': user_id_or_handle,
		'subject': subject,
		'message': message,
	})

def gateway_list():
	send('gateway_list', {})

def admin_connection_list():
	send('admin_connection_list', {})

def admin_sql_query(sql_query):
	send('admin_sql_query',
	{
		'sql_query': sql_query,
	})

def gateway_select(gateway_id):
	send('gateway_select',
	{
		'gateway_id': gateway_id,
	})

def bank_balance():
	send('bank_balance')

def bank_transfer(user_id_or_handle, amount):
	send('bank_transfer', { 'user_id_or_handle': user_id_or_handle, 'amount': amount })

def bank_transactions(*args):
	page_size = 10
	page_number = 1
	if len(args) >= 1:
		page_size = int(args[0])
	if len(args) >= 2:
		page_number = int(args[1])
	send('bank_transactions',
	{
		'page_size': page_size,
		'page_number': page_number,
	})

def gateway_upgrade(*args):
	if len(args) == 5:
		gateway_id = args[0]
		cpu = args[1]
		mem = args[2]
		hdd = args[3]
		net = args[4]
		send('gateway_upgrade', {
			'gateway_id': gateway_id,
			'cpu': cpu,
			'mem': mem,
			'hdd': hdd,
			'net': net,
		})

def gateway_buy(*args):
	send('gateway_buy')

def user_change_password(*args):
	current_password = args[0]
	new_password = args[1]
	send('user_change_password', {
		'current_password': current_password,
		'new_password': new_password,
	})

def user_validate_password(password):
	send('user_validate_password', {
		'password': password,
	})

def gateway_connect(ip_or_domain):
	send('gateway_connect', {
		'ip_or_domain': ip_or_domain,
	})

def gateway_ping(ip_or_domain):
	send('gateway_ping', {
		'ip_or_domain': ip_or_domain,
	})

def directory_list(*args):
	if len(args) == 0:
		send('directory_list')
	else:
		send('directory_list', { 'path':args[0] })

#todo
def directory_list_remote(*args):
	if len(args) == 0:
		send('directory_list_remote')
	else:
		send('directory_list_remote', { 'path':args[0] })
		
def directory_create(path):
	send('directory_create', { 'path':path })

def directory_change(path,remote=False):
	send('directory_change', { 'path':path,'remote':remote})

def process_list(remote):
	send('process_list', { 'remote':remote })

def admin_login():
	send('admin_login')

def admin_crack(*args):
	if len(args) == 0:
		send('admin_crack')
	else:
		send('admin_crack', { 'password_breaker_id': args[0] })

def process_complete(process_id, remote):
	send('process_complete', { 'process_id': process_id, 'remote': remote })

def log_view(page_size, page_number, remote):
	send('log_view', {
		'page_size': page_size,
		'page_number': page_number,
		'remote': remote,
	})

def gateway_disconnect():
	send('gateway_disconnect')

def server_database_add(*args):
	if len(args) == 0:
		send('server_database_add')
	else:
		send('server_database_add', {
			'ip_address': args[0],
		})

def server_database_list(*args):
	page_size = 20
	page_number = 1
	if len(args) >= 1:
		page_size = int(args[0])
	if len(args) >= 2:
		page_number = int(args[1])
	send('server_database_list',
	{
		'page_size': page_size,
		'page_number': page_number,
	})

def server_database_delete(ids):
	send('server_database_delete', { 'ids': ids })

def gateway_hostname(hostname):
	send('gateway_hostname', { 'hostname': hostname })

def dns_lookup(ip_or_domain):
	send('dns_lookup', { 'ip_or_domain': ip_or_domain })
	
def motd_get():
	send('motd_get')
	
def motd_set(motd):
	send('motd_set',{ 'motd': motd })
	
def process_create(fileid):
	send('process_create', { 'fileid': fileid })

def log_delete(logid,logmessage,remote):
	send('log_delete', { 'logid': logid, 'logmessage': logmessage, 'remote': remote })

def process_kill(pid):
	send('process_kill', { 'pid': pid })

def bulletin_board():
	send('bulletin_board')

def log_recover(logid, remote):
	send('log_recover',{'logid':logid,'remote':remote})

def user_ranks():
	send('user_ranks')

def bank_loan_taken():
	send('bank_loan_taken')
def bank_loan_take():
	send('bank_loan_take')
def bank_loan_repay():
	send('bank_loan_repay')

def mission_accept(mission_id):
	send('mission_accept', { 'mission_id':mission_id})

def mission_list():
	send('mission_list')
	
def mission_details(mission_id):
	send('mission_details', { 'mission_id':mission_id})

def mission_complete(mission_id, code):
	send('mission_complete', {'mission_id':mission_id,'code':code})

def public_ftp():
	send('public_ftp')

def file_permissions(file_id, public):
	send('file_permissions', { 'file_id': file_id, 'public': public })

def file_transfers():
	send('file_transfers')

def file_download(file_id):
	send('file_download', { 'file_id': file_id })

def file_upload(file_id):
	send('file_upload', { 'file_id': file_id })

def secret_question_get(username):
	send('secret_question_get', { 'username': username })

def secret_answer_validate(username,secret_answer):
	send('secret_answer_validate', { 'username': username, 'secret_answer':secret_answer })

def adjust_bandwidth(processid,bandwidth):
	send('adjust_bandwidth', { 'processid': processid, 'bandwidth':bandwidth })

def install(fileid):
	send('install', { 'fileid': fileid })

def software():
	send('software')

def collect_all():
	send('collect_all')

def collect(process_id):
	send('collect',{'process_id':process_id})

def recover(username, secretanswer, newpassword):
	send('recover', { 'username': username, 'secretanswer':secretanswer, 'newpassword':newpassword })

def file_copy(pathFrom,pathTo):
	send('file_copy', { 'pathFrom':pathFrom,'pathTo':pathTo })

def get_time():
	send('time')
	
def gateway_change_password():
	send('gateway_change_password')
	

def gateway_change_ip(speed):
	send('gateway_change_ip',{'speed':speed})
	
def research(file_id,hours,tasks):
	send('research',{'file_id':file_id,'hours':hours,'tasks':tasks})

def bonds_market():
	send('bonds_market')

def stock_buy(bond_id,units):
	send('stock_buy',{'bond_id':bond_id,'units':units})

def stock_sell(bond_id,units):
	send('stock_sell',{'bond_id':bond_id,'units':units})

def file_hide(file_id):
	send('file_hide',{'file_id':file_id})

def file_unhide(file_id):
	send('file_unhide',{'file_id':file_id})

def server_time():
	send('server_time')

def file_delete(file_id):
	send('file_delete',{'file_id':file_id})

def destroy(process_id):
	send('destroy',{'process_id':process_id})

def get_captcha():
	send('get_captcha')

#######################################################################################################################

callback_on_server_stats = None
def on_server_stats(callback):
	global callback_on_server_stats
	callback_on_server_stats = callback

callback_on_disconnect = None
def on_disconnect(callback):
	global callback_on_disconnect
	callback_on_disconnect = callback

callback_on_pong = None
def on_pong(callback):
	global callback_on_pong
	callback_on_pong = callback

callback_on_user_register = None
def on_user_register(callback):
	global callback_on_user_register
	callback_on_user_register = callback

callback_on_test = None
def on_test(callback):
	global callback_on_test
	callback_on_test = callback

callback_on_user_login = None
def on_user_login(callback):
	global callback_on_user_login
	callback_on_user_login = callback

callback_on_user_logout = None
def on_user_logout(callback):
	global callback_on_user_logout
	callback_on_user_logout = callback

callback_on_user_list = None
def on_user_list(callback):
	global callback_on_user_list
	callback_on_user_list = callback

callback_on_mail_inbox = None
def on_mail_inbox(callback):
	global callback_on_mail_inbox
	callback_on_mail_inbox = callback

callback_on_mail_read = None
def on_mail_read(callback):
	global callback_on_mail_read
	callback_on_mail_read = callback

callback_on_mail_delete = None
def on_mail_delete(callback):
	global callback_on_mail_delete
	callback_on_mail_delete = callback

callback_on_mail_send = None
def on_mail_send(callback):
	global callback_on_mail_send
	callback_on_mail_send = callback

callback_on_gateway_list = None
def on_gateway_list(callback):
	global callback_on_gateway_list
	callback_on_gateway_list = callback

callback_on_admin_connection_list = None
def on_admin_connection_list(callback):
	global callback_on_admin_connection_list
	callback_on_admin_connection_list = callback

callback_on_admin_sql_query = None
def on_admin_sql_query(callback):
	global callback_on_admin_sql_query
	callback_on_admin_sql_query = callback

callback_on_gateway_select = None
def on_gateway_select(callback):
	global callback_on_gateway_select
	callback_on_gateway_select = callback

callback_on_bank_balance = None
def on_bank_balance(callback):
	global callback_on_bank_balance
	callback_on_bank_balance = callback

callback_on_bank_transfer = None
def on_bank_transfer(callback):
	global callback_on_bank_transfer
	callback_on_bank_transfer = callback

callback_on_bank_transactions = None
def on_bank_transactions(callback):
	global callback_on_bank_transactions
	callback_on_bank_transactions = callback

callback_on_gateway_upgrade = None
def on_gateway_upgrade(callback):
	global callback_on_gateway_upgrade
	callback_on_gateway_upgrade = callback

callback_on_gateway_buy = None
def on_gateway_buy(callback):
	global callback_on_gateway_buy
	callback_on_gateway_buy = callback

callback_on_user_change_password = None
def on_user_change_password(callback):
	global callback_on_user_change_password
	callback_on_user_change_password = callback

callback_on_user_validate_password = None
def on_user_validate_password(callback):
	global callback_on_user_validate_password
	callback_on_user_validate_password = callback

callback_on_gateway_connect = None
def on_gateway_connect(callback):
	global callback_on_gateway_connect
	callback_on_gateway_connect = callback

callback_on_gateway_ping = None
def on_gateway_ping(callback):
	global callback_on_gateway_ping
	callback_on_gateway_ping = callback

callback_on_directory_list = None
def on_directory_list(callback):
	global callback_on_directory_list
	callback_on_directory_list = callback

callback_on_directory_list_remote = None
def on_directory_list_remote(callback):
	global callback_on_directory_list_remote
	callback_on_directory_list_remote = callback

callback_on_directory_create = None
def on_directory_create(callback):
	global callback_on_directory_create
	callback_on_directory_create = callback

callback_on_directory_change = None
def on_directory_change(callback):
	global callback_on_directory_change
	callback_on_directory_change = callback

callback_on_process_list = None
def on_process_list(callback):
	global callback_on_process_list
	callback_on_process_list = callback

callback_on_admin_login = None
def on_admin_login(callback):
	global callback_on_admin_login
	callback_on_admin_login = callback

callback_on_admin_crack = None
def on_admin_crack(callback):
	global callback_on_admin_crack
	callback_on_admin_crack = callback

callback_on_process_complete = None
def on_process_complete(callback):
	global callback_on_process_complete
	callback_on_process_complete = callback

callback_on_log_view = None
def on_log_view(callback):
	global callback_on_log_view
	callback_on_log_view = callback

callback_on_gateway_disconnect = None
def on_gateway_disconnect(callback):
	global callback_on_gateway_disconnect
	callback_on_gateway_disconnect = callback

callback_on_server_database_add = None
def on_server_database_add(callback):
	global callback_on_server_database_add
	callback_on_server_database_add = callback

callback_on_server_database_list = None
def on_server_database_list(callback):
	global callback_on_server_database_list
	callback_on_server_database_list = callback

callback_on_server_database_delete = None
def on_server_database_delete(callback):
	global callback_on_server_database_delete
	callback_on_server_database_delete = callback

callback_on_gateway_hostname = None
def on_gateway_hostname(callback):
	global callback_on_gateway_hostname
	callback_on_gateway_hostname = callback

callback_on_dns_lookup = None
def on_dns_lookup(callback):
	global callback_on_dns_lookup
	callback_on_dns_lookup = callback

callback_on_motd_get = None
def on_motd_get(callback):
	global callback_on_motd_get
	callback_on_motd_get = callback

callback_on_motd_set = None
def on_motd_set(callback):
	global callback_on_motd_set
	callback_on_motd_set = callback

callback_on_process_create = None
def on_process_create(callback):
	global callback_on_process_create
	callback_on_process_create = callback

callback_on_log_delete = None
def on_log_delete(callback):
	global callback_on_log_delete
	callback_on_log_delete = callback

callback_on_mail_receive = None
def on_mail_receive(callback):
	global callback_on_mail_receive
	callback_on_mail_receive = callback

callback_on_process_kill = None
def on_process_kill(callback):
	global callback_on_process_kill
	callback_on_process_kill = callback

callback_on_bulletin_board = None
def on_bulletin_board(callback):
	global callback_on_bulletin_board
	callback_on_bulletin_board = callback

callback_on_log_recover = None
def on_log_recover(callback):
	global callback_on_log_recover
	callback_on_log_recover = callback

callback_on_user_ranks = None
def on_user_ranks(callback):
	global callback_on_user_ranks
	callback_on_user_ranks = callback


callback_on_bank_loan_taken = None
def on_bank_loan_taken(callback):
	global callback_on_bank_loan_taken
	callback_on_bank_loan_taken = callback

callback_on_bank_loan_take = None
def on_bank_loan_take(callback):
	global callback_on_bank_loan_take
	callback_on_bank_loan_take = callback

callback_on_bank_loan_repay = None
def on_bank_loan_repay(callback):
	global callback_on_bank_loan_repay
	callback_on_bank_loan_repay = callback

callback_on_mission_accept = None
def on_mission_accept(callback):
	global callback_on_mission_accept
	callback_on_mission_accept = callback

callback_on_mission_list = None
def on_mission_list(callback):
	global callback_on_mission_list
	callback_on_mission_list = callback

callback_on_mission_details = None
def on_mission_details(callback):
	global callback_on_mission_details
	callback_on_mission_details = callback

callback_on_mission_complete = None
def on_mission_complete(callback):
	global callback_on_mission_complete
	callback_on_mission_complete = callback

callback_on_public_ftp = None
def on_public_ftp(callback):
	global callback_on_public_ftp
	callback_on_public_ftp = callback

callback_on_file_permissions = None
def on_file_permissions(callback):
	global callback_on_file_permissions
	callback_on_file_permissions = callback

callback_on_file_transfers = None
def on_file_transfers(callback):
	global callback_on_file_transfers
	callback_on_file_transfers = callback

callback_on_file_download = None
def on_file_download(callback):
	global callback_on_file_download
	callback_on_file_download = callback

callback_on_file_upload = None
def on_file_upload(callback):
	global callback_on_file_upload
	callback_on_file_upload = callback

callback_on_secret_question_get = None
def on_secret_question_get(callback):
	global callback_on_secret_question_get
	callback_on_secret_question_get = callback

callback_on_secret_answer_validate = None
def on_secret_answer_validate(callback):
	global callback_on_secret_answer_validate
	callback_on_secret_answer_validate = callback

callback_on_adjust_bandwidth = None
def on_adjust_bandwidth(callback):
	global callback_on_adjust_bandwidth
	callback_on_adjust_bandwidth = callback

callback_on_install = None
def on_install(callback):
	global callback_on_install
	callback_on_install = callback

callback_on_software = None
def on_software(callback):
	global callback_on_software
	callback_on_software = callback

callback_on_collect_all = None
def on_collect_all(callback):
	global callback_on_collect_all
	callback_on_collect_all = callback

callback_on_collect = None
def on_collect(callback):
	global callback_on_collect
	callback_on_collect = callback

callback_on_recover = None
def on_recover(callback):
	global callback_on_recover
	callback_on_recover = callback

callback_on_file_copy = None
def on_file_copy(callback):
	global callback_on_file_copy
	callback_on_file_copy = callback

callback_on_time = None
def on_time(callback):
	global callback_on_time
	callback_on_time = callback


callback_on_client_version = None
def on_client_version(callback):
	global callback_on_client_version
	callback_on_client_version = callback


callback_on_gateway_change_password = None
def on_gateway_change_password(callback):
	global callback_on_gateway_change_password
	callback_on_gateway_change_password = callback

callback_on_gateway_change_ip = None
def on_gateway_change_ip(callback):
	global callback_on_gateway_change_ip
	callback_on_gateway_change_ip = callback

callback_on_research = None
def on_research(callback):
	global callback_on_research
	callback_on_research = callback

callback_on_bonds_market = None
def on_bonds_market(callback):
	global callback_on_bonds_market
	callback_on_bonds_market = callback

callback_on_stock_buy = None
def on_stock_buy(callback):
	global callback_on_stock_buy
	callback_on_stock_buy = callback

callback_on_stock_sell = None
def on_stock_sell(callback):
	global callback_on_stock_sell
	callback_on_stock_sell = callback

callback_on_file_hide = None
def on_file_hide(callback):
	global callback_on_file_hide
	callback_on_file_hide = callback

callback_on_file_unhide = None
def on_file_unhide(callback):
	global callback_on_file_unhide
	callback_on_file_unhide = callback

callback_on_server_time = None
def on_server_time(callback):
	global callback_on_server_time
	callback_on_server_time = callback

callback_on_file_delete = None
def on_file_delete(callback):
	global callback_on_file_delete
	callback_on_file_delete = callback

callback_on_destroy = None
def on_destroy(callback):
	global callback_on_destroy
	callback_on_destroy = callback
	
callback_on_get_captcha = None
def on_get_captcha(callback):
	global callback_on_get_captcha
	callback_on_get_captcha = callback

########################################################################################################################################################

@sio.on('connect')
def client_on_connect():
	global sio_connected
	global sio_connect_complete
	sio_connected = True
	sio_connect_complete = True

@sio.on('disconnect')
def client_on_disconnect():
	#global callback_disconnect
	global sio_connected
	sio_connected = False
	if callback_on_disconnect is not None:
		callback_on_disconnect()

@sio.on('test')
def client_on_test(data):
	if debug_print_message_data:
		print(data)
	#print(data)
	if callback_on_test is not None:
		callback_on_test(data)

@sio.on('pong_from_server')
def client_on_pong():#data):
	#if debug_print_message_data:
	#print(data)
	#global sio_ping_enabled
	#print("received pong")
	global sio_ping_start_time
	latency = time.time() - sio_ping_start_time
	if callback_on_pong is not None:
		callback_on_pong(latency)
	if sio_ping_enabled:
		sio.sleep(1)
		ping_send()

@sio.on('server_stats')
def client_on_server_stats(data):
	if debug_print_message_data:
		print(data)
	if callback_on_server_stats is not None:
		callback_on_server_stats(data)

@sio.on('user_register')
def client_on_user_register(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_register is not None:
		callback_on_user_register(data)

@sio.on('user_login')
def client_on_user_login(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_login is not None:
		callback_on_user_login(data)

@sio.on('user_logout')
def client_on_user_logout(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_logout is not None:
		callback_on_user_logout(data)

@sio.on('user_list')
def client_on_user_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_list is not None:
		callback_on_user_list(data)

@sio.on('mail_inbox')
def client_on_mail_inbox(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mail_inbox is not None:
		callback_on_mail_inbox(data)

@sio.on('mail_read')
def client_on_mail_read(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mail_read is not None:
		callback_on_mail_read(data)

@sio.on('mail_delete')
def client_on_mail_delete(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mail_delete is not None:
		callback_on_mail_delete(data)

@sio.on('mail_send')
def client_on_mail_send(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mail_send is not None:
		callback_on_mail_send(data)

@sio.on('gateway_list')
def client_on_gateway_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_list is not None:
		callback_on_gateway_list(data)

@sio.on('admin_connection_list')
def client_on_admin_connection_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_admin_connection_list is not None:
		callback_on_admin_connection_list(data)

@sio.on('admin_sql_query')
def client_on_admin_sql_query(data):
	if debug_print_message_data:
		print(data)
	if callback_on_admin_sql_query is not None:
		callback_on_admin_sql_query(data)

@sio.on('gateway_select')
def client_on_gateway_select(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_select is not None:
		callback_on_gateway_select(data)

@sio.on('bank_balance')
def client_on_bank_balance(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bank_balance is not None:
		callback_on_bank_balance(data)

@sio.on('bank_transfer')
def client_on_bank_transfer(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bank_transfer is not None:
		callback_on_bank_transfer(data)

@sio.on('bank_transactions')
def client_on_bank_transactions(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bank_transactions is not None:
		callback_on_bank_transactions(data)

@sio.on('gateway_upgrade')
def client_on_gateway_upgrade(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_upgrade is not None:
		callback_on_gateway_upgrade(data)

@sio.on('gateway_buy')
def client_on_gateway_buy(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_buy is not None:
		callback_on_gateway_buy(data)

@sio.on('user_change_password')
def client_on_user_change_password(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_change_password is not None:
		callback_on_user_change_password(data)

@sio.on('user_validate_password')
def client_on_user_validate_password(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_validate_password is not None:
		callback_on_user_validate_password(data)

@sio.on('gateway_connect')
def client_on_gateway_connect(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_connect is not None:
		callback_on_gateway_connect(data)

@sio.on('gateway_ping')
def client_on_gateway_ping(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_ping is not None:
		callback_on_gateway_ping(data)

@sio.on('directory_list')
def client_on_directory_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_directory_list is not None:
		callback_on_directory_list(data)

@sio.on('directory_list_remote')
def client_on_directory_list_remote(data):
	if debug_print_message_data:
		print(data)
	if callback_on_directory_list_remote is not None:
		callback_on_directory_list_remote(data)

@sio.on('directory_create')
def client_on_directory_create(data):
	if debug_print_message_data:
		print(data)
	if callback_on_directory_create is not None:
		callback_on_directory_create(data)

@sio.on('directory_change')
def client_on_directory_change(data):
	if debug_print_message_data:
		print(data)
	if callback_on_directory_change is not None:
		callback_on_directory_change(data)

@sio.on('process_list')
def client_on_process_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_process_list is not None:
		callback_on_process_list(data)

@sio.on('admin_login')
def client_on_admin_login(data):
	if debug_print_message_data:
		print(data)
	if callback_on_admin_login is not None:
		callback_on_admin_login(data)

@sio.on('admin_crack')
def client_on_admin_crack(data):
	if debug_print_message_data:
		print(data)
	if callback_on_admin_crack is not None:
		callback_on_admin_crack(data)

@sio.on('process_complete')
def client_on_process_complete(data):
	if debug_print_message_data:
		print(data)
	if callback_on_process_complete is not None:
		callback_on_process_complete(data)

@sio.on('log_view')
def client_on_log_view(data):
	if debug_print_message_data:
		print(data)
	if callback_on_log_view is not None:
		callback_on_log_view(data)

@sio.on('gateway_disconnect')
def client_on_gateway_disconnect(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_disconnect is not None:
		callback_on_gateway_disconnect(data)

@sio.on('server_database_add')
def client_on_server_database_add(data):
	if debug_print_message_data:
		print(data)
	if callback_on_server_database_add is not None:
		callback_on_server_database_add(data)

@sio.on('server_database_list')
def client_on_server_database_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_server_database_list is not None:
		callback_on_server_database_list(data)
		
@sio.on('server_database_delete')
def client_on_server_database_delete(data):
	if debug_print_message_data:
		print(data)
	if callback_on_server_database_delete is not None:
		callback_on_server_database_delete(data)
		
@sio.on('gateway_hostname')
def client_on_gateway_hostname(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_hostname is not None:
		callback_on_gateway_hostname(data)
		
@sio.on('dns_lookup')
def client_on_dns_lookup(data):
	if debug_print_message_data:
		print(data)
	if callback_on_dns_lookup is not None:
		callback_on_dns_lookup(data)

@sio.on('motd_get')
def client_on_motd_get(data):
	if debug_print_message_data:
		print(data)
	if callback_on_motd_get is not None:
		callback_on_motd_get(data)

@sio.on('motd_set')
def client_on_motd_set(data):
	if debug_print_message_data:
		print(data)
	if callback_on_motd_set is not None:
		callback_on_motd_set(data)

@sio.on('process_create')
def client_on_process_create(data):
	if debug_print_message_data:
		print(data)
	if callback_on_process_create is not None:
		callback_on_process_create(data)

@sio.on('log_delete')
def client_on_log_delete(data):
	if debug_print_message_data:
		print(data)
	if callback_on_log_delete is not None:
		callback_on_log_delete(data)

@sio.on('mail_receive')
def client_on_mail_receieve(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mail_receive is not None:
		callback_on_mail_receive(data)

@sio.on('process_kill')
def client_on_process_kill(data):
	if debug_print_message_data:
		print(data)
	if callback_on_process_kill is not None:
		callback_on_process_kill(data)

@sio.on('bulletin_board')
def client_on_bulletin_board(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bulletin_board is not None:
		callback_on_bulletin_board(data)

@sio.on('log_recover')
def client_on_log_recover(data):
	if debug_print_message_data:
		print(data)
	if callback_on_log_recover is not None:
		callback_on_log_recover(data)

@sio.on('user_ranks')
def client_on_user_ranks(data):
	if debug_print_message_data:
		print(data)
	if callback_on_user_ranks is not None:
		callback_on_user_ranks(data)

@sio.on('bank_loan_taken')
def client_on_bank_loan_taken(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bank_loan_taken is not None:
		callback_on_bank_loan_taken(data)

@sio.on('bank_loan_take')
def client_on_bank_loan_take(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bank_loan_take is not None:
		callback_on_bank_loan_take(data)

@sio.on('bank_loan_repay')
def client_on_bank_loan_repay(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bank_loan_repay is not None:
		callback_on_bank_loan_repay(data)

@sio.on('mission_accept')
def client_on_mission_accept(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mission_accept is not None:
		callback_on_mission_accept(data)

@sio.on('mission_list')
def client_on_mission_list(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mission_list is not None:
		callback_on_mission_list(data)

@sio.on('mission_details')
def client_on_mission_details(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mission_details is not None:
		callback_on_mission_details(data)

@sio.on('mission_complete')
def client_on_mission_complete(data):
	if debug_print_message_data:
		print(data)
	if callback_on_mission_complete is not None:
		callback_on_mission_complete(data)

@sio.on('public_ftp')
def client_on_public_ftp(data):
	if debug_print_message_data:
		print(data)
	if callback_on_public_ftp is not None:
		callback_on_public_ftp(data)

@sio.on('file_permissions')
def client_on_file_permissions(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_permissions is not None:
		callback_on_file_permissions(data)

@sio.on('file_transfers')
def client_on_file_transfers(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_transfers is not None:
		callback_on_file_transfers(data)

@sio.on('file_download')
def client_on_file_download(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_download is not None:
		callback_on_file_download(data)

@sio.on('file_upload')
def client_on_file_upload(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_upload is not None:
		callback_on_file_upload(data)

@sio.on('secret_question_get')
def client_on_secret_question_get(data):
	if debug_print_message_data:
		print(data)
	if callback_on_secret_question_get is not None:
		callback_on_secret_question_get(data)

@sio.on('secret_answer_validate')
def client_on_secret_answer_validate(data):
	if debug_print_message_data:
		print(data)
	if callback_on_secret_answer_validate is not None:
		callback_on_secret_answer_validate(data)

@sio.on('adjust_bandwidth')
def client_on_adjust_bandwidth(data):
	if debug_print_message_data:
		print(data)
	if callback_on_adjust_bandwidth is not None:
		callback_on_adjust_bandwidth(data)


@sio.on('install')
def client_on_install(data):
	if debug_print_message_data:
		print(data)
	if callback_on_install is not None:
		callback_on_install(data)



@sio.on('software')
def client_on_software(data):
	if debug_print_message_data:
		print(data)
	if callback_on_software is not None:
		callback_on_software(data)




@sio.on('collect_all')
def client_on_collect_all(data):
	if debug_print_message_data:
		print(data)
	if callback_on_collect_all is not None:
		callback_on_collect_all(data)

@sio.on('collect')
def client_on_collect(data):
	if debug_print_message_data:
		print(data)
	if callback_on_collect is not None:
		callback_on_collect(data)



@sio.on('recover')
def client_on_recover(data):
	if debug_print_message_data:
		print(data)
	if callback_on_recover is not None:
		callback_on_recover(data)


@sio.on('file_copy')
def client_on_file_copy(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_copy is not None:
		callback_on_file_copy(data)



@sio.on('time')
def client_on_time(data):
	if debug_print_message_data:
		print(data)
	if callback_on_time is not None:
		callback_on_time(data)

recommended_client_version = None

@sio.on('client_version')
def client_on_client_version(data):
	global recommended_client_version
	recommended_client_version = data['version']
	if callback_on_client_version is not None:
		callback_on_client_version(data)



@sio.on('gateway_change_password')
def client_on_gateway_change_password(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_change_password is not None:
		callback_on_gateway_change_password(data)


@sio.on('gateway_change_ip')
def client_on_gateway_change_ip(data):
	if debug_print_message_data:
		print(data)
	if callback_on_gateway_change_ip is not None:
		callback_on_gateway_change_ip(data)


@sio.on('research')
def client_on_research(data):
	if debug_print_message_data:
		print(data)
	if callback_on_research is not None:
		callback_on_research(data)

@sio.on('bonds_market')
def client_on_bonds_market(data):
	if debug_print_message_data:
		print(data)
	if callback_on_bonds_market is not None:
		callback_on_bonds_market(data)

@sio.on('stock_buy')
def client_on_stock_buy(data):
	if debug_print_message_data:
		print(data)
	if callback_on_stock_buy is not None:
		callback_on_stock_buy(data)

@sio.on('stock_sell')
def client_on_stock_sell(data):
	if debug_print_message_data:
		print(data)
	if callback_on_stock_sell is not None:
		callback_on_stock_sell(data)

@sio.on('file_hide')
def client_on_file_hide(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_hide is not None:
		callback_on_file_hide(data)

@sio.on('file_unhide')
def client_on_file_unhide(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_unhide is not None:
		callback_on_file_unhide(data)

@sio.on('server_time')
def client_on_server_time(data):
	if debug_print_message_data:
		print(data)
	if callback_on_server_time is not None:
		callback_on_server_time(data)

@sio.on('file_delete')
def client_on_file_delete(data):
	if debug_print_message_data:
		print(data)
	if callback_on_file_delete is not None:
		callback_on_file_delete(data)

@sio.on('destroy')
def client_on_destroy(data):
	if debug_print_message_data:
		print(data)
	if callback_on_destroy is not None:
		callback_on_destroy(data)

@sio.on('get_captcha')
def client_on_get_captcha(data):
	if debug_print_message_data:
		print(data)
	if callback_on_get_captcha is not None:
		callback_on_get_captcha(data)
