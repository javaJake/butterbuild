"""This module maps out the hierarchy of dependencies.

It primarily tries to organize dependencies so that the ones with no
dependencies are at the "top", and ones with the most dependencies
are at the bottom."""

from services.events import EventHandler

class DepGraph(EventHandler):
    """Handles unit events and maintains a depgraph"""

    def __init__(self, eventrouter):
        super(DepGraph, self).__init__()
        self.eventrouter = eventrouter
        self.eventrouter.add(self, 'unit')

    def _handle(self, event, sender, eargs):
        print('hi', event, eargs)
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
