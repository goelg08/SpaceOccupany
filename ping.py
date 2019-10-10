import json
import subprocess
import os
import sys
import platform
import socket
import pypyodbc

def parsejson(d):
	for k, v in d.items():
		if isinstance(v, dict):
			parsejson(v)		
		else:
			if isinstance(v, list):
				parselist(v)
			else:
				print("{0} : {1}".format(k, v))	
			
def parselist(d):
	for l in d:
		if isinstance(l, dict):
			parsejson(l)
		else:
			pingtest(l)

#def pingtest(l):
#	for n in range(1, 2):
#		ip=(l+"{0}").format(n)
#		result=subprocess.call(["ping", "-c", "1", ip])
#		#print(result)
#		if result == 0:
#			print(ip, "active")
#		else:
#			print(ip, "inactive")
			
def pingtest(l):
	for n in range(1, 2):
		ip=(l+"{0}").format(n)
		print(platform.system())
		if platform.system() == "linux" or platform.system() == "darwin":
			command=["ping", "-c", "3", "-i", "0.2", ip]
			timeout=0.5
		else:
			command=["ping", "-n", "1", ip]
			timeout=0.2
		ping=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		try:             
			[out, err]=ping.communicate(timeout=2.1)
			if ping.returncode == 0:
				if platform.system() == "linux" or platform.system() == "darwin":
					print("Linux"+" Active")
				else:
					print("Windows"+" Active")
					get_Host_name_IP(ip)
		except subprocess.TimeoutExpired:
			ping.kill()
		#finally:
		#	get_Host_name_IP(ip)
			
def get_Host_name_IP(ip):
	try: 
		print(ip)
		host_name = socket.getfqdn(ip)
		print("Hostname :  ",host_name)
	except: 
		print("Unable to get Hostname by IP") 
	finally:
		populate_DB(ip,host_name)
		
def populate_DB(ip,host_name):
	try:
		status = "Active"
		conn = pypyodbc.connect('Driver={SQL Server};'
								'Server=localhost;'
								'Database=DemoDB;'
								'Trusted_Connection=yes')
		cursor = conn.cursor()
		SQLCommand = ("INSERT INTO DemoDB.dbo.pinginfo(IPAddr, HostName, Status) VALUES(?,?,?)")
		Values = [ip,host_name,status]
		cursor.execute(SQLCommand,Values)	
		conn.commit()
		print("Data inserted")
		conn.close()
	except Exception as e: 
		print(sys.exc_value)
		catchEverything()
			

f = open('properties.json')
data = json.load(f)
print(data)
f.close()


parsejson(data)

