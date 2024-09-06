#!/usr/bin/python

# was: #!/usr/bin/python3
# Po 19. srpna 2024, 17:50:37 CEST
# 5.9.2024

import ROOT
from math import sqrt, pow, log, exp
import os, sys, getopt
import random
from math import pow, log, exp, sqrt

from utils import *
from consts import *

cans = []
stuff = []


##########################################
class cworld():
    def __init__(self):
        self.can = None
        self.x0 = 0.02
        self.y0 = 0.5
        self.xscale = 0.0009
        self.yscale = 0.0014
        self.SFy = 0.3 # for separating particles in y for drawing; using rad./int. lengths
        self.deltaY = 0.7 # particles fork visual factor
        return
    
    def Draw(self):
        print('Drawing the world...')
        canname = 'ShowerVis'
        self.can = ROOT.TCanvas(canname, canname, 0, 0, 1200, 600)
        self.can.Draw()
        return self.can

##########################################
class cpart:
    
    def __init__(self, E, pid, x, y, yend, gen, interacted):
        self.E = E
        self.pid = pid
        self.x = x # position where born
        self.y = y # position where born
        self.xend = None # end position
        self.yend = yend # end position
        self.gen = gen # generation
        self.interacted = interacted
        
    def Draw(self, world, verbose = 0):
        if verbose:
            print(f'Drawing particle {self.pid} of generation {self.gen}...')
        xscale, yscale, x0, y0, SFy = world.xscale, world.yscale, world.x0, world.y0, world.SFy
        x1 = self.xend
        y1 = self.yend
        if x1 == None:
            # unterminated particle, possible end of shower
            x1 = self.x + gLength[self.pid]
        X1, Y1, X2, Y2 = x0 + xscale*self.x, y0 + yscale*self.y, x0 + xscale*x1, y0 + yscale*y1
        if verbose:
            print(f'   ...coors: {X1:1.3f}, {Y1:1.3f}, {X2:1.3f}, {Y2:1.3f}')
        line = ROOT.TLine(X1, Y1, X2, Y2)
        line.SetNDC()
        alpha =  0.8 * (world.genmax - self.gen ) / world.genmax + 0.1
        line.SetLineColorAlpha(gcol[self.pid], alpha)
        line.SetLineStyle(glst[self.pid])
        line.SetLineWidth(glwd[self.pid])
        #if verbose:
        #    print('...drawing...')
        line.Draw()
        return line
    

##########################################
#def ChooseNextInteractionPoint(part):
#    return x + gX0[part.pid]

##########################################
def splitParticle(world, part, randomizeY = 1, verbose = 0):
    if part.interacted:
        return []
    gen = part.gen
    y = part.yend
    pid = part.pid
    SFy = world.SFy
    rnd1 = 0.
    rnd2 = 0.

    deltaY = world.deltaY
    dy1, dy2, dy3, dy4 = deltaY, -deltaY, (1. - deltaY), -deltaY
    if randomizeY:
        rnd1 = random.random() / 2
        rnd2 = random.random() / 2
    if verbose:
        print(f' ...trying {part.pid}')
    if part.pid == 'e' and part.E > gECEM:
        if verbose:
            print('  ...performing brehms!')
        # new interaction position:
        x = part.x + gLength[part.pid]*log(2)
        E1 = part.E / 2. # TBF, to be randomized, swapped...
        E2 = part.E / 2. # TBF
        p1 = cpart(E1, 'gamma', x, y, y + (dy1 + rnd1)*SFy*gLength[pid], gen+1, False)
        p2 = cpart(E2, 'e',     x, y, y + (dy2 + rnd2)*SFy*gLength[pid], gen+1, False)
        part.xend = x # terminate the parent particle
        part.interacted = True
        return [p1, p2]
    elif part.pid == 'gamma' and part.E > gECpair:
        if verbose:
            print('  ...performing conversion!')
        x = part.x + gLength[part.pid]*log(2)
        E1 = part.E / 2. # TBF, to be randomized, swapped...
        E2 = part.E / 2. # TBF
        p1 = cpart(E1, 'e', x, y, y + (dy1 + rnd1)*SFy*gLength[pid], gen+1, False)
        p2 = cpart(E2, 'e', x, y, y + (dy2 + rnd2)*SFy*gLength[pid], gen+1, False) 
        part.xend = x # terminate the parent particle
        part.interacted = True
        return [p1, p2]
    elif part.pid == 'pi' and part.E > ECpiThr:
        x = part.x + gLength[part.pid]*log(2)
        if verbose:
            print('  ...performing pion production!')
        E1 = part.E / 3. # TBF, to be randomized, swapped...
        E2 = part.E / 3. # TBF
        E3 = part.E / 3. # TBF
        dy1, dy2 = (1. - deltaY), deltaY
        dy3, dy4 = -(1. - deltaY), -deltaY
        newps = []
        newps.append( cpart(E1, 'pi', x, y, y + (dy1 + rnd1)*SFy*gLength[pid], gen+1, False) )
        newps.append( cpart(E2, 'pi', x, y, y + (dy2 + rnd2)*SFy*gLength[pid], gen+1, False) )
        # p0 --> gamma gamma:
        rnd3 = 0.
        rnd4 = 0.
        if randomizeY:
            rnd3 = random.random() / 3
            rnd4 = random.random() / 3
        newps.append( cpart(E3/2, 'gamma', x, y, y + (dy3 + rnd3)*SFy*gLength[pid], gen+1, False) )
        newps.append( cpart(E3/2, 'gamma', x, y, y + (dy4 + rnd4)*SFy*gLength[pid], gen+1, False) )
        part.xend = x # terminate the parent particle
        part.interacted = True
        return newps
    if verbose:
        print('  ...nothing done!') #
    return []

