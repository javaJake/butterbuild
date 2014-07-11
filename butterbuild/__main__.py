#!/usr/bin/env python

import argparse
    
parser = argparse.ArgumentParser(description='Build stuff')
parser.add_argument('source', metavar='S', type=file, help='The source directory')
# Insert source as top-level dependency
# Locate dependencies; insert; rinse and repeat
# Build once dependencies are satisfied
