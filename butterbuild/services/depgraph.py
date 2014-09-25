from collections import deque

class CompilationGroup():

    def __init__(self):
	self.units = []

class DepGraph():

    def __init__(self, sourcedir):
	self.debug = False
	self.sourcedir = sourcedir
	self.groupstack = {}
	self._providetogroup = {}
	self._nextgroupid = 0

	# Iterate over each unit in each provider...
	for provide in self.sourcedir.providers:
	    self._calculateGraph([], provide)

    def _calculateGraph(self, depthstack, provide):
	if provide in self._providetogroup:
	    return

	if self.debug: print('>>> ' + provide)
	# Breadth-first search for cycles
	for unit in self.sourcedir.providers[provide]:
	    for depend in unit.depends:
		if depend not in self.sourcedir.providers:
		    raise Exception('Unit at node ' + unit.node.path + ' which provides ' + provide + ' is missing dependency: ' + depend)
		elif depend == unit.provides:
		    # TODO: provide warning
		    continue
		elif depend in depthstack:
		    # (a,b)->(c,d)->e->a becomes:
		    # (a,b,c,d,e)
		    cycle = depthstack[depthstack.index(depend):]
		    cycle.append(provide)
		    if self.debug: print('groupcycle: ' + str(cycle) + ' -> ' + depend)

		    groupid = self._nextgroupid
		    self._nextgroupid+=1

		    collapsablegroupids = [] # dict guarantees uniqueness; value doesn't matter
		    newgroup = []
		    for cycleMember in cycle:
			if cycleMember in self._providetogroup:
			    oldgroupid = self._providetogroup[cycleMember]
			    oldgroup = self.groupstack[oldgroupid]
			    newgroup.extend(oldgroup)
			    for oldprovide in oldgroup:
				self._providetogroup.pop(oldprovide)
			    self.groupstack.pop(oldgroupid)
			else:
			    newgroup.append(cycleMember)
		    self._addToGroup(newgroup, groupid)
		else:
		    if self.debug: print(depend + ' is not cycled')
	
	# Depth-"after" search
	if self.debug: print(provide + ' initiating depth search')
	if provide not in self._providetogroup:
	    self._addToGroup([provide], self._nextgroupid)
	    self._nextgroupid+=1
	depthstack.append(provide)
	for unit in self.sourcedir.providers[provide]:
	    for depend in unit.depends:
		if depend == unit.provides:
		    # TODO: provide warning
		    continue
		self._calculateGraph(depthstack[:], depend)
	if self.debug: print('<<< ' + provide)

    def _addToGroup(self, newgroup, groupid = -1):
	if groupid in self.groupstack:
	    self.groupstack[groupid].extend(newgroup)
	else:
	    self.groupstack[groupid] = newgroup
	if self.debug: print('new group: ' + str(groupid) + ': ' + str(self.groupstack[groupid]))
	for provide in newgroup:
	    if provide in self._providetogroup:
		raise Exception('provide already exists in a compile group: ' + provide)
	    self._providetogroup[provide] = groupid