##########################################
def PerformInteractionStep(world, particles, randomizeY, verbose = 0):
    newparticles = []
    for p in particles:
        if verbose:
            print(f'...making {p.pid} interact...')
        newparts = splitParticle(world, p, randomizeY)
        for newp in newparts:
            newparticles.append(newp)
    particles.extend(newparticles)
    return particles
    
##########################################
def Simulate(world, E0, randomizeY):
    particles = []

    primary = 'pi'
    #primary = 'e'
    #primary = 'gamma'

    gen0 = 0
    x, y = 0.*gkm, 0.*gm
    yend = 0*gm # dummy
    particles.append(cpart(E0, primary, x, y, yend, gen0, False))
    
    newnp = len(particles)
    np = -1
    istep = -1
    nMax = 1e8
    while newnp != np and np < nMax: # producing particles
        istep = istep + 1
        print(f'step: {istep} newnp: {newnp}')
        particles = PerformInteractionStep(world, particles, randomizeY)
        np = 1*newnp
        newnp = len(particles)
    return particles

##########################################
def DrawResults(world, particles):
    lines = []
    can = world.Draw()
    can.cd()
    print('Drawing particles...')
    for part in particles:
        line = part.Draw(world)
        #print('E: ', part.E)
        lines.append(line)
    return can, lines

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]
    
    gBatch = False

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('batch={:}'.format(gBatch))
 
    #E0 = 1.*gTeV #1e14*geV
    E0 = 100*gTeV #1e14*geV
    # randomizeY = True
    randomizeY = False
 
    ROOT.gStyle.SetOptTitle(0)
    
    world = cworld()
    particles = Simulate(world, E0, randomizeY)
    world.genmax = getMaxGen(particles)
    can, lines = DrawResults(world, particles)


    print(f'Drawn lines: {len(lines)}')
    primary = particles[0]
    # draw label
    txt = ROOT.TLatex(0.05, 0.95, 'Primary {} E={:1.1f} TeV'.format(glabel[primary.pid], E0/1000.))
    txt.SetNDC()
    txt.Draw()

    jmax,maxx = getMaxX(particles)
    last = particles[jmax]
    
    # fill histogrammes
    hname = 'h1Nx'
    htitle = ';x[g/cm^{2}];N'
    nb = 40
    x1 = 0
    x2 = last.x*1.25
    print('x1, x2: ', x1, x2)
    h1Nx = ROOT.TH1D(hname, htitle, nb, x1, x2)
    for part in particles:
        #if part.xend != None and part.x != None:
        #    h1Nx.Fill( 0.5*(part.xend - part.x) )
        #elif part.x != None:
        h1Nx.Fill(part.x)

    canname = 'AirStats'
    statcan = ROOT.TCanvas(canname, canname, 1225, 0, 700, 600)
    statcan.cd()
    h1Nx.Draw('hist')
    
    stuff.append(txt)
    can.Update()

    tag = '_{}_E{:1.0f}GeV'.format(primary.pid, E0)
    can.Print(can.GetName() + tag + '.pdf')
    can.Print(can.GetName() + tag + '.png')

    statcan.Print(statcan.GetName() + tag + '.pdf')
    statcan.Print(statcan.GetName() + tag + '.png')

    stuff.append([can, statcan, lines])

    print('DONE!')
    
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

