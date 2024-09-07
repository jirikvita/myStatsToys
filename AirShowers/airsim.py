#!/usr/bin/python

# was: #!/usr/bin/python3
# Po 19. srpna 2024, 17:50:37 CEST
# 5.9.2024

# TODO
# enable possibility of separate particle histograms
# decay pions to muons
# add neutrinos?
# finish Xmax error in plotting

import ROOT

from math import sqrt, pow, log, exp
import os, sys, getopt
import random
from math import pow, log, exp, sqrt
from numpy.random import exponential as exponential
    
from utils import *
from consts import *

cans = []
stuff = []


##########################################
class cworld():
    def __init__(self):
        self.can = None
        self.x0 = 0.0
        self.y0 = 0.
        self.xscale = 0.00015
        self.yscale = 0.0035
        self.SFy = 0.3    # for separating particles in y for drawing; using rad./int. lengths
        self.deltaY = 0.7 # particles fork visual factor
        self.rndSF = 4.   # SF for random number division in vertical split

        self.x1, self.x2 = 0., 4000. #g/cm2  #self.xscale*50

        return
    
    def Draw(self):
        print('Drawing the world...')
        canname = 'ShowerVis'
        self.can = ROOT.TCanvas(canname, canname, 0, 0, 1200, 600)
        self.can.Draw()
        self.can.cd()
        
        ny = 5
        nb = 1000
        y1, y2 = -100, 100
        self.h2 = ROOT.TH2D("worldhisto", ";x[g/cm^{2}];y[arb.];", nb, self.x1, self.x2, nb, y1, y2)
        self.h2.SetStats(0)
        self.h2.GetYaxis().SetAxisColor(ROOT.kWhite)
        self.h2.GetYaxis().SetLabelColor(ROOT.kWhite)
        self.h2.GetYaxis().SetTitleColor(ROOT.kWhite)

        self.h2.Draw()
        return self.can, self.h2

