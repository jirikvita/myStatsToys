#!/usr/bin/python
#
# jk 12.11.2017
#
########################################

from __future__ import print_function
import os, sys, ROOT
from math import sqrt, tan, pow, pi, fabs, atan, cos, sin

########################################
# globals:
gdebug = 0
ROOT.gStyle.SetOptTitle(0)
mm = 1e-1
cm = 1.
MeV = 1.
gEmin = 0.*MeV
gEmax = 10.*MeV

# high granularity:
Nstepsx = 400
Nstepsy = Nstepsx/2
NstepsPhi = 256 #512

# small test:
#Nstepsx = 20
#Nstepsy = Nstepsx/2
#NstepsPhi = 12

# scale factor for radial range of points to be considered:
SFR = 1.2

## Nosek:
power = 3./2.
xi = 3.1*mm*pow(MeV, -power)

# Radek via G4:
#power = 1.7
#xi = 2.1*mm*pow(MeV, -power)

# JK random:
#power = 3./2
#xi = 3.1*mm*pow(MeV, -power)


E0 = 8*MeV
sigmaE = 0.02*MeV
Cans = []
Stuff = []
gSpectLine = ROOT.TF1('SpectLine', '[0]*( exp(-(x-[1])^2/(2*[2]^2)) + [3]*exp(-(x-[4])^2/(2*[5]^2)) ) ', gEmin, gEmax)
gSpectLine.SetNpx(400)

########################################
# defs:

def Init(E1, sigmaE1, frac, E2, sigmaE2):
    gSpectLine.SetParameters(1., E1, sigmaE1, frac, E2, sigmaE2)
    gSpectLine.DrawCopy()
    #ROOT.gApplication.Run()

def DeltaR(x1, y1, x2, y2):
    return sqrt( pow(x1-x2,2) + pow(y1-y2,2) )

class MyLine:
    def __init__(self,a,b,x,y,phi):
        self._a = a
        self._b = b
        self._x = x
        self._y = y
        self._phi = phi
    def a(): return self._a
    def b(): return self._b
    def x(): return self._x
    def y(): return self._y
    def phi(): return self._phi

    
def MakeLineParams(x,y,phi):
    # y = ax + b
    ap = tan(phi)
    bp = y - ap*x
    return MyLine(ap, bp, x, y, phi)

def FindIntercept(ray, detline):
    # ray: a, b: y=ax+b
    # detector line: x1, x2, y=const
    Y = detline[2]
    if gdebug > 2: print( 'pars: a={:f}, b={:f}, Y={:f}'.format(ray.a(), ray.b(), Y) )
    if fabs(ray._a) > 1.e-4:
        x = 1/ray._a*(Y - ray._b)
        return [x, Y]
    else:
        return [-2*infty, -2*infty]
    
def CheckIntercept(ray, detlines):
    intercept = []
    # check intercept with either of the ranges:
    for subdet in detlines:
        point = (FindIntercept(ray, subdet))
        if gdebug > 2: print ('        Intercept: {:f},{:f}'.format(point[0], point[1]) )
        # verify the x range of the intercept to be within the line range:
        if point[0] > subdet[0] and point[0] < subdet[1]:
            intercept.append(point)
    return intercept

def ComputeDistance(x0, y0, x1, y1):
    found = False
    R = DeltaR(x0, y0, x1, y1)
    return R
    return -1.

def PickE():
    return gSpectLine.GetRandom()

def ComputeXRange(E):
    return xi*pow(E, power)

def ComputeE(E, x):
    val = pow(E,power) - x/xi
    if val > 0.:
        return pow(val, 1/power)
    return -1.

def DrawE(hist, line):
    canname = 'AlphaSpectSim'
    can = ROOT.TCanvas(canname, canname, 0, 0, 1200, 800)
    Cans.append(can)
    hist.SetMarkerStyle(20)
    hist.SetMarkerColor(ROOT.kBlack)
    hist.SetMarkerSize(1)

    oldint = line.Integral(gEmin, gEmax)
    frac = line.GetParameter(3)
    sigma1 = line.GetParameter(2)
    sigma2 = line.GetParameter(5)
    # line.SetParameter(0, hist.Integral() / (1+frac) * (  1/(sqrt(2*pi)*sigma1) + frac/(sqrt(2*pi)*sigma2)  )  )
    # line.SetParameter(0, hist.GetMaximum() / (1+frac) * (  1/(sqrt(2*pi)*sigma1) + frac/(sqrt(2*pi)*sigma2)  )  )
    line.SetParameter(0, hist.GetMaximum() / line.GetMaximum() )

    #line.Draw()
    #hist.Draw('e1same')

    hist.Draw('e1')
    line.Draw('same')

    tag = '_nx{:}_ny{:}_nphi{:}'.format(Nstepsx, Nstepsy, NstepsPhi)
    can.Print(canname + tag + '.png')
    can.Print(canname + tag + '.pdf')
    return

