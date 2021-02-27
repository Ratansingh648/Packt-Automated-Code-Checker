from configparser import ConfigParser
import os
import subprocess
from pprint import pprint
import sys

from NBComparator import NBComparator
from NBRunner import NBRunner
from utils import printAndLog, get_dir_structure

# Reading the configuration file
config = ConfigParser()
config.read('config.ini')

# Defining parameters for following flow
local_dir = config['Repository']['local-repo']
test_dir = os.path.join(os.getcwd(), "TEST")

print("-"*85)
print("Local Directory :: {}".format(local_dir))
print("Git Directory :: {}".format(test_dir))
print("-"*85)


# Handling Git Checkout / Update before matching process
if os.path.exists(test_dir):
    printAndLog("TEST Directory exists. Changing directory to TEST folder ...", "complete")
    os.chdir(test_dir)
    git_folder = config['Repository']['git-repo'].split("/")[-1].split(".")[0]
    git_dir = os.path.join(test_dir, git_folder)
    if os.path.exists(git_dir):
        printAndLog("Detected a cloned folder {} in TEST directory. Pulling the latest".format(git_folder), "warning")
        os.chdir(git_dir)
        try:
            p = subprocess.call("git pull", shell=True)
            if p != 0:
                raise Exception("Git Pull Failed")
        except Exception as e:
            printAndLog("We ran into some problem while updating the git folder.", "error")
            continue_flag = input("Please update the folder manually and press quit (q) / continue (c) :: ")
            if continue_flag.strip().lower() != "c":
                sys.exit()
    else:
        printAndLog("Git Directory doesnt exist. Trying to clone it .. ", "warning")
        try:
            subprocess.call("git clone {}".format(config['Repository']['git-repo']), shell=True)
        except Exception as e:
            printAndLog(e, "error")
            printAndLog("We ran into some problem while cloning the git Repo. ", "error")
            raise RuntimeError
else:
    os.mkdir(test_dir)
    printAndLog("Successfully created TEST folder ...", "complete")
    os.chdir(test_dir)
    subprocess.call("git clone {}".format(config['Repository']['git-repo']), shell=True)
    printAndLog("Clone the git folder in TEST directory", "complete")
printAndLog("Cloned the git folder in TEST directory", "complete")


# Checking the directory tree and pointing the files not considered for match
print(local_dir)
print(git_dir)
local_files = get_dir_structure(local_dir)
git_files = get_dir_structure(git_dir)


# Filtering the data to have folder starting with chapter
local_files = {key: val for key, val in local_files.items() if "Chapter" in key}
git_files = {key: val for key, val in git_files.items() if "Chapter" in key}

if len(local_files) == 0:
    printAndLog("Local Folder do not contain any folder named Chapter", "error")
if len(git_files) == 0:
    print("Git Folder do not contain any folder named Chapter", "error")


# Matching the tree structure
match_status = {'matched': [], 'mismatch': [], 'missing': []}
for sub_folder, sub_files in local_files.items():
    try:
        git_sub_files = git_files[sub_folder]
    except:
        printAndLog("Folder '{}' is missing from the Git Repo".format(sub_folder), "error")
        match_status['missing'].append(sub_folder)
        continue

    if not (git_sub_files == sub_files):
        match_status['mismatch'].append(sub_folder)
        printAndLog("Directory structure inside folder {} doesn't coincide with the git".format(sub_folder), "error")
    else:
        match_status['matched'].append(sub_folder)

printAndLog("Directory Matching Done. Proceeding with execution of matched local folders", "complete")


# Running the local files
for chapter in match_status['matched']:
    print("-"*85)
    printAndLog("Processing {}".format(chapter), "warning")
    for ipynb_file in local_files[chapter]:
        if ipynb_file.endswith('.ipynb'):
            printAndLog("Processing File {}".format(ipynb_file), "complete")
        else:
            printAndLog("Skipping File {}".format(ipynb_file), "warning")
    printAndLog("Done Processing {}".format(chapter), "complete")
