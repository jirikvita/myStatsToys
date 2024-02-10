#!/usr/bin/python

from math import *
import sys, os
from array import array
#########################################
#########################################

def DoSubs(line, subs):
    newline = '' + line
    for key in subs:
        val = subs[key]
        newline = newline.replace(key, val)
    return newline

#########################################

def main(argv):
    print(argv)
    if len(argv) < 2:
        print('Usage: {} script.py')
        return

    pyname = argv[1]
    cname = pyname.replace('', '')
    if pyname == cname:
        cname = pyname + '.C'

    subs = { '\'' : '"',
             'print(' : 'cout << ',
             'ROOT.' : '',
             ' = TH1D(' : ' = new TH1D(',
             ' = TF1(' : ' = new TF1(',
             ' = TH2D(' : ' = new TH2D(',
             ' = TCanvas(' : ' = new TCanvas(',
             '.' : ' -> ',
             ' -> png' : '.png',
             ' -> pdf' : '.pdf',
             ' -> ,' : '., ',
             ' -> )' : ')',
             
            }
    for xline in os.popen('cat {}'.format(pyname)).readlines():
        line = xline[:-1]
        #print(line)
        newline = DoSubs(line, subs)
        if newline != '':
            newline = newline + ';'
        print(newline)
    return



#########################################
#########################################
#########################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
#########################################
#########################################
#########################################

