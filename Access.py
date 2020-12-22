import requests
import json
import subprocess
import sys
import operator
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as pl
from PIL import Image
mp.use("TkAgg")

target = 'test'
################################################################
# Global variables #
################################################################
user_list = []
repo_list = []
language_dictionary = {}
language_list = []
language_value = []
target_additions = [0]
hist_additions = [0]
target_removals = [0]
hist_removals = [0]
target_repo_list = []
total_commits = [0]
avg_additions = [0]
avg_removals = [0]
################################################################
# takes dictionary and orders by value - splits into seperate lists #
################################################################
def ordering(dictionary):
	print(dictionary)
	x = sorted(dictionary.items(), key = lambda kv:(kv[1],kv[0]))
	print(x)
	key = []
	value = []
	for i in x:
		key.append(i[0])
		value.append(i[1])
	print(key)
	print(value)	
	plotting_two_datasets(key, value)


################################################################
# Plotting the 2 data sets against one another #
################################################################

def plotting_two_datasets(x, y):	
	fig = pl.figure(figsize=(12,6))
	ax = fig.add_subplot(111)

	ax.bar(x, y)
	ax.set_xticklabels(x, rotation=45)

	pl.savefig(target + '_languages.png')
	#pl.show()
	#pl.close()

################################################################
# Plotting multiple sets against one axis #
################################################################

def plotting_four_datasets(x1, y1, y2, y3, y4):
	pl.plot(x1, y1, label = "Historical additions")
	pl.plot(x1, y2, label = "Historical deletions")
	pl.plot(x1, y3, label = "Avg. additions")
	pl.plot(x1, y4, label = "Avg. deletions")
	pl.xlabel("Commit #")
	pl.ylabel("Lines per commit")
	pl.savefig(target + '_commits.png')
	pl.legend()
	#pl.show()

################################################################
# Sample dictionary to speed up tests #
################################################################
if sys.argv[1] == 'test':
	temp = {'Rust': 1, 'HTML': 2, 'LabVIEW': 1, 'JavaScript': 5, 'C++': 3, 'C': 3, 'Java': 2, 'Python': 6, 'Jupyter Notebook': 3, 'CSS': 1, 'Objective-C': 1, 'TypeScript': 1, 'PHP': 1}
	ordering(temp)
	
################################################################
# Github accesing for data #
################################################################

else :
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

my_headers = {'{username}' : '{access_token}'}

##############################################################
# Take the target user and generate the list of followers #
##############################################################

def get_followers(user):
	url = 'https://api.github.com/users/' + user + '/followers'
	response = requests.get(url,auth=(username, access_token))
	for i in response.json():
		user_list.append(i["login"])
##############################################################
# Take the target user and generate the list of following #
##############################################################
def get_following(user):
	url = 'https://api.github.com/users/' + user + '/following'
	response = requests.get(url,auth=(username, access_token))
	for i in response.json():
		user_list.append(i["login"])
	
################################################################
# Return the language with the most lines commited #
################################################################

def maxLanguages(dictionary):
	max_key = max(dictionary, key=dictionary.get)
	return max_key

#############################################################
# goes through a user's list of public repos and finds the language that has the most lines of code in it
#############################################################
def find_repos(user): 
	url = 'https://api.github.com/users/' + user + '/repos'
	response = requests.get(url,auth=(username, access_token))
	
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
	
	return user_favourite_language



#############################################################
# takes a user's dictionary and returns a dictionary of the largest language in the repo and the assosiated #lines of code
#############################################################
def get_language(repo):
	url = 'https://api.github.com/repos/' + repo + '/languages'
	repo_lang = []
	repo_dict = {}
	response = requests.get(url,auth=(username, access_token ))
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
	
	
	return max_lang

################################
# avg size of commits
################################ 

def commit_changes(repo, commit):
	global target_additions, target_removals, total_commits
	url = 'https://api.github.com/repos/' + repo + '/commits/' + commit
	response = requests.get(url,auth=(username, access_token))
	list_res = response.json()['files']
	dict_res = list_res[0]

	target_additions.append(target_additions[-1] + dict_res['additions']) 
	hist_additions.append(dict_res['additions'])
	target_removals.append(target_removals[-1] + dict_res['deletions'])
	hist_removals.append(dict_res['deletions'])
	total_commits.append(total_commits[-1] + 1) 
	avg_additions.append(int(target_additions[-1] / total_commits[-1]))
	avg_removals.append(int(target_removals[-1] / total_commits[-1]))
	
	

def target_repos():
	url = 'https://api.github.com/users/' + target + '/repos'
	response = requests.get(url,auth=(username, access_token))
	for i in response.json():
		target_repo_list.append(i['full_name'])
	

def target_commits(repo):
	url = 'https://api.github.com/repos/' + repo + '/commits'
	response = requests.get(url,auth=(username, access_token))
	target_commits = []
	for i in response.json():
		target_commits.append(i['sha'])
	for x in target_commits:
		#print(x)
		commit_changes(repo, x)

def commit_size():
	target_repos()
	
	for i in target_repo_list:
		target_commits(i)
	
	plotting_four_datasets(total_commits, hist_additions, hist_removals, avg_additions, avg_removals)
	#print(target_additions)
	#print(target_removals)
	#print(avg_additions)
	#print(avg_removals)
	
	#plotting(target_additions, target_removes)


################################
# Number of commits per language
################################

################################
# Frequency of commits per language
################################
###############################
# Main
###############################

commit_size()

target_fav = find_repos(target)
print(target_fav)
get_followers(target)
print(user_list)
for i in user_list:
	returned_language = find_repos(i)
	if returned_language == '':
		returned_language = 'Nothing'
	if returned_language in language_dictionary:
		language_dictionary[returned_language] = language_dictionary[returned_language] + 1
	else: 
		language_dictionary[returned_language] = 1


ordering(language_dictionary)

f = Image.open(target +"_commits.png").show()
x = Image.open(target +"_languages.png").show()