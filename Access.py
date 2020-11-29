import requests, json
import subprocess
import sys
access_token = '1a23bd36a62a85df3fd3188c76c5591ab8ff7125'
my_headers = {'Authorization' : '{access_token}'}


response = requests.get('https://api.github.com/users/dgreen8443/repos')

y = response.json()
#x = json.loads(y)
for i in y:
	print(json.dumps(i, indent = 4))
	print(i["full_name"])

#print(json.dumps(x, indent = 4))

response = requests.get('https://api.github.com/repos/dgreen8443/SWENG-Group-9/languages', headers = my_headers)
y = response.json()
print(json.dumps(y, indent = 4))
