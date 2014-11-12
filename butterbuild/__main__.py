#!/usr/bin/env python

import argparse
import os

from unit import java
from services.events import EventRouter
from services.fs import split_path, path_to_node, Node
from services.sourcedir import SourceDir
from services.depgraph import DepGraph
from threading import Thread
    
parser = argparse.ArgumentParser(description='Build stuff')
parser.add_argument('source', metavar='source', help='The source')
args = parser.parse_args()

# Insert source as top-level dependency
# Locate dependencies; insert; rinse and repeat
# Build once dependencies are satisfied
rootnode = Node(None, None, '/')
sourcenode = path_to_node(rootnode, args.source)
eventrouter = EventRouter()

print('>>> Loading source')
sourcedir = SourceDir(sourcenode, eventrouter, [java])
sourcedir.waitIdle()
print('>>> Closing')

sourcedir.stop()
eventrouter.stop()

