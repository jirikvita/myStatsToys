#!/usr/bin/python

# was: #!/usr/bin/python3
# Po 19. srpna 2024, 17:50:37 CEST
# 5.9.2024

# TODO
# enable possibility of separate particle histograms
# ...and no to keep particles in memory!
# finish Xmax unc. in plotting

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
        #self.xscale = 0.00015
        #self.yscale = 0.0035

        self.SFy = 0.3    # for separating particles in y for drawing; using rad./int. lengths
        self.gammaySF = 8.
        self.elySF = 0.3
        self.piySF = 0.08
        self.deltaY = 0.7 # particles fork visual factor

        self.x1, self.x2 = 0., 4000. #g/cm2  #self.xscale*50
        DY = 1.
        self.y1, self.y2 = -DY, DY
                
        self.maxgen = 0
        self.steps = 0

        self.Tunables = tunables()
        return
    
    #def UpdateMaxGen(self):
    #    self.maxgen = self.maxgen + 1
    
    def Draw(self):
        print('Drawing the world...')
        canname = 'ShowerVis'
        self.can = ROOT.TCanvas(canname, canname, 0, 0, 1200, 600)
        self.can.Draw()
        self.can.cd()
        
        ny = 5
        nb = 1000
        self.h2 = ROOT.TH2D("worldhisto", ";x[g/cm^{2}];y[arb.];", nb, self.x1, self.x2, nb, self.y1, self.y2)
        self.h2.SetStats(0)
        self.h2.GetYaxis().SetAxisColor(ROOT.kWhite)
        self.h2.GetYaxis().SetLabelColor(ROOT.kWhite)
        self.h2.GetYaxis().SetTitleColor(ROOT.kWhite)

        self.h2.Draw()
        return self.can, self.h2

    ##########################################
    def makeOutHistos(self, iteration, rtag, ropt, rootdir = 'root/'):
        hname = f'h1Nx_{iteration}'
        htitle = ';x[g/cm^{2}];N'
        nb = 200
        x1 = 0
        x2 = 4000. # g/cm^2 #last.x*1.25
        os.system(f'mkdir -p {rootdir}')
        self.outfile = ROOT.TFile(rootdir + 'histos' + rtag + '_tmp.root', ropt)   
        self.h1Nx = ROOT.TH1D(hname, htitle, nb, x1, x2)

        E1, E2 = 20*gGeV, 1e6*gGeV
        n1, n2 = 0, 50
        hname, htitle = 'Nhad0vsE', ';E[GeV];N_{had}'
        self.h1NhadE = ROOT.TH2D(hname, htitle, nb, E1, E2, nb, n1, n2)
        hname, htitle = 'Nch0vsE', ';E[GeV];N_{ch}'
        self.h1NchE = ROOT.TH2D(hname, htitle, nb, E1, E2, nb, n1, n2)
        hname, htitle = 'Npi0vsE', ';E[GeV];N_{#pi0}'
        self.h1Npi0E = ROOT.TH2D(hname, htitle, nb, E1, E2, nb, n1, n2)
        hname, htitle = 'NpvsE', ';E[GeV];N_{p}'
        self.h1NpE = ROOT.TH2D(hname, htitle, nb, E1, E2, nb, n1, n2)

##########################################
class cpart:
    
    def __init__(self, E, pid, x, y, yend): #, interacted):
        self.E = E
        self.pid = pid
        self.x = x # position where born
        self.y = y # position where born
        self.xend = None # end position
        self.yend = yend # end position
        #self.gen = gen # generation
        #self.interacted = interacted
        
##########################################

