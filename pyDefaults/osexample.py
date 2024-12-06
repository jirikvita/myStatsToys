#!/usr/bin/python
import os
files = os.listdir()

for x in files:
    if x.startswith('xyz') and x.endswith('.root'):
        print('Ha!')
