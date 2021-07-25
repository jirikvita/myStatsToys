#!/usr/bin/python

import os, sys

hists = ['xi', 'DijetMass', 
         'njets',
         'LeadJetPt', 'SubLeadJetPt',
         'LeadJetEta', 'SubLeadJetEta'
         ]



exe='root -b -q -l \'draw.c+'

tags = ['0', '1', '2', '3']

for tag in tags:

    for hist in hists:
        cmd = exe + "(\"%s\", %s)'" % (hist, tag)
        print cmd
        os.system(cmd)