def DrawParticle(part, world, halfSteps, verbose = 0):
    if verbose:
        print(f'Drawing particle {part.pid} of generation {part.gen}...')
    x0, y0, SFy = world.x0, world.y0, world.SFy
    x1 = part.xend
    y1 = part.yend
    if x1 == None:
        # unterminated particle, possible end of shower
        if halfSteps:
            x1 = min(part.x + gLength[part.pid], world.x2)
        else:
            x1 = min(part.x + exponential(gLength[part.pid]), world.x2)

    #X1, Y1, X2, Y2 = x0 + xscale*part.x, y0 + yscale*part.y, x0 + xscale*x1, y0 + yscale*y1
    X1, Y1, X2, Y2 = x0 + part.x, y0 + part.y, x0 + x1, y0 + y1
    if verbose:
        print(f'   ...coors: {X1:1.3f}, {Y1:1.3f}, {X2:1.3f}, {Y2:1.3f}')
    line = ROOT.TLine(X1, Y1, X2, Y2)
    #line.SetNDC()
    alpha =  0.2 # * (world.maxgen - part.gen ) / world.maxgen + 0.1
    line.SetLineColorAlpha(gcol[part.pid], alpha)
    line.SetLineStyle(glst[part.pid])
    line.SetLineWidth(glwd[part.pid])
    #if verbose:
    #    print('...drawing...')
    line.Draw()
    return line


##########################################
#def ChooseNextInteractionPoint(part):
#    return x + gX0[part.pid]

##########################################

def genPions(pid, E, gamma, length, x, y, world):
    SFy, gammaySF, piySF = world.SFy, world.gammaySF, world.piySF
    # gen pions and actuially also gammas from pi0 decay;)
    pions = []
    # TODO: make some of these protons, actually, too?
    nCharged = int(world.Tunables.PionsConst*pow(E/gGeV, world.Tunables.PionsExp)) # 10 # can be randomized say between 6 and 12
    PiZeroFrac = chooseFrom (1/4., 1/3.)
    nNeutral = int( PiZeroFrac*nCharged / (1. - PiZeroFrac)  ) 
    ECh = E*(1. - PiZeroFrac)
    ENeutral = E*PiZeroFrac
    #print('PiZeroFrac , nCharged, nNeutral: ',  PiZeroFrac , nCharged, nNeutral)

    world.h1NhadE.Fill(E, nCharged + nNeutral)
    world.h1NchE.Fill(E, nCharged)
    world.h1Npi0E.Fill(E, nNeutral)
    
    # make some additinal protons, addition to the leading one already done before
    protonsToMake = 0
    if pid != 'pi':
        protonsToMake = 1
    for ipi in range(0, nCharged):
        newpid = 'pi'
        if protonsToMake > 0:
            newpid = 'p'
            protonsToMake = protonsToMake - 1
        Epi = ECh / nCharged # to randomize later
        #print('Epi ch.', Epi)
        yrnd = getRndSign()*random.random() / gamma
        pions.append( cpart(Epi, newpid, x, y, y + yrnd*SFy*length*piySF) )

    world.h1NpE.Fill(E, protonsToMake + 1)

    # and now pi0 --> gamma gamma:
    for ipi in range(0, nNeutral ):
        Epi = ENeutral / nNeutral # to randmize later
        #print('Epi neutr.', Epi)
        yrnd = getRndSign()*random.random() / gamma
        zeta = random.random()
        # TODO: zeta as a random number drawn from the lab photons energy distribution?
        pions.append( cpart(    zeta*Epi, 'gamma', x, y, y + yrnd*SFy*length / gammaySF) )
        pions.append( cpart((1-zeta)*Epi, 'gamma', x, y, y - yrnd*SFy*length / gammaySF) )

    return pions

##########################################
def twoParticleDecay(part, gamma, world, dy1, rnd1, dy2, rnd2, addSFy):
    SFy = world.SFy * addSFy
    # decay the pion to a muon
    # less transverse separation
    rnd1 = getRndSign()*random.random() / gamma
    rnd2 = -rnd1

    length = gamma*gctau[part.pid]
    dx = exponential(length)
    y = part.y
    x = min(part.x + dx, world.x2)
    xi = exp(-dx / length)
    E1 = xi*part.E
    E2 = (1-xi)*part.E
    #SFpid = 1.
    if part.pid == 'mu':
        # hack the y of muons to be smaller, like pions
        length = gLength['pi']
    p1 = cpart(E1, gdaughters[part.pid][0], x, y, y + (dy1 + rnd1)*SFy*length)
    p2 = cpart(E2, gdaughters[part.pid][1], x, y, y + (dy2 + rnd2)*SFy*length)
    
    return [p1, p2], x

