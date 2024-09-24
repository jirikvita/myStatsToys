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
    Data = readData(infname, 10)
    print(Data)
    
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

