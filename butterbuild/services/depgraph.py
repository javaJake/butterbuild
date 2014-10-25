from collections import deque
import itertools

class CompilationGroup():

    def __init__(self, units=[]):
	self.units = {}
	self.depends = []
	self.addUnits(units)
	
    def addUnits(self, units):
	self.units.update(dict([ (unit.name, unit) for unit in units]))
	self.depends.extend(list(itertools.chain.from_iterable([unit.depends for unit in units])))

class DepGraph():

    def __init__(self, sourcedir):
	self.debug = True
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

		    newgroup = CompilationGroup()
		    for cycleMember in cycle:
			if cycleMember in self._providetogroup:
			    oldgroupid = self._providetogroup[cycleMember]
			    oldgroup = self.groupstack[oldgroupid]
			    print ('del group: '+str(oldgroupid))
			    newgroup.addUnits(oldgroup.units)
			    for oldprovidelist in [groupunit.provides for groupunit in oldgroup.units]:
				for oldprovide in oldprovidelist:
				    self._providetogroup.pop(oldprovide)
			    self.groupstack.pop(oldgroupid)
			else:
			    newgroup.addUnits(self.sourcedir.providers[cycleMember])
		    self._addToGroup(newgroup, groupid)
		else:
		    if self.debug: print(depend + ' is not cycled')
	
	# Depth-"after" search
	if self.debug: print(provide + ' initiating depth search')
	if provide not in self._providetogroup:
	    self._addToGroup(CompilationGroup(self.sourcedir.providers[provide]), self._nextgroupid)
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
	    self.groupstack[groupid].addUnits(newgroup.units)
	else:
	    self.groupstack[groupid] = newgroup
	if self.debug: print('new group: ' + str(groupid) + ': ' + str(self.groupstack[groupid]))
	for provide in newgroup.units.viewvalues():
	    print provide
	    if provide in self._providetogroup:
	       raise Exception('provide already exists in a compile group: ' + provide)
	    self._providetogroup[provide] = groupid
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