##########################################
def splitParticle(world, part, randomizeY, halfSteps, verbose = 0):
    if (not world.decayMuons and part.pid == 'mu') or part.pid == 'nu':
        return []
    if part.x >= world.x2*(1 - gEpsilon):
        return []
    y = part.yend
    pid = part.pid
    length = gLength[part.pid]
    gammaySF = world.gammaySF
    elySF = world.elySF
    
    gamma = 1
    if gmass[pid] > gEpsilon:
        gamma = part.E / gmass[pid]
    else:
        gamma = part.E / gmass['e'] * gammaySF
    
    SFy = world.SFy
    rnd1 = 0.
    rnd2 = 0.
    addSFy = 0.1

    deltaY = world.deltaY
    dy1, dy2, dy3, dy4 = deltaY, -deltaY, (1. - deltaY), -deltaY
    if randomizeY:
        dy1, dy2, dy3, dy4 = 0, 0, 0, 0
        rnd1 = getRndSign()*random.random()
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
            x = min(part.x + dx, world.x2)
            xi = exp(-dx / length)
        E1 = xi*part.E
        E2 = (1-xi)*part.E
        p1 = cpart(E1, 'gamma', x, y, y + (dy1 + rnd1)*SFy*length / gamma )
        p2 = cpart(E2, 'e',     x, y, y + (dy2 + rnd2)*SFy*length / gamma * elySF)
        part.xend = x # terminate the parent particle
        #part.interacted = True
        #world.UpdateMaxGen()
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
            if x > world.x2:
                x = world.x2
            xi = exp(-dx / length)
            # TODO: xi as a random number drawn from distribution
            # C*(1 - 4/3*x*(1-x)), C = 9/7?
            # TF1 b("b", "9./7.5*(1 - 4/3*x*(1-x))", 0, 1);

        E1 = xi*part.E
        E2 = (1-xi)*part.E
        p1 = cpart(E1, 'e', x, y, y + (dy1 + rnd1)*SFy*length / gamma * elySF)
        p2 = cpart(E2, 'e', x, y, y + (dy2 + rnd2)*SFy*length / gamma * elySF)
        part.xend = x # terminate the parent particle
        #part.interacted = True
        #world.UpdateMaxGen()
        return [p1, p2]
    
    # decay the pions
    elif part.pid == 'pi' and part.E < ECpiThr:
        ps, xend = twoParticleDecay(part, gamma, world, dy1, rnd1, dy2, rnd2, addSFy)
        # terminate muons and neutrinos:
        if len(ps) == 0:
            return []
        ps[0].xend = world.x2
        ps[1].xend = world.x2
        part.xend = xend # terminate the parent particle
        #part.interacted = True
        #world.UpdateMaxGen()
        return ps
            
    elif (part.pid == 'pi' or part.pid == 'p') and part.E >= ECpiThr:
            #xi = 1/3.
            #chi = 0.
            if halfSteps:
                x = part.x + length*log(2)
            else:
                dx = exponential(length)
                #xi = exp(-dx / length)
                x = part.x + dx
                if x > world.x2:
                    x = world.x2
                #chi = 2.
                #while 1 - xi - chi < 0.:
                #    chi = random.random()
            #if verbose:
            #    print('  ...performing pion production!')
            pions = genPions( part.pid, (1.-world.Tunables.Inelasticity)*part.E, gamma, length, x, y, world)
            # keep the same y for the continuing proton or proton born in pi interaction:
            proton = cpart(part.E*world.Tunables.Inelasticity, 'p', x, y, y)
            newps = [proton]
            newps.extend(pions)
            part.xend = x # terminate the parent particle
            #part.interacted = True
            #world.UpdateMaxGen()
            return newps

    # decay muons
    elif part.pid == 'mu':
        ps, xend = twoParticleDecay(part, gamma, world, dy1, rnd1, dy2, rnd2, addSFy)
        # terminate electron and neutrino:
        if len(ps) == 0:
            return []
        ps[0].xend = world.x2
        ps[1].xend = world.x2
        part.xend = xend # terminate the parent particle
        #part.interacted = True
        #world.UpdateMaxGen()
        return ps
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
def Simulate(doDraw, primary, world, E0, randomizeY, halfSteps):
    print('===> Running the simulation!')
    newparticles = []
    newparticles.append(primary)
    
    np = -1
    istep = -1
    nMax = 1e8

    allparticles = []
    while len(newparticles) > 0 and len(allparticles) < nMax: # producing particles
        istep = istep + 1
        print(f'step: {istep:3} | total particles count: {len(allparticles):11,} | new particles: {len(newparticles):11,}')
        todoparticles = PerformInteractionStep(world, newparticles, randomizeY, halfSteps)
        
        if doDraw:
            allparticles.extend(newparticles)
        newparticles = todoparticles
        for part in newparticles:
            pid = part.pid
            if pid == 'e' or pid == 'pi' or pid == 'p':
                # we do not have the xend information at this point
                # so cannot average x and xend...
                world.h1Nx.Fill(part.x - primary.xend)

    print('...done simulating!')
    world.steps = 1*istep
    return allparticles

