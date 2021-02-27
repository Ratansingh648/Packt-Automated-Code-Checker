"""
Structure to store the state of MarkdownCell
"""


class MarkdownCell(object):

    def __init__(self, source_code=""):
        self.source_code = source_code

    def __eq__(self, other):
        matched = False
        if isinstance(other, self.__class__):
            if self.source_code == other.source_code:
                matched = True
        return matched
