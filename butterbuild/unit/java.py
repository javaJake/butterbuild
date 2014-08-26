import fnmatch
import os
import re

from services.fs import Node

def getUnit(node):
    if not node.path.endswith('.java'):
        return None

    return Java(node)

class Java:

    _pkg_re = re.compile('package[\s]+(?P<name>[^\s;]+)')
    _import_pkg_re = re.compile('import[\s]+(?:static[\s]+)*(?P<name>[^\s;]+)')

    def __init__(self, node):
        self.node = node
        self.provides = []
        self.depends = []
        self.name = node.filename[:-1*node.filename.rfind('.java')-1]
        with open(node.path) as f:
            for line in f:
                pkg = Java._pkg_re.search(line)
                if pkg:
                    self.provides.append('java:'+pkg.group('name')+'.'+self.name)

                importPkg = Java._import_pkg_re.search(line)
                if importPkg:
                    self.depends.append('java:'+importPkg.group('name'))
                elif 'class' in line:
                    # no more imports possible
                    break

    def getProvides(self):
        return self.provides

    def getDepends(self):
        return self.depends