##########################################
class cpart:
    
    def __init__(self, E, pid, x, y, yend, gen): #, interacted):
        self.E = E
        self.pid = pid
        self.x = x # position where born
        self.y = y # position where born
        self.xend = None # end position
        self.yend = yend # end position
        self.gen = gen # generation
        #self.interacted = interacted
        
    def Draw(self, world, halfSteps, verbose = 0):
        if verbose:
            print(f'Drawing particle {self.pid} of generation {self.gen}...')
        xscale, yscale, x0, y0, SFy = world.xscale, world.yscale, world.x0, world.y0, world.SFy
        x1 = self.xend
        y1 = self.yend
        if x1 == None:
            # unterminated particle, possible end of shower
            if halfSteps:
                x1 = self.x + gLength[self.pid]
            else:
                x1 = self.x + exponential(gLength[self.pid])

        #X1, Y1, X2, Y2 = x0 + xscale*self.x, y0 + yscale*self.y, x0 + xscale*x1, y0 + yscale*y1
        X1, Y1, X2, Y2 = x0 + self.x, y0 + self.y, x0 + x1, y0 + y1
        if verbose:
            print(f'   ...coors: {X1:1.3f}, {Y1:1.3f}, {X2:1.3f}, {Y2:1.3f}')
        line = ROOT.TLine(X1, Y1, X2, Y2)
        #line.SetNDC()
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
def splitParticle(world, part, randomizeY, halfSteps, verbose = 0):
    if part.pid == 'mu' or part.pid == 'nu':
        return []
    gen = part.gen
    y = part.yend
    pid = part.pid
    length = gLength[part.pid]
    
    SFy = world.SFy
    rnd1 = 0.
    rnd2 = 0.
    rndSF = world.rndSF
    
    deltaY = world.deltaY
    dy1, dy2, dy3, dy4 = deltaY, -deltaY, (1. - deltaY), -deltaY
    if randomizeY:
        dy1, dy2, dy3, dy4 = 0, 0, 0, 0
        rnd1 = getRndSign()*random.random() / rndSF
        rnd2 = -rnd1
    if verbose:
        print(f' ...trying {part.pid}')

    # Electrons:
    if part.pid == 'e' and part.E > gECEM:
        if verbose:
            print('  ...performing brehms!')
        # new interaction position:
        xi = 0.5
        if halfSteps:
            x = part.x + length*log(2)
        else:
            dx = exponential(length)
            x = part.x + dx
            xi = exp(-dx / length)
        E1 = xi*part.E
        E2 = (1-xi)*part.E
        p1 = cpart(E1, 'gamma', x, y, y + (dy1 + rnd1)*SFy*length, gen+1) #, False)
        p2 = cpart(E2, 'e',     x, y, y + (dy2 + rnd2)*SFy*length, gen+1) #, False)
        part.xend = x # terminate the parent particle
        #part.interacted = True
        return [p1, p2]

    # Photons
    elif part.pid == 'gamma' and part.E > gECpair:
        if verbose:
            print('  ...performing conversion!')
        xi = 0.5
        if halfSteps:
            x = part.x + length*log(2)
        else:
            dx = exponential(length)
            x = part.x + dx
            xi = exp(-dx / length)
            # TODO: xi as a random number drawn from distribution
            # C*(1 - 4/3*x*(1-x)), C = 9/7?
            # TF1 b("b", "9./7.5*(1 - 4/3*x*(1-x))", 0, 1);

        E1 = xi*part.E
        E2 = (1-xi)*part.E
        p1 = cpart(E1, 'e', x, y, y + (dy1 + rnd1)*SFy*length, gen+1) #, False)
        p2 = cpart(E2, 'e', x, y, y + (dy2 + rnd2)*SFy*length, gen+1) #, False) 
        part.xend = x # terminate the parent particle
        #part.interacted = True
        return [p1, p2]
    elif part.pid == 'pi':
        if part.E < ECpiThr:
            # decay the pion to a muon
            # less transverse separation
            rnd1 = getRndSign()*random.random() / rndSF / rndSF
            rnd2 = -rnd1
            gamma = part.E / gmass[part.pid]
            length = gamma*gctau[part.pid]
            dx = exponential(length)
            x = part.x + dx
            if x > world.x2:
                x = world.x2
            xi = exp(-dx / length)
            E1 = xi*part.E
            E2 = (1-xi)*part.E
            p1 = cpart(E1, 'mu', x, y, y + (dy1 + rnd1)*SFy*length, gen+1) #, False)
            p2 = cpart(E2, 'nu',     x, y, y + (dy2 + rnd2)*SFy*length, gen+1) #, False)
            # terminate muons and neutrinos:
            p1.xend = world.x2
            p2.xend = world.x2
            
            part.xend = x # terminate the parent particle
            #part.interacted = True
            return [p1, p2]
            
        else:
            xi = 1/3.
            chi = 0.
            if halfSteps:
                x = part.x + length*log(2)
            else:
                dx = exponential(length)
                xi = exp(-dx / length)
                x = part.x + dx
                chi = 2.
                while 1 - xi - chi < 0.:
                    chi = random.random()
            if verbose:
                print('  ...performing pion production!')
            E1 = xi*part.E
            E2 = (1-xi-chi)*part.E
            E3 = (1-xi+chi)*part.E
            #dy1, dy2 = (1. - deltaY), deltaY
            #dy3, dy4 = -(1. - deltaY), -deltaY
            dy3, dy4 = 0, 0
            newps = []
            rnd3 = 0.
            rnd4 = 0.
            if randomizeY:
                rnd3 = getRndSign()*random.random() / rndSF
                rnd4 = -rnd4

            newps.append( cpart(E1, 'pi', x, y, y + (dy1 + rnd1)*SFy*length, gen+1) ) #, False) )
            newps.append( cpart(E2, 'pi', x, y, y + (dy2 + rnd2)*SFy*length, gen+1) )  #, False) )
            # p0 --> gamma gamma:
            zeta = random.random()
            # TODO: zeta as a random number drawn from distribution
            # C*(1 - 4/3*x*(1-x)), C = 9/7?
            newps.append( cpart(zeta*E3, 'gamma', x, y, y + (dy3 + rnd3)*SFy*length, gen+1) ) #, False) )
            newps.append( cpart((1-zeta)*E3, 'gamma', x, y, y + (dy4 + rnd4)*SFy*length, gen+1) )  #, False) )
            part.xend = x # terminate the parent particle
            #part.interacted = True
            return newps
    if verbose:
        print('  ...nothing done!') #
    return []

