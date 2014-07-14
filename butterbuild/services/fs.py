import os
import threading

# http://stackoverflow.com/a/4580931/387239
#def os_path_split_asunder(path):
#    components = [] 
#    while True:
#        (path,tail) = os.path.split(path)
#        if tail == "":
#            components.reverse()
#            return components
#        components.append(tail)

def os_path_split_asunder(path, debug=False):
    parts = []
    while True:
        newpath, tail = os.path.split(path)
        if debug: print repr(path), (newpath, tail)
        if newpath == path:
            assert not tail
            if path: parts.append(path)
            break
        parts.append(tail)
        path = newpath
    parts.reverse()
    return parts


class Filesystem():

    def __init__(self):
        self.cache = dict()
        self.lock = threading.Lock()

    def get(self, path):
        path = os_path_split_asunder(os.path.abspath(path))

        with self.lock:
            i = 0
            currCache = self.cache
            print("Scanning ",path)
            while i < len(path):
                if not path[i] in currCache:
                    currCache[path[i]] = os.listdir(os.path.join(*path[0:(i+1)]))
                currCache = currCache[path[i]]
                i+=1

            return currCache
