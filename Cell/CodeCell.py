"""
Structure to store the state of the Code Cell
"""


class CodeCell(object):

    def __init__(self, execution_count="", source_code="", output=""):
        self.execution_count = execution_count
        self.source_code = source_code
        self.output = output

    def __eq__(self, other):
        matched = False
        if isinstance(other, self.__class__):
            if self.source_code == other.source_code and self.output == other.output:
                matched = True
        return matched
