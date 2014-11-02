class SourceDir(object):

    def __init__(self, node, eventrouter, unitTypes):
        self.node = node
        self.eventrouter = eventrouter
        self.unitTypes = unitTypes
        self.units = []
        self.providers = {}

    def __call__(self):
        self._buildUnits(self.node)

    def _buildUnits(self, node):
        for unitType in self.unitTypes:
            unit = unitType.getUnit(node)
            if unit:
                for provide in unit.provides:
                    if provide not in self.providers:
                        self.providers[provide] = []
                    self.providers[provide].append(unit)
        for child in node.getChildren():
            self._buildUnits(child)
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
