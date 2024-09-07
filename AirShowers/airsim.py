#!/usr/bin/python

# was: #!/usr/bin/python3
# Po 19. srpna 2024, 17:50:37 CEST
# 5.9.2024

# TODO
# decay pions to muons
# add neutrinos?
# finish Xmax error in plotting
# squeeze the particles in y, using the rnds sum

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
        self.x0 = 0.02
        self.y0 = 0.5
        self.xscale = 0.00015
        self.yscale = 0.0035
        self.SFy = 0.3 # for separating particles in y for drawing; using rad./int. lengths
        self.deltaY = 0.7 # particles fork visual factor
        self.rndSF = 4. # SF for random number division in vertical split
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
def splitParticle(world, part, randomizeY, halfSteps, verbose = 0):
    if part.interacted:
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
        #rnd1 = 1
        #while abs(rnd1 + rnd2) > 0.01:
        #    rnd1 = getRndSign()*random.random() / rndSF
        #    rnd2 = getRndSign()*random.random() / rndSF
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
        p1 = cpart(E1, 'gamma', x, y, y + (dy1 + rnd1)*SFy*gLength[pid], gen+1, False)
        p2 = cpart(E2, 'e',     x, y, y + (dy2 + rnd2)*SFy*gLength[pid], gen+1, False)
        part.xend = x # terminate the parent particle
        part.interacted = True
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
        p1 = cpart(E1, 'e', x, y, y + (dy1 + rnd1)*SFy*gLength[pid], gen+1, False)
        p2 = cpart(E2, 'e', x, y, y + (dy2 + rnd2)*SFy*gLength[pid], gen+1, False) 
        part.xend = x # terminate the parent particle
        part.interacted = True
        return [p1, p2]
    elif part.pid == 'pi' and part.E > ECpiThr:
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
            #while abs(rnd1 + rnd2 + rnd3 + rnd4) > 0.01:
            #    rnd1 = getRndSign()*random.random() / rndSF
            #    rnd2 = getRndSign()*random.random() / rndSF
            #    rnd3 = getRndSign()*random.random() / rndSF
            #    rnd4 = getRndSign()*random.random() / rndSF
            rnd3 = getRndSign()*random.random() / rndSF
            rnd4 = -rnd4

        newps.append( cpart(E1, 'pi', x, y, y + (dy1 + rnd1)*SFy*gLength[pid], gen+1, False) )
        newps.append( cpart(E2, 'pi', x, y, y + (dy2 + rnd2)*SFy*gLength[pid], gen+1, False) )
        # p0 --> gamma gamma:
        zeta = random.random()
        # TODO: zeta as a random number drawn from distribution
        # C*(1 - 4/3*x*(1-x)), C = 9/7?
        newps.append( cpart(zeta*E3, 'gamma', x, y, y + (dy3 + rnd3)*SFy*gLength[pid], gen+1, False) )
        newps.append( cpart((1-zeta)*E3, 'gamma', x, y, y + (dy4 + rnd4)*SFy*gLength[pid], gen+1, False) )
        part.xend = x # terminate the parent particle
        part.interacted = True
        return newps
    if verbose:
        print('  ...nothing done!') #
    return []

##########################################
def PerformInteractionStep(world, particles, randomizeY, halfSteps, verbose = 0):
    newparticles = []
    #allparticles = []
    for p in particles:
        if verbose:
            print(f'...making {p.pid} interact...')
        newparts = splitParticle(world, p, randomizeY, halfSteps)
        for newp in newparts:
            newparticles.append(newp)
    particles.extend(newparticles)
    return particles
    # return newparticles
    
##########################################
def Simulate(world, E0, randomizeY, halfSteps):
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
        print(f'step: {istep:3} actual particles count: {newnp:10,}')
        particles = PerformInteractionStep(world, particles, randomizeY, halfSteps)
        np = 1*newnp
        newnp = len(particles)
    return particles

##########################################
def DrawResults(world, particles, halfSteps):
    lines = []
    can = world.Draw()
    can.cd()
    print('Drawing particles...')
    drawn = 0
    Ncut = 2e6
    NmaxDraw = 4e6 # must be bigger than Ncut!
    drawFrac = 0.1
    partialDraw = len(particles) > Ncut
    ipart = 0
    for part in particles:
        ipart = ipart + 1
        if ipart % 1000000 == 0:
            print(f'{ipart:10,} / {len(particles):10,}, drawn: {drawn:10,}')
        if drawn < NmaxDraw:
            if drawn < Ncut or (drawn >= Ncut and random.random() < drawFrac):
                line = part.Draw(world, halfSteps)
                drawn = drawn + 1
                #print('E: ', part.E)
                lines.append(line)
    return can, lines, partialDraw

##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #  foo = sys.argv[1]

    E = 100 # GeV
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
            print(f'OK, using user-define iteration {req_iteration}')
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
            print(f'OK, using user-define draw mode {reqDraw}')
            doDraw = reqDraw
        
        
    print('*** Settings:')
    print('batch={:}'.format(gBatch))

    ##############################
    ##############################
    ##############################
    E0 = E*gGeV #1e14*geV
    randomizeY = True
    #randomizeY = False
    halfSteps = False
    ROOT.gStyle.SetOptTitle(0)
    
    world = cworld()
    particles = Simulate(world, E0, randomizeY, halfSteps)
    world.genmax = getMaxGen(particles)
    primary = particles[0]

    jmax,maxx = getMaxX(particles)
    last = particles[jmax]
    
    # fill histogrammes
    tag = '_{}_E{:1.0f}GeV'.format(primary.pid, E0)
    rtag = tag + ''
    tag = tag + '_iter{}'.format(iteration)
    gtag = tag + ''

    ropt = 'recreate'
    if iteration > 0:
        ropt = 'update'

    hname = f'h1Nx_{iteration}'
    htitle = ';x[g/cm^{2}];N'
    nb = 40
    x1 = 0
    x2 = last.x*1.25
    #print('x1, x2: ', x1, x2)
    outfile = ROOT.TFile('histos' + rtag + '.root', ropt)   
    h1Nx = ROOT.TH1D(hname, htitle, nb, x1, x2)
    for part in particles:
        #if part.xend != None and part.x != None:
        #    h1Nx.Fill( 0.5*(part.xend - part.x) )
        #elif part.x != None:
        h1Nx.Fill(part.x - primary.xend)

    print('Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M, depth={:1.0f}'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6, world.genmax))
    if doDraw:
        can, lines, partialDraw = DrawResults(world, particles, halfSteps)
        if partialDraw:
            gtag = gtag + '_partialDraw'
        print(f'Drawn lines: {len(lines):10,}')
        # draw label
        txt = ROOT.TLatex(0.05, 0.95, 'Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M, depth={:1.0f}'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6, world.genmax))
        txt.SetNDC()
        txt.Draw()

        canname = 'AirStats'
        statcan = ROOT.TCanvas(canname, canname, 1225, 0, 700, 600)
        statcan.cd()
        h1Nx.Draw('hist')

        stuff.append(txt)
        can.Update()

        print('Printing to png and pdf...')
        can.Print(can.GetName() + gtag + '.pdf')
        can.Print(can.GetName() + gtag + '.png')

        statcan.Print(statcan.GetName() + tag + '.pdf')
        statcan.Print(statcan.GetName() + tag + '.png')

        stuff.append([can, statcan, lines])

        print('DONE!')

    
    outfile.Write()
    outfile.Close()

    if doDraw and not gBatch:
        ROOT.gApplication.Run()

    
    print('...returning and kiling oneself!')
    os.system('killall -9 airsim.py')
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

