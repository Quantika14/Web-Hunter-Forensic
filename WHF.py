#!/usr/bin/python
# encoding: utf-8

import os, MySQLdb, hashlib, subprocess
#CONSTANTES

#The directory where it's going to be cloned
#dir_output = "/home/vm/Escritorio/clonado/"

file_auth_log = "/var/log/auth.log"

file_access_log = "/opt/lampp/logs/access_log"

#MySQL data

table_name = "wp_posts"

column_name = "post_date"

#Locate logs
auth_array_root = []
access_array_root = []

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
		
		auth_array_root = auth_array.split("\n")
		for auth in auth_array_root:
			if not auth == '':
				name_split = auth.split("/")
				l = len(name_split)
				file_name = name_split[l-1]
				print "[INFO] Cloning the file: " + auth
				os.system("dd if=" + auth + " of=" + file_name + " bs=1")
				hash_auth = SHA256_Checksum(file_name)
				print "[HASH][SHA256][>] " + hash_auth
				
		access_array_root = access_array.split("\n")
		for access in access_array_root:
			if not access == '':
				name_split = access.split("/")
				l = len(name_split)
				file_name = name_split[l-1]
				print "[INFO] Cloning the file: " + auth
				os.system("dd if=" + access + " of=" + file_name + " bs=1")
				hash_auth = SHA256_Checksum(file_name)
				print "[HASH][SHA256][>] " + hash_auth
	
	
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
	db = MySQLdb.connect(host="127.0.0.1",    # change for your data
			user="root",         # username
			passwd="",  # password
			db="wppruebas")        # Data Base Name

	cur = db.cursor()
	query = "SELECT * FROM `" + table_name + "` WHERE `" + column_name + "` LIKE " + "'%" + find_date + "%'"
	cur.execute(query)

	for row in cur.fetchall():
	    print "[USERID][>] " + str(row[1]) + " | [POST_TITLE][>] " + row[5] + " | [POST_ID][>] " + str(row[0]) + " | [POST_DATE][>] " + str(row[2]) + " | [POST_MODIFIED][>] " + str(row[15])

def find_in_Access(find_date_access):
	global access_array_root
	print "*****************************************************************"
	print "*** STARTING TO FIND IN ACCESS.LOG                            ***"
	print "*****************************************************************"
	
	if len(access_array_root) > 1:
		for access in access_array_root:
			if not access == '':
				f = open(access, "r")
				for line in f.readlines():
					if find_date_access in line:
						print "[FILE][ " + str(access) + "][>] " + str(line)
				f.close()

	else:
		f = open("access.log", "r")
		for line in f.readlines():
			if find_date_access in line:
				print "[FILE][ACCESS.LOG][>] " + str(line)
		f.close()

def find_in_auth(find_date_auth):
	global auth_array_root
	print "*****************************************************************"
	print "*** STARTING TO FIND IN AUTH.LOG                              ***"
	print "*****************************************************************"
	
	if len(auth_array_root) > 1:
		for auth in auth_array_root:
			if not auth == '':
				f = open(auth, "r")
				for line in f.readlines():
					if find_date_auth in line:
						print "[FILE][ " + str(auth) + "][>] " + str(line)
				f.close()
	else:
		f = open("auth.log", "r")
		for line in f.readlines():
			if find_date_auth in line:
				print "[FILE][AUTH.LOG][>] " + str(line)
		f.close()

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
			find_date_WP = str(raw_input("Insert date (AAAA-MM-DD)[GMT]: "))
			find_date_access = str(raw_input("Insert date (YEAR/MONTH/DAY)(ej: 28/Aug/2018): )"))
			find_date_auth = str(raw_input("Insert date (DD MONTH)(ej: 28 Aug): "))
			find_in_MySQL(find_date_WP)
			find_in_Access(find_date_access)
			find_date_auth(find_date_auth)
		if x == 4:
			print "Chau! ;-p"
			break
			
menu()
