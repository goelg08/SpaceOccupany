import json
import subprocess
import os
import sys
import platform

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
		print(platform)
		if platform == "linux" or platform == "darwin":
			command=["ping", "-c", "3", "-i", "0.2", ip]
			timeout=0.5
		else:
			command=["ping", "-n", "1", ip]
			timeout=0.2
		ping=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		try:             
			[out, err]=ping.communicate(timeout=2.1)
			if ping.returncode == 0:
				if platform == "linux" or platform == "darwin":
					print("Linux"+" Active")
				else:
					print("Windows"+" Active")
		except subprocess.TimeoutExpired:
			ping.kill()
		finally:
			print(ip)
			

f = open('properties.json')
data = json.load(f)
print(data)
f.close()

parsejson(data)
