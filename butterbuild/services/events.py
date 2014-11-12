import threading
import queue

class Event(object):

    def __init__(self, name):
        self.name = name
        self.handlers = []
        self.lock = threading.Lock()
    
    def add(self, handler):
        with self.lock:
            self.handlers.append(handler)
    
    def remove(self, handler):
        with self.lock:
            self.handlers.remove(handler)

    def stop(self):
        with self.lock:
            for handler in self.handlers:
                handler.stop()
    
    def fire(self, sender, earg=None):
        with self.lock:
            for handler in self.handlers:
                handler.handle(self.name, sender, earg)

class EventHandler(threading.Thread):

    def __init__(self):
        super(EventHandler, self).__init__()
        self.stopevent = threading.Event()
        self.idleevent = threading.Event()
        self.eventqueue = queue.Queue()
        threading.Thread(target=self._threadLoop).start()

    def handle(self, name, sender, earg):
        self.eventqueue.put((name, sender, earg))

    def _handle(self, name, sender, earg):
        pass

    def stop(self):
        self.stopevent.set()

    def isIdle(self):
        return self.idleevent.is_set()

    def waitIdle(self):
        return self.idleevent.wait()

    def _threadLoop(self):
        while not self.stopevent.is_set():
            try:
                event, sender, eargs = self.eventqueue.get(True, 1)
                self.idleevent.clear()
                self._handle(event, sender, eargs)
            except queue.Empty:
                self.idleevent.set()
                continue

class EventRouter(object):

    def __init__(self):
        self.channels = {}
        self.lock = threading.Lock()

    def add(self, handler, channel):
        with self.lock:
            if channel not in self.channels:
                self.channels[channel] = Event(channel)
        self.channels[channel].add(handler)

    def remove(self, handler, channel):
        with self.lock:
            if channel not in self.channels:
                return
        self.channels[channel].remove(handler)

    def stop(self):
        with self.lock:
            for name, channel in self.channels.items():
                channel.stop()

    def fire(self, sender, channel, earg=None):
        with self.lock:
            print("[Event: "+channel+", " + str(earg) + "]")
            if channel not in self.channels:
                return
        self.channels[channel].fire(sender, earg)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
