import requests
import json
import os
from urllib.parse import urlparse


ext = [".cpp", ".c", ".h", ".hpp", ".cxx", ".cc", ".ii", ".ixx", ".ipp",
       ".inl", ".txx", ".tpp", "tpl"]


def get_response(url, user, pswd):
    r = requests.get(url, auth=(user, pswd))
    if r.ok:
        r = json.loads(r.text or r.content)
        return r


def get_files(url, user, repo_name, auth_user, pswd):
    contents = get_response(url, auth_user, pswd)
    for file in contents:
        if file['name'].endswith(tuple(ext)):
            download_file(file['download_url'], user, repo_name, file['name'])
        if file['type'] == "dir":
            get_files(file['_links']['self'], user, repo_name, auth_user, pswd)


def scrap(userlist, auth_user, psw):
    for user in userlist:
        repos = get_response('https://api.github.com/users/' + user + '/repos', auth_user, psw)
        if repos:
            for repo in repos:
                if (repo['language'] == 'C++' or repo['language'] == 'C') and repo['fork'] == False:
                    contents_url = 'https://api.github.com/repos/' + \
                        user + '/' + repo['name'] + '/contents'
                    repo_name = repo['name']
                    get_files(contents_url, user, repo_name, auth_user, psw)


def download_file(url, user, repo_name, filename):
    path = os.path.join('./data', user, repo_name, filename)
    try:
        os.makedirs(os.path.dirname(path))
    except FileExistsError:
        pass
    response = requests.get(url, stream=True)
    if response.ok:
        with open(path, 'wb') as file:
            file.write(response.content)