##########################################
def DrawResults(world, particles, halfSteps):
    lines = []
    can, h2 = world.Draw()
    can.cd()
    print('Drawing particles...')
    h2.Draw()
    drawn = 0
    Ncut = 1e7
    NmaxDraw = 1e8 # must be bigger than Ncut!
    drawFrac = 0.3
    partialDraw = len(particles) > Ncut
    ipart = 0

    requids = ['pi', 'p']
    skipmode = True
    for part in particles:
        if len(requids) > 0:
            if part.pid in requids and skipmode:
                continue
            if not part.pid in requids and not skipmode:
                continue
        ipart = ipart + 1
        if (ipart-1) % 1000000 == 0 and ipart > 0:
            print(f'{ipart-1:10,} / {len(particles):10,}; drawn: {drawn:10,}')
        if drawn < NmaxDraw:
            if drawn < Ncut or (drawn >= Ncut and random.random() < drawFrac):
                line = DrawParticle(part, world, halfSteps)
                drawn = drawn + 1
                #print('E: ', part.E)
                lines.append(line)
                
    skipmode = False
    requids = ['pi']
    for part in particles:
        if len(requids) > 0:
            if part.pid in requids and skipmode:
                continue
            if not part.pid in requids and not skipmode:
                continue
        ipart = ipart + 1
        if (ipart-1) % 1000000 == 0 and ipart > 0:
            print(f'{ipart-1:10,} / {len(particles):10,}; drawn: {drawn:10,}')
        line = DrawParticle(part, world, halfSteps)
        lines.append(line)

    requids = ['p']
    for part in particles:
        if len(requids) > 0:
            if part.pid in requids and skipmode:
                continue
            if not part.pid in requids and not skipmode:
                continue
        ipart = ipart + 1
        if (ipart-1) % 1000000 == 0 and ipart > 0:
            print(f'{ipart-1:10,} / {len(particles):10,}; drawn: {drawn:10,}')
        line = DrawParticle(part, world, halfSteps)
        lines.append(line)

    return can, h2, lines, partialDraw

##########################################