##########################################
def PerformInteractionStep(world, particles, randomizeY, halfSteps, verbose = 0):
    newparticles = []
    for p in particles:
        if verbose:
            print(f'...making {p.pid} interact...')
        newparts = splitParticle(world, p, randomizeY, halfSteps)
        for newp in newparts:
            newparticles.append(newp)
    return newparticles
    
##########################################
def Simulate(primaryPID, world, E0, randomizeY, halfSteps):

    gen0 = 0
    x, y = 0.*gkm, 0.*gm
    yend = 0*gm # dummy

    newparticles = []
    newparticles.append(cpart(E0, primaryPID, x, y, yend, gen0)) # False
    
    np = -1
    istep = -1
    nMax = 1e8

    allparticles = []
    while len(newparticles) > 0 and len(allparticles) < nMax: # producing particles
        istep = istep + 1
        print(f'step: {istep:3} | total particles count: {len(allparticles):11,} | new particles: {len(newparticles):11,}')
        todoparticles = PerformInteractionStep(world, newparticles, randomizeY, halfSteps)
        allparticles.extend(newparticles)
        newparticles = todoparticles
    return allparticles

##########################################
def DrawResults(world, particles, halfSteps):
    lines = []
    can, h2 = world.Draw()
    can.cd()
    print('Drawing particles...')
    h2.Draw()
    drawn = 0
    Ncut = 2e6
    NmaxDraw = 4e6 # must be bigger than Ncut!
    drawFrac = 0.1
    partialDraw = len(particles) > Ncut
    ipart = 0
    for part in particles:
        ipart = ipart + 1
        if (ipart-1) % 1000000 == 0 and ipart > 0:
            print(f'{ipart-1:10,} / {len(particles):10,}; drawn: {drawn:10,}')
        if drawn < NmaxDraw:
            if drawn < Ncut or (drawn >= Ncut and random.random() < drawFrac):
                line = part.Draw(world, halfSteps)
                drawn = drawn + 1
                #print('E: ', part.E)
                lines.append(line)
    return can, h2, lines, partialDraw

##########################################

def processArgs(argv):

    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print(f'Usage: {argv[0]} [E(GeV)=100GeV] [iteration=0] [batch=0] [draw=1]')
        return -1, 0, 0, 0

    print(f'*** Running {sys.argv[0]}')
    E = 300 # GeV
    if len(sys.argv) > 1:
        Ereq = int(sys.argv[1])
        if Ereq <= 1000000 and Ereq >= 30:
            print(f'Using custom energy E={Ereq} GeV')
            E = Ereq
        else:
            print(f'Wrong custom energy E={Ereq} GeV, using default E={E} GeV')

    iteration = 0
    if len(sys.argv) > 2:
        req_iteration = int(sys.argv[2])
        if req_iteration >= 0 and req_iteration < 1000:
            print(f'OK, using user-define iteration  {req_iteration}')
            iteration = req_iteration

    gBatch = False
    if len(sys.argv) > 3:
        reqBatch = int(sys.argv[3])
        if reqBatch > 0:
            print(f'OK, using user-define batch mode {reqBatch}')
            gBatch = True
        
    if gBatch:
        ROOT.gROOT.SetBatch(1)

    doDraw = True
    if len(sys.argv) > 4:
        reqDraw = int(sys.argv[4])
        if reqDraw == 0:
            print(f'OK, using user-define draw mode  {reqDraw}')
            doDraw = reqDraw
        
    print('*** Settings:')
    print('batch={:}'.format(gBatch))

    return E,iteration,gBatch,doDraw 

##########################################
def makeTags(primary, E0, iteration):
    tag = '_{}_E{:1.0f}GeV'.format(primary.pid, E0)
    rtag = tag + ''
    tag = tag + '_iter{}'.format(iteration)
    gtag = tag + ''

    ropt = 'recreate'
    if iteration > 0:
        ropt = 'update'
    return tag, rtag, gtag, ropt

