#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import codecs
import requests

def d(msg):
    if not nodebugfile:
        debugFile.write(msg + "\n")

    if verbose == False:
        return

    print msg

scriptPath = os.path.dirname(os.path.abspath(__file__))
debugPath = '/tmp/fr24-stats-dump1090-json-cacti.log'
debugFile = codecs.open(debugPath,'w','utf-8')

# Parse command line arguments
# ======================================================================
parser = argparse.ArgumentParser(description='Parse and output dump1090 stats for aircrafts tracked with fr24')

parser.add_argument('--server', help='IP address of the fr24 server', required=False, action="store")
parser.add_argument('--verbose', help='Print debug information', action="store_true", required=False)
parser.add_argument('--nodebugfile', help='Do not log to debug file', action="store_true", required=False)

args = parser.parse_args()

# Logic to handle command line arguments
# ======================================================================
if args.nodebugfile:
    nodebugfile = True
    d('Disabling debug file')
else:
    nodebugfile = False

if args.verbose:
    verbose = True
    d('Enabling verbosity as requested by command line')
else:
    verbose = False

if args.server:
    server = args.server
else:
    print('ERROR: No server name of your local fr24 installation provided. Cannot continue.')
    sys.exit(1)

try:
    debugFile = codecs.open(debugPath,'w','utf-8')
except:
    print('ERROR: Could not open "' + debugPath + '" for writing. Cannot continue.')
    sys.exit(1)

url = 'http://' + server + '/dump1090/data/aircraft.json'
r = requests.get(url)
rJson = r.json()

data = {}

if rJson['now']:
    data['TIMESTAMP'] = str(rJson['now'])

if rJson['aircraft']:
    aircraftsCount = len(rJson['aircraft'])
    data['AIRCRAFTS'] = str(aircraftsCount)

if rJson['messages']:
    data['MESSAGES'] = str(rJson['messages'])

out = ''
for key, value in data.iteritems():
    out = out + key + ':' + value + ' '

print out
