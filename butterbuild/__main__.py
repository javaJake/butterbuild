#!/usr/bin/env python

import argparse
import os

from unit.java import Java
from services.fs import split_path, Node
    
parser = argparse.ArgumentParser(description='Build stuff')
parser.add_argument('source', metavar='source', help='The source')
args = parser.parse_args()
# Insert source as top-level dependency
# Locate dependencies; insert; rinse and repeat
# Build once dependencies are satisfied
rootnode = Node(None, None, '/')

sourcenode = rootnode
for part in split_path(os.path.abspath(args.source)):
    sourcenode = sourcenode.getChild(part)

print(Java().isUnit(sourcenode))