def DrawLines(Range, lines, detcover, det, R = 0.2):
    canname = 'DecayPoints'
    can = ROOT.TCanvas(canname, canname, 1000, 1000, 1000, 1000)
    Cans.append(can)
    name = 'tmphist'
    SF = 1.4
    tmp = ROOT.TH2D(name, name, 100, -SF*Range, SF*Range, 100, -Range/10., SF*Range)
    tmp.SetStats(0)
    Stuff.append(tmp)
    tmp.Draw()
    gr = ROOT.TGraph()
    Stuff.append(gr)
    i = -1
    # show roughly every 1000th point:
    nl = len (lines)
    verbose = int(nl/831)
    ip = 0
    for line in lines:
        i = i+1
        if nl < 2500 or i % verbose == 0:
            x = line._x
            y = line._y
            gr.SetPoint(ip, x, y)
            ip = ip+1

    i  = -1
    if nl < 2500:
        for line in lines:
            i = i+1
            x = line._x
            y = line._y
            # y = ax+b
            t = 0.1
            phi = line._phi
            vect = ROOT.TLine(x, y, x+R*cos(phi), y+R*sin(phi))
            vect.SetLineColor(ROOT.kOrange)
            Stuff.append(vect)
            vect.Draw()
        
        
    gr.SetMarkerStyle(20)
    gr.SetMarkerColor(ROOT.kBlue)
    gr.SetMarkerSize(0.8)
    gr.Draw('P')

    DrawBorders(tmp, detcover, ROOT.kBlack)
    DrawBorders(tmp, det, ROOT.kRed)

    tag = '_nx{:}_ny{:}_nphi{:}'.format(Nstepsx, Nstepsy, NstepsPhi)
    can.Print(canname + tag + '.png')
    can.Print(canname + tag + '.pdf')
    
    return

def DrawBorders(tmp, dets, col):
    for det in dets:
        x1 = det[0]
        x2 = det[1]
        val = tmp.GetXaxis().GetXmin()
        if x1 < val: x1 = val
        val = tmp.GetXaxis().GetXmax()
        if x2 > val: x2 = val
        line = ROOT.TLine(x1, det[2], x2, det[2])
        line.SetLineColor(col)
        line.SetLineWidth(3)
        Stuff.append(line)
        line.Draw()


########################################
# Init:

infty = 1000.
# detector depth below cover:
DetDepth = 3*mm #cm
# slit/detector width:
DetWidth = 256*0.0551*mm # 256 pixels per 55mum

print( 'Detector parameters: a={:f} DetDepth={:f}'.format(DetWidth, DetDepth) )

# params in format: [x1, x2, y]:
detcover = [ [-infty, -DetWidth/2, DetDepth], [DetWidth/2, infty, DetDepth] ]
det = [ [-DetWidth/2, DetWidth/2, 0.] ]

Init(E0, sigmaE, 0.4, 0.65*E0, sigmaE)
name = 'AlphaSpectHist'
nbins = 200
Ehist = ROOT.TH1D( name, name, nbins, gEmin, gEmax)#, (E0+3*sigmaE)/MeV )

# generate a grid of x and y points, 
# start with a range of alpha particles, allow n*sigma fluctuation
Nsigmas = 5.
print ('Expected range for kinetic energy E={:f} MeV :: R={:f} cm'.format(E0, ComputeXRange(E0)) )
Range = ComputeXRange(E0) + Nsigmas*ComputeXRange(sigmaE)

# x; add a safety 2*a margin:
x0 = Range
stepx = 2*x0/Nstepsx
Xs = [ -x0 + i*stepx for i in range(0, Nstepsx) ]
if gdebug > 2: print(Xs)

# y; add a safety 2*a margin:
y0 = Range
stepy = y0/Nstepsy
Ys = [   DetDepth/10. + i*stepy for i in range(0, Nstepsy) ]
if gdebug > 2: print(Ys)

# angle goes from some small value to -pi
stepPhi = 2*pi/NstepsPhi
Phis = [ -pi+0.1 + i*stepPhi for i in range(0, NstepsPhi) ]
if gdebug > 2: print(Phis)

Lines = []

########################################
# Loops:

Niter = len(Phis)*len(Xs)*len(Ys)
print ('Expecting {:} steps!'.format(Niter) )
verbose = 100000
istep = -1
deltax = stepx/4.     
for phi in Phis:
    if gdebug > 1: print ( 'phi={:f}'.format(phi) )
    for y in Ys:
        if gdebug > 1: print ( '  x,y={:f},{:f}'.format(x,y) )
        deltax *= -1.
        for xx in Xs:
            if gdebug > 1: print ( '  x={:f}'.format(x) )
            x = xx + deltax
            istep = istep+1
            if istep % verbose == 0:
                print ('Processing iteration {:}/{:} [{:3.1f}%]'.format(istep, Niter, 100*istep*1./Niter) )
            
            # remove decay points not in the air:
            if (x < -DetWidth/2 or x > DetWidth/2) and y < DetDepth:
                continue
            # remove points outside the rough reach-sphere:
            if sqrt( pow(x,2) + pow(y,2) ) > SFR*Range:
                continue
            
            Egen = PickE()
            if gdebug > 2: print( '      Egen={:f}'.format(Egen) )
            line = MakeLineParams(x, y, phi)
            if gdebug > 5: print('Line params: ', line)
            Lines.append(line)
            intercepts = CheckIntercept(line, detcover)
            if gdebug > 2: print( '    cover: nintercepts={:}'.format(len(intercepts)) )
            if len(intercepts) > 0:
                continue
            intercepts = CheckIntercept(line, det)
            if gdebug > 2: print( '    detector: nintercepts={:}'.format(len(intercepts)) )
            if len(intercepts) < 1:
                continue
            range = ComputeDistance(x, y, intercepts[0][0], intercepts[0][1])
            if gdebug > 2: print( '    range={:f}'.format(range) )
            if range > 0.:
                Edet = ComputeE(Egen, range)
                if gdebug > 2: print( '      Edet={:f}'.format(Edet) )
                if Edet > 0:
                    Ehist.Fill(Edet/MeV)

print ('Done loops.')
########################################
# Draw and finish:

print ('Drawing...')
DrawE(Ehist, gSpectLine)
DrawLines(Range, Lines, detcover, det)

print ('All done!')

ROOT.gApplication.Run()

            
