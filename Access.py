import requests
import json
import subprocess
import sys
import operator

with  open('./authkey.txt', 'r') as reader:
	access_token = reader.read()
with open('./user.txt', 'r') as reader:
	username = reader.read()
reader.close()
my_headers = {'{username}' : '{access_token}'}
user_list = []
repo_list = []


def get_users(user):
	url = 'https://api.github.com/users/' + user + '/following'
	response = requests.get(url,auth=(username, access_token))#headers = my_headers)
	
	for i in response.json():
		user_list.append(i["login"])
	

	## goes through a user's list of public repos and finds the language that has the most lines of code in it
def find_repos(user): 
	url = 'https://api.github.com/users/' + user + '/repos'
	response = requests.get(url,auth=(username, access_token))#headers = my_headers)
	
	user_lang = []
	for i in response.json():
		repo_list.append(i["full_name"])
		res = get_language(i["full_name"])
		user_lang.append(res)
	for i in user_lang:
		if i == {'blank' : 0}:
			user_lang.remove(i)
	print(user_lang)
	user_fav = {}
	for dict in user_lang:
		for key,value in dict.items():
			if user_fav.has_key(key):
				user_fav[key] = user_fav[key] + value
			else:	
				user_fav[key] = value
	print (user_fav)
	user_favourite_language = max(user_fav.iteritems(), key = operator.itemgetter(1))[0]
	print(user_favourite_language)



## takes a user's dictionary and returns a dictionary of the largest language in the repo and the assosiated #lines of code
def get_language(repo):
	url = 'https://api.github.com/repos/' + repo + '/languages'
	repo_lang = []
	repo_dict = {}
	response = requests.get(url,auth=(username, access_token ))#headers = my_headers)
	y = response.json()
	for i in y:
		repo_lang.append(i)
	i = 0
	while i < len(repo_lang):
		repo_dict[repo_lang[i]] = y[repo_lang[i]]
		i = i+1
	
	max_lang = {"blank": 0}

	#only take the language with most lines of code
	for i in repo_dict:
		for j in max_lang:
			if(max_lang[j] < repo_dict[i]):
				max_lang.clear()
				max_lang[i] = repo_dict[i]
	#print(max_lang)
	
	return max_lang
	

get_users('dgreen8443')
print(user_list)
for i in user_list:
	find_repos(i)
#print(repo_list)



