import fnmatch
import os

from services.fs import Node

class Java:

    def isUnit(self, node):
        if node.path.endswith('.java'):
            return True
        else:
            return False
