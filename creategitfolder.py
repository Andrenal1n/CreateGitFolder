# script for automated creation of a git project
# imports
import os
from wsgiref import headers
import git
from pip import main
import requests
from pprint import pprint
from secrets import GITHUB_TOKEN
from secrets import path

# navigate to projects folder
os.chdir(path)
current_dir = os.getcwd()

# create a new folder
# ask the user for the new folder name
name_dir = input("Please enter the name for the new project: ")
print("The new project will be named: " + name_dir)

# create the folder with the new name
try:
    os.mkdir(name_dir)

# check if folder already exists
except FileExistsError:
    print("The folder " + name_dir + " already exists")

# navigate into the new folder
os.chdir(name_dir)
current_dir = os.getcwd()

# create a README file
readme = open("README.md", "w+") 
main_file_name = name_dir + ".py" 
main_file = open(main_file_name, "w+")

# write a first description into the README
readme_description = input("Please enter a first description for your project: ")
readme.write("The project " + name_dir + " has the following description: " + readme_description)

# initialize git repo
repository = git.Repo.init()

# navigate to github.com and create a new repo with the designated project name
API_URL = "https://api.github.com/"
payload = '{"name": "' + name_dir + '" }'
headers = {
    "Authorization": "token " + GITHUB_TOKEN,
    "Accept": "application/vnd.github+json"
}
r = requests.post(API_URL+"user/repos", data=payload, headers=headers)
pprint(r.json())
    
# add all files (README.md)    
repository.index.add(["README.md", main_file_name])
print("README.md and main.py was added")
    
# Provide a commit message
repository.index.commit('Initial commit.')
print("An initial commit was done")

# add the git remote repository
repo_url = "https://github.com/Andrenal1n/" + name_dir+ ".git"
repository.create_remote("origin", repo_url)

# push the changes to the repo
repository.git.push('origin', '-u', 'master')
print("Everything was pushed")

os.startfile(main_file_name)


# if repository.is_dirty(untracked_files=True):
#     print('Changes detected.')
# else:
#     print("Everything is OK")

    
