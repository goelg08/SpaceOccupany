import concurrent.futures
import time
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
			buildiplist(l)
			
def buildiplist(l):
	for n in range(1, 10):
		ip=(l+"{0}").format(n)
		ips.append(ip)
			
			
def pingtest(ip):
	print(ip)
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
				return "Linux Active"
			else:
				host_name = socket.getfqdn(ip)
				print("Hostname :  ",host_name)
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
				return "Data inserted"
				conn.close()				
	except subprocess.TimeoutExpired:
		ping.kill()
	except Exception as e: 
		print(sys.exc_value)
		catchEverything()
	except: 
		host_name = "NA"

			
start = time.perf_counter()

f = open('properties.json')
data = json.load(f)
print(data)
f.close()

#parsejson(data)

ips = []
parsejson(data)
print(ips)


with concurrent.futures.ThreadPoolExecutor() as executor:
	secs = ips
	results = executor.map(pingtest, secs)
	
for result in results:
		print(result)
		
finish = time.perf_counter()


print(f'Finished in {round(finish-start, 2)} second(s)')

