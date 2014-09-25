#!/usr/bin/env python

import argparse
import os

from unit import java
from services.fs import split_path, path_to_node, Node
from services.sourcedir import SourceDir
from services.depgraph import DepGraph
    
parser = argparse.ArgumentParser(description='Build stuff')
parser.add_argument('source', metavar='source', help='The source')
args = parser.parse_args()
# Insert source as top-level dependency
# Locate dependencies; insert; rinse and repeat
# Build once dependencies are satisfied
rootnode = Node(None, None, '/')
sourcenode = path_to_node(rootnode, args.source)

sourcedir = SourceDir(sourcenode, [java])
depgraph = DepGraph(sourcedir)
groupidstack = depgraph.groupstack.keys()
groupidstack.reverse()
for groupid in groupidstack:
    print '>>> Compile:'
    units = []
    for provide in depgraph.groupstack[groupid]:
	units.extend(sourcedir.providers[provide])
    print('classpaths: ' + str([unit.classpath.path for unit in units]))
    print('java files: ' + str([unit.node.path for unit in units]))
