import threading

class Event(object):

    def __init__(self):
        self.handlers = []
        self.lock = threading.Lock()
    
    def add(self, handler):
        with self.lock:
            self.handlers.append(handler)
    
    def remove(self, handler):
        with self.lock:
            self.handlers.remove(handler)
    
    def fire(self, sender, earg=None):
        with self.lock:
            for handler in self.handlers:
                handler.handle(sender, earg)

class EventHandler(object):

    def __init__(self):
        self.eventqueue = queue.Queue()

    def handle(self, earg):
        self.eventqueue.put(earg)

    def nextEvent(self):
        return self.eventqueue.get()

class EventRouter(object):

    def __init__(self):
        self.channels = {}
        self.lock = threading.Lock()

    def add(self, channel, handler):
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = EventHandler()
        self.channels[channel].add(handler)

    def remove(self, channel, handler):
        with self.lock:
            if channel not in self.channels:
                return
        self.channels[channel].remove(handler)

    def fire(self, sender, channel, earg=None):
        with self.lock:
            if channel not in self.channels:
                return
        self.channels[channel].fire(sender, channel, earg)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
