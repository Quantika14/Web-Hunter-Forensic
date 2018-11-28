#!/usr/bin/python
# encoding: utf-8

#AUTHOR: JORGE CORONADO
#TWITTER: @JORGEWEBSEC
#CONTACT: JORGEWEBSEC[@]GMAIL.COM

import os, MySQLdb, hashlib, subprocess
#CONSTANTS

#The directory where it's going to be cloned
#dir_output = "/home/vm/Escritorio/clonado/"

file_auth_log = "/var/log/auth.log"

file_access_log = "/opt/lampp/logs/access_log"

#MySQL data

table_name = "wp_posts"

column_name = "post_date"

#MySQL Connections data
db_HOST = "127.0.0.1" #Localhost
db_USER = "root"
db_PASS = ""
db_NAME = "wppruebas"

DANGEROUS_WORDS_AUTH = ("/usr/bin/apt-get install", "root")
RISK_WORDS_AUTH = ("COMMAND")

DANGEROUS_WORDS_ACCESS = ("wp-admin", "login", "admin", "'", "--", "%")


#Locate logs
auth_array_root = []
access_array_root = []

class color:
	header = '\033[95m'
	blue = '\033[94m'
	green = '\033[92m'
	alert = '\033[93m'
	fail = '\033[91m'
	normal = '\033[0m'
	bold = '\033[1m'
	underline = '\033[4m'

# -
# CLONE AND LOCATE LOGS FUNCTIONS
# -

def var_log_cloned(locate=0):
	global auth_array_root, access_array_root
	
	if locate == 0:
		print "[INFO] Cloning the file: " + file_auth_log
		os.system("dd if=" + file_auth_log + " of=auth.log bs=1")
		hash_auth = SHA256_Checksum("auth.log")
		print "[HASH][SHA256][>] " + hash_auth
		
		print "[INFO] Cloning the file: " + file_access_log
		os.system("dd if=" + file_access_log + " of=access.log bs=1")
		hash_access = SHA256_Checksum("access.log")
		print "[HASH][SHA256][>] " + hash_access
	else:
		print "[INFO] Locate logs..."
		auth_array = os.popen("locate 'auth.log'").read()
		access_array = os.popen("locate 'access.log'").read()

		f = open("locate_logs.txt", "a")

		auth_array_root = auth_array.split("\n")
		for auth in auth_array_root:
			if not auth == '':
				try:
					name_split = auth.split("/")
					l = len(name_split)
					file_name = name_split[l-1]
					f.write(auth + "|||" + file_name + "\n")
					print "[INFO] Cloning the file: " + auth
					os.system("dd if=" + auth + " of=" + file_name + " bs=1")
					hash_auth = SHA256_Checksum(file_name)
					print "[HASH][SHA256][>] " + hash_auth
				except:
					print "[WARNING] File " + str(auth) + "not found..."
				
		access_array_root = access_array.split("\n")
		for access in access_array_root:
			if not access == '':
				try:
					f.write(access+"\n")
					name_split = access.split("/")
					l = len(name_split)
					file_name = name_split[l-1]
					f.write(access + "|||" + file_name + "\n")
					print "[INFO] Cloning the file: " + auth
					os.system("dd if=" + access + " of=" + file_name + " bs=1")
					hash_auth = SHA256_Checksum(file_name)
					print "[HASH][SHA256][>] " + hash_auth
				except:
					print "[WARNING] File " + str(access) + "not found..."

		f.close()
	
def SHA256_Checksum(ruta):
	h = hashlib.sha256()
	with open(ruta, 'rb', buffering=0) as f:
		for b in iter(lambda : f.read(128*1024), b''):
			h.update(b)
	return h.hexdigest()

# -
# FIND FUNCTIONS
# -

