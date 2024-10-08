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
    infname = '/home/qitek/work/github/myStatsToys/FastProcessing/ascii_5k.txt'
    
    # central vals and sigma around them to accept
    restrictions = { 'logE' : [ [17.5, 18, 19, 20], 0.25],
                     'Xmax' : [ [390], 250 ],
                     'Azimuth' : [ [4.5], 40],
                     'Zenith' : [ [7.], 40],
                     'Corex' : [ [-18000], 2000],
                     'Corey' : [ [-25000], 2000]
                }
    Data = readData(infname, 0, verb=1000, debug = -1, restrictions = {})#restrictions)
    ###print(Data)
    
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

