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
        self.name = node.filename[:node.filename.rfind('.java')]
	self.classpath = node.parent
        with open(node.path) as f:
            for line in f:
                pkg = Java._pkg_re.search(line)
                if pkg:
		    pkg = pkg.group('name')
                    self.provides.append('java:'+pkg+'.'+self.name)
		    self._calculateClasspath(pkg)

                importPkg = Java._import_pkg_re.search(line)
                if importPkg:
                    self.depends.append('java:'+importPkg.group('name'))
                elif 'class' in line:
                    # no more imports possible
                    break

    def _calculateClasspath(self, pkg):
	pkgparts = pkg.split('.')
	pkgparts.reverse()
	pkgnode = self.node
	for pkgpart in pkgparts:
	    pkgnode = pkgnode.parent
	    if pkgnode is None or pkgnode.parent is None:
		raise Exception('package decleration "'+str(pkg)+'" invalid; classpath calculation failed: '+self.node.path)
	    elif pkgnode.filename is not pkgpart:
		raise Exception('package decleration "'+str(pkg)+'" invalid for directory "'+str(pkgnode.filename)+'"; classpath calculation failed: '+self.node.path)
	self.classpath = pkgnode.parent

    def getProvides(self):
        return self.provides

    def getDepends(self):
        return self.depends