def find_in_MySQL(find_date):
	print "*****************************************************************"
	print "*** STARTING TO FIND IN MYSQL                                 ***"
	print "*****************************************************************"
	global db_HOST, db_USER, db_PASS, db_NAME
	try:
		db = MySQLdb.connect(host=db_HOST,    # change for your data
				user=db_USER,         # username
				passwd=db_PASS,  # password
				db=db_NAME)        # Data Base Name

		cur = db.cursor()
		query = "SELECT * FROM `" + table_name + "` WHERE `" + column_name + "` LIKE " + "'%" + find_date + "%'"
		cur.execute(query)

		for row in cur.fetchall():
			print "[USERID][>] " + str(row[1]) + " | [POST_TITLE][>] " + row[5] + " | [POST_ID][>] " + str(row[0]) + " | [POST_DATE][>] " + str(row[2]) + " | [POST_MODIFIED][>] " + str(row[15])
		return True

	except:
		print "[!][ERROR][>] it's not possible to connect to the MYSQL database..."
		print "[!][ERROR][>] you must try changing the connection data and start the database service."
		return False

def find_in_Access(find_date_access):
	global access_array_root
	print "*****************************************************************"
	print "*** STARTING TO FIND IN ACCESS.LOG                            ***"
	print "*****************************************************************"
	
	sizefile = os.stat("locate_logs.txt").st_size
	count_access = 0

	if sizefile > 10:
		file_locate = open("locate_logs.txt", "r")
		for line in file_locate.readlines():
			if "access" in line:
				access_file = line.split("|||")
				access = access_file[1].replace("\n","")
				f = open(access, "r")
				for line in f.readlines():
					if find_date_access in line:
						print_data(str(access_file[1]), line)
				f.close()
				count_access += 1
		file_locate.close()
		print "[WARNING] File access.log not found..."

	else:
		try:
			f = open("access.log", "r")
			for line in f.readlines():
				if find_date_access in line:
					print_data("access.log", line)
			f.close()
		except:
			print "[WARNING] File access.log not found...'"

def find_in_auth(find_date_auth):
	global auth_array_root
	print "*****************************************************************"
	print "*** STARTING TO FIND IN AUTH.LOG                              ***"
	print "*****************************************************************"
	
	sizefile = os.stat("locate_logs.txt").st_size

	if sizefile > 10:

		file_locate = open("locate_logs.txt", "r")
		for line in file_locate.readlines():
			if "auth" in line:
				auth_file = line.split("|||")
				if not auth_file[1] == '':
					auth = auth_file[1].replace("\n", "")
					f = open(auth, "r")
					for line in f.readlines():
						if find_date_auth in line:
							print_data(str(auth_file[1]), str(line))
					f.close()
		file_locate.close()

	else:
		f = open("auth.log", "r")
		for line in f.readlines():
			if find_date_auth in line:
				print_data("auth.log", str(line))
		f.close()
# -
# PRINT DATA FUNCTION
# -

def print_data(log, data):
	if "access" in log:
		for word in DANGEROUS_WORDS_ACCESS:
			if word in data:
				print color.alert + "[FILE][ " + str(log).replace("\n", "") + "][>] " + str(data) + color.normal
			else:
				print "[FILE][ " + str(log).replace("\n", "") + "][>] " + str(data)

	if "auth" in log:
		for word in DANGEROUS_WORDS_AUTH:
			if word in data:
				print color.alert + "[FILE][ " + str(log).replace("\n", "") + "][>] " + str(data) + color.normal
			else:
				print "[FILE][ " + str(log).replace("\n","") + "][>] " + str(data)
	else:
		print "[ERROR][>] Not found log..."

# -
# MENU FUNCTION
# -

