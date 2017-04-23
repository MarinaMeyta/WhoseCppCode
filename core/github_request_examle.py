import requests
import json
import os
from urllib.parse import urlparse

auth_user = "MarinaMeyta"
psw = "722mmv20011994"
basedir = '/media/marina/hdd/diploma'

userlist = ['paroj', 'asmorkalov']
ext = [".cpp", ".c", ".h"]

def get_response(url, user, pswd):
    r = requests.get(url, auth=(user, pswd))
    if r.ok:
        r = json.loads(r.text or r.content)
        return r


def get_files(url, user, auth_user, pswd):
    contents = get_response(url, auth_user, pswd)
    for file in contents:
        if file['name'].endswith(tuple(ext)):
            print('appending...')
            print(urlparse(file['download_url']).path)
            download_file(file['download_url'], file[''])
        if file['type'] == "dir":
            print('is a dir...')
            get_files(file['_links']['self'], user, auth_user, pswd)


def download_files(user):
    repos = get_response('https://api.github.com/users/' + user + '/repos', auth_user, psw)
    for repo in repos:
        if (repo['language'] == 'C++' or repo['language'] == 'C') and repo['fork'] == False:
            links = get_files('https://api.github.com/repos/' + user + '/' + repo['name'] + '/contents', user, auth_user, psw)


#repos = {user:get_download_links(user) for user in userlist}
#print(repos)

def download_file(url, user, repo, filename):
    path = os.path.join(user, repo, filename)
    print(path)
    #os.makedirs(path, exist_ok=True)
    response = requests.get(url, stream=True)
    if response.ok:
        with open(path, 'wb') as file:
            file.write(response.content)

download_files('paroj')
