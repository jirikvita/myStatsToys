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
    restrictions = { #'logE' : [ [17.5, 18, 19, 20], 0.25],
                     #'Xmax' : [ [390], 250 ],
                     'Azimuth' : [ [100.], 100],
                     'Zenith' : [ [40.], 50],
                     'Corex' : [ [-20000], 10000],
                     'Corey' : [ [-15000], 10000]
                }
    Data = readData(infname, 0, verb=1000, debug = 1, restrictions = {})#restrictions)
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

