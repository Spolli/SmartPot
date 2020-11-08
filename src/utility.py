#!/usr/bin/env python3

import json

def getDataSheet(filename):
    with open(filename, 'r') as f:
        return json.load(f)
