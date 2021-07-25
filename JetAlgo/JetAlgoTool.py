#!/usr/bin/python

# JK March 2016


from myAll import *
from ProcessTools import *

debug = 0

###############################################
def NnonEmptyAround(hist,ii,jj,d,thr):
    n = 0
    for i in range(ii-d,ii+d):
        for j in range(jj-d,jj+d):
            if j<=0 or j > maxN: continue
            if i<=0 or i > maxN: continue
            val = hist.GetBinContent(i,j)
            if val > thr:
                n=n+1
    return n
            
###############################################
def makeListFromHisto(hist, thr = 50., thr2=50., d=2, nmin = 6):
    plist = []
    for i in range(1,hist.GetXaxis().GetNbins()+1):
        for j in range(1,hist.GetYaxis().GetNbins()+1):
            val = hist.GetBinContent(i,j)
            if NnonEmptyAround(hist,i,j,d,thr) >= nmin:
                if val > thr2:
                    plist.append(pitem(val, i, j))
    return plist


###############################################

class pitem:
    # massless initializer:
    def __init__(self, E, eta, phi):
        if debug > 1: print ('MassLess E,eta,phi ', E, eta, phi)
        self.eta = eta
        self.phi = phi
        # massless:
        self.E = E

    def Print(self):
        print ('  E,eta,phi ', self.E, self.eta, self.phi)

###############################################
def combine(it1, it2):
    E = it1.E + it2.E
    # energy weighted:
    eta = (it1.eta*it1.E + it2.eta*it2.E) / (it1.E + it2.E)
    phi = (it1.phi*it1.E + it2.phi*it2.E) / (it1.E + it2.E)
    it = pitem(E, eta, phi)
    return it

###############################################
def DeltaPhi(phi1, phi2):
    dphi = math.fabs(phi1 - phi2)
    #if dphi > 2*Pi:
    #    dphi = 2*Pi - dphi 
    #if debug > 2: print ('dphi = {:f} '.format(dphi,) )
    return dphi

###############################################
def DeltaR2(i1, i2):
    return  ( pow( DeltaPhi(i1.phi,i2.phi), 2) + pow(i1.eta - i2.eta, 2) )


###############################################
def MakeDistances(pList, R, p):
    distances = []
    for i in range(0, len(pList)):
        for j in range(0, len(pList)):
            distance = -1.
            if i != j:
                minpt = min( pow(pList[i].E, 2*p), pow(pList[j].E, 2*p) )
                distance = DeltaR2(pList[i], pList[j])*minpt
            else:
                distance = pow(pList[i].E, 2*p) * pow(R, 2)
            distances.append( [i, j, distance] )
    return distances
            

###############################################
def GetMin(distances):
    imin = -1
    dmin = 1.e32
    i = 0
    for d in distances:
        if d[2] < dmin:
            dmin = d[2]
            imin = i
        i = i + 1
    return imin

###############################################
def RunJetAlgo(pList, R = 5, p = -1.):

    Jets = []

    ipass = -1
    while len(pList) > 0:
        ipass = ipass+1
        if ipass % 100 == 0: print ('=== iteration {:} ==='.format(ipass,) )
        if debug > 1:
            for particle in pList:
                particle.Print()

    # index of min distance
        distances = MakeDistances(pList, R, p)
        imind = GetMin(distances) 
        mind = distances[imind][2]

        # is the min distance a self-distance?
        # compare indices of the objects, w.r.t. the pList:
        if distances[imind][0] == distances[imind][1]:
            # we have a jet!
            Jets.append(pList[distances[imind][0]])
            pList.pop(distances[imind][0])
        else:
            # combine the particles:
            newitem = combine(pList[distances[imind][0]], pList[distances[imind][1]])
            indices = [distances[imind][0], distances[imind][1] ]
            for index in sorted(indices, reverse=True):
                if debug: print ('deleting item ', index)
                del pList[index]
            pList.append(newitem)
    
    return Jets


###############################################
###############################################
###############################################



# STEERING

# the R parameter of the jet algorithm
Rs = [5.]

# the p parameter of the jet algorithm
# -1 ... anti-kt
#  0 ... cone
#  1 ... kt

ps = [-1.]
#ps = [0]
#ps = [1]

cirs = []

rfile = ROOT.TFile('JeskyneJune201603.root', 'read')
hist0 = rfile.Get('histo')


print ('Exponents of the JetKt algorith to process: ', ps)
for p in ps:
    print ('--- processig p={:1.1f} ---'.format(p,) )
    for R in Rs:
        print ('  --- processig R={:1.1f} ---'.format(R,) )
        # generate same jets in event:
        hist = RemoveSpikes(hist0) 
        pList = makeListFromHisto(hist)
 
        ###################################
        # Draw bare:
        canname = 'GeneratedParticles'
        can = nextCan.nextTCanvas(canname, canname, 100, 100, 1000, 800)
        hcopy = hist.DrawCopy('lego2')
        #can.Print(canname + '.png')
        hcopy = hist.Draw('colz')
        can.Print(canname + '_colz.png')
        can.Print(canname + '_colz.pdf')

        
        ###################################
        # run jet algorithm on event
        Jets = RunJetAlgo(pList, R, p)
        ###################################

        
        # keep associated particles in jet somehow?
        # TODO

        # plots jets constituents with different color?
        # mark jet axis and draw a circle
        # most still TODO
        

        ###################################
        # Draw jets:
        canname = 'Jets_R%1.1f_p%1.1f' % (R,p,)
        can = nextCan.nextTCanvas(canname, canname, 0, 0, 1000, 800)


        hist.Draw('colz')
        print ('=============================================')
        print ('                  RESULTS                    ')
        print ('=============================================')
        print ('===> {:} jets found:'.format(len(Jets),) )

        canname = 'EhistCan'
        can = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)
        name = 'Ehist'
        hist.DrawCopy('colz')
        Ehist = nextCan.nextH1(name, name, 20, 0., 10.)

        # TODO: histogramme of jet energies above 1MeV!;-)
        for jet in Jets:
            jet.Print()
            # draw a circle:
            # TODO
            circ = ROOT.TEllipse(jet.eta, jet.phi, R, R)
            #delta = ROOT.Double(0)
            circ.SetLineStyle(1)
            circ.SetLineColor(ROOT.kRed)
            circ.SetLineWidth(1)
            circ.SetFillStyle(-1)
            Ehist.Fill(jet.E)
            if jet.E > 1000.:
                circ.SetLineStyle(1)
                circ.SetLineWidth(2)
                #jet.Print()
                #    circ.SetLineWidth(2)
                #    circ.SetLineStyle(2)
                #if jet.E > 100.:
                #    circ.SetLineWidth(3)
                #    circ.SetLineStyle(1)
                #    #delta = max(0,math.log(jet.E))
                #    #circ.SetLineWidth(1.+delta/10.)
                
                # one more circle to account for cyclic phi?
            circ.Draw()
            cirs.append(circ)

        print ('Energy mean: {:1.3f}'.format(Ehist.GetMean(),) )
        ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

        tag = '_p{:}_R{:}'.format(p, R)
        can.Print(canname + tag + '.png')
        can.Print(canname + tag + '.pdf')


ROOT.gApplication.Run()

