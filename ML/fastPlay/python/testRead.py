#!/usr/bin/python

# was: #!/snap/bin/pyroot
# was: #!/usr/bin/python3

# Út 24. září 2024, 13:57:02 CEST

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

from readData import *

stuff = []

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    # infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_5k.txt'
    infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_full.txt'
    
    # central vals and sigma around them to accept
    # visible square areas:
    restrictions1 = { 'logE' : [ [17., 18, 19, 20], 0.20],
                      'Xmax' : [ [400, 600, 800], 50 ],
                      'Azimuth' : [ [0.], 45],
                      'Zenith' : [ [45.], 25],
                      'Corex' : [ [-18000, -15000], 1000],
                      'Corey' : [ [-22000, -18000], 1000]
                     }
    
    # more relaxed:
    restrictions2 = { 'Azimuth' : [ [125.], 40],
                      'Zenith' : [ [80.], 40.],
                      'Corex' : [ [-18000], 8000],
                      'Corey' : [ [-18000], 8000]
                     }

    restrictions = restrictions1
    #restrictions = {}
    
    Data = readData(infname, 0, -1, verb=1000, debug = 0, plotmetahistos = True, restrictions = restrictions)
    ###print(Data)
    print(f'Read {len(Data)} data lines.')
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

