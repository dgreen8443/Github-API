import requests, json
import subprocess
import sys
access_token = '1a23bd36a62a85df3fd3188c76c5591ab8ff7125'
my_headers = {'Authorization' : '{access_token}'}


response = requests.get('https://api.github.com/repos/dgreen8443/Connect4', headers = my_headers)
print(response.json())
