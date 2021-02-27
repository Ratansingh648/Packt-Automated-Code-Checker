from click import secho
import os

"""
STDOUT utility for colored messages
"""


def printAndLog(message, level):
    if level == "error":
        secho(message, fg="red")
    elif level == "warning":
        secho(message, fg="yellow")
    elif level == "complete":
        secho(message, fg="green")
    else:
        print(message)


"""
Returns a dictionary depicting the tree structure
"""


def get_dir_structure(directory):
    directory_structure = {}
    directory_list = os.listdir(directory)
    skip_folders = [".ipynb_checkpoints"]
    skip_files = [".ipynb_checkpoints"]
    for element in directory_list:
        # Skipping some files and folders
        if element in skip_folders or element in skip_files:
            continue

        if os.path.isdir(os.path.join(directory, element)):
            directory_structure[element] = get_dir_structure(os.path.join(directory, element))
        else:
            directory_structure[element] = None
    return directory_structure
