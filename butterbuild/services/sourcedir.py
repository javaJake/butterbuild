from threading import Event, Thread
from services.events import EventHandler
import queue

class SourceDir(EventHandler):

    def __init__(self, node, eventrouter, unitTypes):
        super(SourceDir, self).__init__()
        self.node = node
        self.eventrouter = eventrouter
        self.unitTypes = unitTypes
        self.units = []
        self.providers = {}
        self.eventrouter.add(self, 'unit')

        # Initialized. Notify world.
        self.eventrouter.fire(self, 'unit', ('new', self.node))

    def _handle(self, event, sender, eargs):
        eventType, node = eargs
        if eventType is 'new':
            for child in node.getChildren():
                for unitType in self.unitTypes:
                    unit = unitType.getUnit(node)
                    if unit:
                        for provide in unit.provides:
                            if provide not in self.providers:
                                self.providers[provide] = []
                            self.providers[provide].append(unit)
                self.eventrouter.fire(self, 'unit', ('new', child))
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
