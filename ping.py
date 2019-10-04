import json
import subprocess
import os

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

def pingtest(l):
	for n in range(1, 10):
		ip=(l+"{0}").format(n)
		result=subprocess.call(["ping", "-c", "1", ip])
		print(result)
		if result == 0:
			print(ip, "active")
		else:
			print(ip, "inactive")

			
f = open('properties.json')
data = json.load(f)
print(data)
f.close()

parsejson(data)