def menu():
	print """
	 █     █░▓█████  ▄▄▄▄       ██░ ██  █    ██  ███▄    █ ▄▄▄█████▓▓█████  ██▀███       █████▒▒█████   ██▀███  ▓█████  ███▄    █   ██████  ██▓ ▄████▄  
	▓█░ █ ░█░▓█   ▀ ▓█████▄    ▓██░ ██▒ ██  ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒   ▓██   ▒▒██▒  ██▒▓██ ▒ ██▒▓█   ▀  ██ ▀█   █ ▒██    ▒ ▓██▒▒██▀ ▀█  
	▒█░ █ ░█ ▒███   ▒██▒ ▄██   ▒██▀▀██░▓██  ▒██░▓██  ▀█ ██▒▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒   ▒████ ░▒██░  ██▒▓██ ░▄█ ▒▒███   ▓██  ▀█ ██▒░ ▓██▄   ▒██▒▒▓█    ▄ 
	░█░ █ ░█ ▒▓█  ▄ ▒██░█▀     ░▓█ ░██ ▓▓█  ░██░▓██▒  ▐▌██▒░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄     ░▓█▒  ░▒██   ██░▒██▀▀█▄  ▒▓█  ▄ ▓██▒  ▐▌██▒  ▒   ██▒░██░▒▓▓▄ ▄██▒
	░░██▒██▓ ░▒████▒░▓█  ▀█▓   ░▓█▒░██▓▒▒█████▓ ▒██░   ▓██░  ▒██▒ ░ ░▒████▒░██▓ ▒██▒   ░▒█░   ░ ████▓▒░░██▓ ▒██▒░▒████▒▒██░   ▓██░▒██████▒▒░██░▒ ▓███▀ ░
	░ ▓░▒ ▒  ░░ ▒░ ░░▒▓███▀▒    ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒   ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░    ▒ ░   ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░░ ▒░ ░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░▓  ░ ░▒ ▒  ░
	  ▒ ░ ░   ░ ░  ░▒░▒   ░     ▒ ░▒░ ░░░▒░ ░ ░ ░ ░░   ░ ▒░    ░     ░ ░  ░  ░▒ ░ ▒░    ░       ░ ▒ ▒░   ░▒ ░ ▒░ ░ ░  ░░ ░░   ░ ▒░░ ░▒  ░ ░ ▒ ░  ░  ▒   
	  ░   ░     ░    ░    ░     ░  ░░ ░ ░░░ ░ ░    ░   ░ ░   ░         ░     ░░   ░     ░ ░   ░ ░ ░ ▒    ░░   ░    ░      ░   ░ ░ ░  ░  ░   ▒ ░░        
	    ░       ░  ░ ░          ░  ░  ░   ░              ░             ░  ░   ░                   ░ ░     ░        ░  ░         ░       ░   ░  ░ ░      
	                      ░                                                                                                                    ░        
			AUTHOR: JORGE CORONADO | TWITTER: @JORGEWEBSEC | WEB: BLOG.QUANTIKA14.COM | VERSION: 1.0 | DATE: 29/08/2018
	"""
	
	while 1:
		print ""
		print "--------------------------------------------------------------------------------------------------------------------------------------------"
		print "1. Clone logs by default"
		print "2. Locate logs & clone"
		print "3. Find clues"
		print "4. Exit"
		x = int(raw_input("Select [1/2/3]: "))
		if x == 1:
			var_log_cloned()
		if x == 2:
			var_log_cloned(locate=1)
		if x == 3:
			find_date_WP = str(raw_input("[MYSQL] Insert date (AAAA-MM-DD)[GMT]: "))
			find_date_access = str(raw_input("[ACCESS.LOG] Insert date (YEAR/MONTH/DAY)(ej: 28/Aug/2018): )"))
			find_date_auth = str(raw_input("[AUTH.LOG] Insert date (DD MONTH)(ej: 28 Aug): "))
			fWP = find_in_MySQL(find_date_WP)
			
			if fWP == False:
				z = str(raw_input("Do you want to continue? [S/n]: "))
				if z == "s" or z == "S":
					try:
						find_in_Access(find_date_access)
					except: print "[WARNING][>] Error in find_ind_access"
					#try:
					find_in_auth(find_date_auth)
					#except Exception as e: print "[WARNING][>] Error in find_in_auth: " + str(e)
				else:
					menu()
			else:
				try:
					find_in_Access(find_date_access)
				except: print "[WARNING][>] Error in find_ind_access"
				try:
					find_in_auth(find_date_auth)
				except: print "[WARNING][>] Error in find_in_auth"
		if x == 4:
			print "Chau! ;-p"
			break
			
menu()
