"""Provides some basic filesystem analysis functions."""

import os
import threading

def split_path(path):
    """ Inspired by http://stackoverflow.com/a/4580931/387239
    Splits a path into its parts """

    parts = []
    while True:
        newpath, tail = os.path.split(path)
        if newpath == path:
            assert not tail
            if path:
                parts.append(path)
            break
        parts.append(tail)
        path = newpath
    parts.reverse()
    return parts

def get_root():
    """ Gets the root path of the OS """
    return os.path.abspath(os.sep)

def path_to_node(rootnode, pathstr):
    """ Resolves the filesystem node that represents theA given path. """
    node = rootnode
    for part in split_path(os.path.abspath(pathstr)):
        node = node.getChild(part)
    return node

class FileNotExistsError(Exception):
    """ Error thrown when the file on disk does not exist. """
    pass

class Node():
    """ An object which represents a file on disk """

    def __init__(self, root, parent, filename):
        self.root = root
        if root is None:
            self.root = self

        self.parent = parent
        self.filename = filename
        self.__metadata = dict()
        self.__children = dict()
        self.__childrenlock = threading.Lock()

        if self.parent != None:
            self.path = os.path.join(self.parent.path, self.filename)
        else:
            self.path = self.filename

        if not os.path.exists(self.path):
            raise FileNotExistsError(self.path)
        elif os.path.abspath(self.path) != self.path:
            raise ValueError("Path is not absolute: "+str(filename))

        if os.path.islink(self.path):
            # resolve symbolic link
            self.realpath = os.readlink(self.path)
            realpathParts = split_path(self.realpath)
            try:
                currNode = self.root
                for part in realpathParts[1:]:
                    currNode = currNode.getChild(part)
                # we now target another node
                self.__target = currNode
            except FileNotExistsError:
                raise FileNotExistsError(self.path, "symbolic link points to a non-existant path")
        else:
            self.realpath = self.path
            self.__target = None

    def getChild(self, filename):
        """ Gets a child node """

        if self.__target != None:
            return self.__target.getChild(filename)

        if not filename in self.__children:
            with self.__childrenlock:
                if not filename in self.__children:
                    self.__children[filename] = Node(self.root, self, filename)

        return self.__children[filename]

    def getChildren(self):
        """ Gets all known children nodes """

        if self.__target != None:
            return self.__target.getChildren()

        childrenList = []
        if os.path.isdir(self.path):
            for filename in os.listdir(self.path):
                childrenList.append(self.getChild(filename))
        return childrenList

    def getMeta(self, key):
        """ Gets a piece of metadata for this node """

        if not key in self.__metadata:
            if self.__target != None:
                return self.__target.getMeta(key)
            else:
                return None
        else:
            return self.__metadata[key]

    def setMeta(self, key, value):
        """ Sets a piece of metadata for this node """

        if self.__target != None:
            return self.__target.setMeta(key, value)

        self.__metadata[key] = value
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
