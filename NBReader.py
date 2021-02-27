import json
import os

from Cell.CodeCell import CodeCell
from Cell.MarkdownCell import MarkdownCell

"""
Reads the Jupyter notebook and stores the data as
"""


class NBReader(object):

    def __init__(self):
        self.cells = []

    def read(self, path):
        if os.path.isfile(path):
            try:
                f = open(path).read()
                book = json.loads(f)
                cells = book['cells']

                data = []
                for cell in cells:
                    if cell["cell_type"] == "markdown":
                        data.append(MarkdownCell(cell["source"]))
                    elif cell["cell_type"] == "code":
                        data.append(
                            CodeCell(cell["execution_count"], cell["source"], cell["outputs"]))
                self.cells = data

            except Exception as e:
                print(e)
                print("Error Occured while reading the file {}".format(path))
        else:
            raise FileNotFoundError("File {} does not exist.")
