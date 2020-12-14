import requests
import json
import subprocess
import sys
import operator
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as pl
mp.use("TkAgg")

if len(sys.argv) < 2:
	with  open('./authkey.txt', 'r') as reader:
		access_token = reader.read()
	with open('./user.txt', 'r') as reader:
		username = reader.read()
	target = 'dgreen8443'

else: 
	access_token = sys.argv[3]
	username = sys.argv[2]
	target = sys.argv[1]

#reader.close()
my_headers = {'{username}' : '{access_token}'}
user_list = []
repo_list = []
language_count = {}



def get_users(user):
	url = 'https://api.github.com/users/' + user + '/followers'
	response = requests.get(url,auth=(username, access_token))#headers = my_headers)
	for i in response.json():
		user_list.append(i["login"])
	
def maxLanguages(dictionary):
	max_key = max(dictionary, key=dictionary.get)
	return max_key


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
		if i == {'' : 0}:
			user_lang.remove(i)
	
	user_fav = {}
	for dictionary in user_lang:
		for key,value in dictionary.items():
			if key in user_fav:
				user_fav[key] = user_fav[key] + value
			else:	
				user_fav[key] = value
	
	if user_fav != {}:
		user_favourite_language = maxLanguages(user_fav)	
	else: 
		user_favourite_language = 'Nothing'
	#print(user_favourite_language)
	return user_favourite_language




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
	
	max_lang = {'': 0}

	#only take the language with most lines of code
	for i in repo_dict:
		for j in max_lang:
			if(max_lang[j] < repo_dict[i]):
				max_lang.clear()
				max_lang[i] = repo_dict[i]
	#print(max_lang)
	
	return max_lang
	
target_fav = find_repos(target)
print(target_fav)
get_users(target)
print(user_list)
for i in user_list:
	returned_language = find_repos(i)
	if returned_language == '':
		returned_language = 'Nothing'
	if returned_language in language_count:
		language_count[returned_language] = language_count[returned_language] + 1
	else: 
		language_count[returned_language] = 1
language_list = []
language_value = []
print(language_count)
for i in language_count:
	language_list.append(i)
	language_value.append(language_count[i])

fig = pl.figure
pl.plot(language_list, language_value)
pl.savefig('./test1.png')
pl.show()

pl.close()