def processArgs(argv):

    print(argv)
    if len(argv) > 1 and argv[1] == '-h':
        print(f'Usage: {argv[0]} [E(GeV)=100GeV] [iteration=0] [batch=0] [draw=1]')
        return -1, 0, 0, 0

    print(f'*** Running {argv[0]}')
    E = 500 # GeV
    if len(argv) > 1:
        Ereq = float(argv[1])
        #if Ereq <= 1000000 and Ereq >= 30:
        E = Ereq
        if E < 21:
            # assuming we got logE
            E = pow(10, E - 9)
        else:
            # assuming we got E in GeV
            E = Ereq
        #else:
        #    print(f'Wrong custom energy E={Ereq} GeV, using default E={E} GeV')
        print(f'Using custom energy             E: {E} GeV')

    iteration = 0
    if len(argv) > 2:
        req_iteration = int(argv[2])
        if req_iteration >= 0 and req_iteration < 10000:
            print(f'OK, using user-defined iteration : {req_iteration}')
            iteration = req_iteration

    gBatch = False
    if len(argv) > 3:
        reqBatch = int(argv[3])
        if reqBatch > 0:
            print(f'OK, using user-defined batch mode: {reqBatch}')
            gBatch = True
        
    if gBatch:
        ROOT.gROOT.SetBatch(1)

    doDraw = True
    if len(argv) > 4:
        reqDraw = int(argv[4])
        if reqDraw == 0:
            print(f'OK, using user-defined draw mode : {reqDraw}')
            doDraw = reqDraw
   
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

#########################################
def doAllDrawing(world, primary, E0, particles, halfSteps, tag, gtag, h1Nx, partCounts):

        can, h2, lines, partialDraw = DrawResults(world, particles, halfSteps)
        if partialDraw:
            gtag = gtag + '_partialDraw'
        print(f'Drawn lines: {len(lines):10,}')
        # draw label
        txt = ROOT.TLatex(0.02, 0.95, 'Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M, steps={:1.0f}, muons stable: {}'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6, world.steps, not world.decayMuons) )
        #txt = ROOT.TLatex(0.02, 0.95, 'Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6))
        txt.SetTextColor(ROOT.kWhite)
        #txt.SetTextSize(0.03)
        txt.SetNDC()
        txt.Draw()

        #xx, yy, dd = 0.70, 0.82, 0.045
        xx, yy, dd = 0.135, 0.825, 0.05
        ptxt = makePtctLabels(xx, yy, dd, partCounts)
        
        stuff.append(ptxt)
        
        can.Update()
        
        canname = 'AirStats'
        statcan = ROOT.TCanvas(canname, canname, 1225, 0, 700, 600)
        statcan.cd()
        h1Nx.SetLineColor(ROOT.kGreen)
        h1Nx.SetLineWidth(2)
        h1Nx.Draw('hist')

        form = '(x > [1])*[0]*( (x-[1])/([2]-[1]) )^( ([2]-[1])/([3]) ) * exp(([2] - x)/[3])'
        pns = 'Nmax', 'X0', 'Xmax', 'lambda'
        fname = 'fit'
        fun = ROOT.TF1(fname, form, h1Nx.GetXaxis().GetXmin(), h1Nx.GetXaxis().GetXmax())
        fun.SetLineColor(ROOT.kWhite)
        fun.SetLineWidth(2)
        fun.SetLineStyle(2)
        pvs = [h1Nx.GetMaximum()/8., 0., h1Nx.GetMean(), 150.]
        #h1.Fit(fname, '', '0')
        for pn,pv in zip(pns,pvs):
            ip = pns.index(pn)
            fun.SetParameter(ip, pv)
            fun.SetParName(ip, pn)
        h1Nx.Fit(fun, '', '0')
        fun.Draw('same')
        adjustStats(h1Nx)
        
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

        stuff.append([can, h2, statcan, lines, txt, fun])

        print('DONE!')
        return can, h2, lines, partialDraw, statcan, txt


##########################################
def spitSomeInfo(primary, E0, particles, world):
    print('Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M, steps={:1.0f}'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6, world.steps))
    #print('Primary: {}; E={:1.1f} TeV, particles: {:1.2f}M'.format(glabel[primary.pid], E0/1000., len(particles) / 1e6))

##########################################
