class SourceDir():

    def __init__(self, node, unitTypes):
        self.node = node
        self.unitTypes = unitTypes
        self.units = []
        self.providers = {}
        self._buildUnits(node)

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