##########################################
def makeOutHistos(last, iteration, rtag, ropt, rootdir = 'root/'):
    hname = f'h1Nx_{iteration}'
    htitle = ';x[g/cm^{2}];N'
    nb = 40
    x1 = 0
    x2 = last.x*1.25
    #print('x1, x2: ', x1, x2)
    outfile = ROOT.TFile(rootdir + 'histos' + rtag + '.root', ropt)   
    h1Nx = ROOT.TH1D(hname, htitle, nb, x1, x2)
    return outfile, h1Nx

#########################################
def doAllDrawing(world, primary, E0, particles, halfSteps, tag, gtag, h1Nx):
        can, h2, lines, partialDraw = DrawResults(world, particles, halfSteps)
        if partialDraw:
            gtag = gtag + '_partialDraw'
        print(f'Drawn lines: {len(lines):10,}')
        # draw label
        txt = ROOT.TLatex(0.02, 0.95, 'Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M, depth={:1.0f}'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6, world.genmax))
        txt.SetTextColor(ROOT.kWhite)
        txt.SetNDC()
        txt.Draw()

        ptxt = makePtctLabels(0.875, 0.855, 0.041)
        stuff.append(ptxt)
        
        can.Update()
        
        canname = 'AirStats'
        statcan = ROOT.TCanvas(canname, canname, 1225, 0, 700, 600)
        statcan.cd()
        h1Nx.SetLineColor(ROOT.kGreen)
        h1Nx.Draw('hist')
        h1Nx.GetYaxis().SetAxisColor(ROOT.kWhite)
        h1Nx.GetYaxis().SetLabelColor(ROOT.kWhite)
        h1Nx.GetYaxis().SetTitleColor(ROOT.kWhite)
        stuff.append(txt)
        statcan.Update()

        print('Printing to png and pdf...')
        pngdir = 'png/'
        pdfdir = 'pdf/'

        #can.Print(pdfdir + can.GetName() + gtag + '.pdf')
        can.Print(pngdir + can.GetName() + gtag + '.png')

        statcan.Print(pdfdir + statcan.GetName() + tag + '.pdf')
        statcan.Print(pngdir + statcan.GetName() + tag + '.png')

        stuff.append([can, h2, statcan, lines, txt])

        print('DONE!')
        return can, h2, lines, partialDraw, statcan, txt


##########################################
def spitSomeInfo(primary, E0, particles, world):
    print('Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M, depth={:1.0f}'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6, world.genmax))

##########################################
##########################################
##########################################

def main(argv):

    dirs = ['png', 'pdf', 'root']
    for dir in dirs:
        os.system(f'mkdir -p {dir}')
    
    E,iteration,gBatch,doDraw = processArgs(argv)
    if E < 0:
        return 1

    # Primary particle energy!
    E0 = E*gGeV #1e14*geV
    primaryPID = 'pi'
    #primaryPID = 'e'
    #primaryPID = 'gamma'
    randomizeY = True
    halfSteps = False

    ROOT.gStyle.SetOptTitle(0)
    SetMyStyle()
    world = cworld()

    # Simulate!
    particles = Simulate(primaryPID, world, E0, randomizeY, halfSteps)

    # get/make some stuff needed
    world.genmax = getMaxGen(particles)
    primary      = particles[0]
    jmax,maxx    = getMaxX(particles)
    last         = particles[jmax]    
    tag, rtag, gtag, ropt = makeTags(primary, E0, iteration)

    # fill histogrammes
    outfile, h1Nx = makeOutHistos(last, iteration, rtag, ropt)
    for part in particles:
        if part.pid != 'mu' and part.pid != 'nu':
            h1Nx.Fill(part.x - primary.xend)

    spitSomeInfo(primary, E0, particles, world)
    if doDraw:
        can, h2, lines, partialDraw, statcan, txt = doAllDrawing(world, primary, E0, particles, halfSteps, tag, gtag, h1Nx)
        stuff.append([can, h2, lines, partialDraw, statcan, txt])
    
    outfile.Write()
    
    if doDraw and not gBatch:
        ROOT.gApplication.Run()
    
    outfile.Close()
    
    print(f'...Thanks for running {sys.argv[0]}')
    print('...Returning and kiling oneself!')
    print('...So long, and thanks for all the fish!')
    os.system('killall -9 airsim.py')
    return 0

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

