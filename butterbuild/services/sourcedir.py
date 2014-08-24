class SourceDir():

    def __init__(self, node, unitTypes):
        self.node = node
        self.unitTypes = unitTypes
        self.units = []
        self._buildUnits(node)

    def _buildUnits(self, node):
        for unitType in self.unitTypes:
            unit = unitType.getUnit(node)
            if unit:
                self.units.append(unit)
        for child in node.getChildren():
            self._buildUnits(child)
