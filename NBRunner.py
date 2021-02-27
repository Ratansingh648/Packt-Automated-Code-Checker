import os
import subprocess

"""
Runs the given notebook and stores the file with same on given path
"""


class NBRunner(object):
    def __init__(self, dest_dir):
        self.__dest_dir = dest_dir

    def run(self, notebook):
        if not os.path.isfile(notebook):
            raise FileNotFoundError
        try:
            subprocess.call('jupyter nbconvert --to notebook --execute "{}" --output-dir {}'.format(notebook, self.__dest_dir), shell=True)
        except Exception as e:
            print(e)
            raise RuntimeError
