#!/snap/bin/pyroot

# was: #!/usr/bin/python3
# St 1. května 2024, 17:24:52 CEST

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt

kEpsilon = 1.e-6

cans = []
stuff = []
allstuff = []

##########################################

class mypoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    #def __init__(self, point):
    #    self.x = point.x
    #    self.y = point.y
    def __add__(self, other):
        return mypoint(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return mypoint(self.x - other.x, self.y - other.y)
    def __truediv__(self, denum):
        if isinstance(denum, float):
            if abs(denum) > kEpsilon:
                self.x = self.x / denum
                self.y = self.y / denum
    def Divide(self, denum):
        if abs(denum) > kEpsilon:
            self.x = self.x / denum
            self.y = self.y / denum
        return self

##########################################
def MakeThreeSetOfMidPoints(points):
    #print('making points')    
    newpoints = [
        # Left
        [points[0],
         (points[0] + points[1]).Divide(2.),
         (points[0] + points[2]).Divide(2.), 
         ],
        # Right
        [(points[0] + points[1]).Divide(2.),
         points[1],
         (points[1] + points[2]).Divide(2.),
         ],
        # Top
        [(points[0] + points[2]).Divide(2.), 
         (points[1] + points[2]).Divide(2.), 
         points[2]
         ]
    ]
                    
        
    #print('created ', points)
    return newpoints

##########################################
def DrawTriangle(points, nLevels, level, tid):
    lines = []
    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if j >= i:
                continue
            #print('  coors: ', points[i].x, points[i].y, 
            #      points[j].x, points[j].y)
            line = ROOT.TLine(points[i].x, points[i].y, 
                              points[j].x, points[j].y)
            lines.append(line)     
            lines[-1].SetNDC()
            dc = 0
            #if level == 1:
            #    dc = tid
            #ci = ROOT.TColor.GetFreeColorIndex()
            #color = ROOT.TColor(ci, (points[i].x + points[i].y)/2, 
            #                    (points[j].x + points[j].y)/2,
            #                    abs(points[i].x - points[i].y)/2)
            color = ROOT.TColor()
            #cc = color.GetColor( int(256*(points[i].x + points[i].y)/2), int(256*(points[j].x + points[j].y)/2), int(256*abs(points[i].x + points[i].y)/4))                              
            #cc = color.GetColor( int(256*(points[i].x)/2), int(256*(points[j].x + points[j].y)/2), int(256*abs(points[i].x + points[i].y)/2))
            cc = color.GetColor( int(256*(1. - points[i].x)) - 10, int(256*(points[i].x + points[i].y)/2) - 10, int(256*abs(1. - points[i].y/2)) - 10)
            line.SetLineColor(cc)
            line.SetLineStyle(1)
            line.SetLineWidth(1) # 1
            line.Draw()
            allstuff.append(line)
    #print('these lines ', lines)
    return lines

##########################################
def DrawSubTriangles(Lines, points, tid, level, nLevels):
    print('* level ', level)
    if level >= nLevels:
        return
    lines = DrawTriangle(points, nLevels, level, tid)
    Lines.append(lines)
    #print('  lines: ', len(lines))
    newSetsOfPoints = MakeThreeSetOfMidPoints(points)
    # print(newSetsOfPoints)
    tid = 0
    for newpoints in newSetsOfPoints:
        #print('got     ', newpoints)
        morelines = DrawSubTriangles(Lines, newpoints, tid, level+1, nLevels)
        tid = tid+1
        #for xline in morelines:
        #    Lines.append(xline)
        Lines.append(morelines)
    #print('Current lines', Lines)
    return Lines


##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
    

    canname = 'Sierpinski'
    cw, ch = 1550, 1200
    can = ROOT.TCanvas(canname, canname, 0, 0, cw, ch)
    cans.append(can)
    can.cd()
    #h2 = ROOT.TH2D('tmp', '', 100, 0, 1, 100, 0, 1)
    #h2.SetStats(0)
    #h2.Draw()
    #stuff.append(h2)
    
    nLevels = 8
    l = 1/sqrt(2.)
    delta = (1. - l)/2.
    Lines = []
    y0 = 0.04
    points = [ mypoint(delta, y0), mypoint(1.-delta, y0), mypoint(0.5, 1-y0)]
    GotLines = DrawSubTriangles(Lines, points, 0, 0, nLevels)    
    stuff.append(Lines)
    stuff.append(GotLines)
    #print(Lines)

    can.Update()
    can.Print(can.GetName() + '.png')
    can.Print(can.GetName() + '.pdf')
    ROOT.gApplication.Run()
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

