from collections import deque

class CompilationGroup():

    def __init__(self):
	self.units = []

class DepGraph():

    def __init__(self, sourcedir):
	self.sourcedir = sourcedir
	self._providestack = []
	self._groupstack = []
	self._providetogroup = {}

	# Iterate over each unit in each provider...
	for provide in self.sourcedir.providers:
	    self._calculateGraph(provide)
	print self._providestack

    def _calculateGraph(self, provide):
	if provide in self._providestack:
	    return
	# Breadth-first search for cycles or leaf nodes
	for unit in self.sourcedir.providers[provide]:
	    for depend in unit.depends:
		if depend not in self.sourcedir.providers:
		    raise Exception('Unit at node ' + unit.node.path + ' which provides ' + provide + ' is missing dependency: ' + depend)
		elif depend == unit.provides:
		    # TODO: provide warning
		    continue
		elif depend in self._providestack:
		    print('cycle: ' + provide + ' -> ' + depend)
	# Depth-first search
	self._providestack.append(provide)
	for unit in self.sourcedir.providers[provide]:
	    for depend in unit.depends:
		self._calculateGraph(depend)
