"""
Reads and extracts Node data out of a directory
"""

from threading import Event, Thread
from services.events import EventHandler
import queue
import pyinotify
import time

class SourceDir(EventHandler):
    """
    Creates Nodes based on directory contents.

    unit channel:
        new(Node): the Node has been created
    """

    mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY | pyinotify.IN_DELETE_SELF

    def __init__(self, node, eventrouter, unitTypes):
        super(SourceDir, self).__init__()
        self.node = node
        self.eventrouter = eventrouter
        self.utypes = unitTypes
        self.units = []
        self.providers = {}

        self.watchmanager = pyinotify.WatchManager()
        self.notifier = pyinotify.ThreadedNotifier(self.watchmanager, SourceDirEventHandler())
        self.notifier.start()

        self.eventrouter.add(self, 'unit')

        # Initialized. Notify world.
        self.eventrouter.fire(self, 'unit', ('new', self.node))

    def _handle(self, event, sender, eargs):
        eventType, node = eargs
        if eventType is 'new':
            self.watchmanager.add_watch(node.realpath, SourceDir.mask)
            for child in node.getChildren():
                for unitType in self.utypes:
                    unit = unitType.getUnit(node)
                    if unit:
                        for provide in unit.provides:
                            if provide not in self.providers:
                                self.providers[provide] = []
                            self.providers[provide].append(unit)
                self.eventrouter.fire(self, 'unit', ('new', child))

    def stop(self):
        super(SourceDir, self).stop()
        self.notifier.stop()

class SourceDirEventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print("Creating: ", event.pathname)
    def process_IN_MODIFY(self, event):
        print("Modify: ", event.pathname)
    def process_IN_DELETE(self, event):
        print("Removing: ", event.pathname)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
