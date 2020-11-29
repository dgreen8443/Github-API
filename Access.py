import requests, json
import subprocess
import sys
access_token = 'd4671af90b713d32019f549dfcf447d1a80465f3'
my_headers = {'dgreen8443' : '{access_token}'}
user_list = []
repo_list = []
def get_users(user):
	url = 'https://api.github.com/users/' + user + '/following'
	response = requests.get(url,auth=('dgreen8443','d4671af90b713d32019f549dfcf447d1a80465f3'))#headers = my_headers)
	print(response)
	for i in response.json():
		user_list.append(i["login"])
	
def find_repos(user):
	url = 'https://api.github.com/users/' + user + '/repos'
	response = requests.get(url,auth=('dgreen8443','d4671af90b713d32019f549dfcf447d1a80465f3'))#headers = my_headers)
	print(response)
	for i in response.json():
		repo_list.append(i["full_name"])
		res = get_language(i["full_name"])
		for i in res:
			print(i)


def get_language(repo):
	url = 'https://api.github.com/repos/' + repo + '/languages'

	response = requests.get(url,auth=('dgreen8443','d4671af90b713d32019f549dfcf447d1a80465f3'))#headers = my_headers)
	#print(response.json())
	return response
	

get_users('dgreen8443')
print(user_list)
for i in user_list:
	find_repos(i)
print(repo_list)
for i in repo_list:
	get_language(i)
#y = response.json()

#x = json.loads(y)
#for i in y:
	#print(json.dumps(i, indent = 4))
#	print(i["login"])
	

#print(json.dumps(y, indent = 4))

response = requests.get('https://api.github.com/repos/dgreen8443/SWENG-Group-9/languages',auth=('dgreen8443','d4671af90b713d32019f549dfcf447d1a80465f3'))#headers = my_headers)
y = response.json()
print(json.dumps(y, indent = 4))
