#!/usr/bin/python

# jk 23-27.4.2018

import ROOT

from Minverse import *

from CovEngine import *

from math import *

# https://en.wikipedia.org/wiki/Multivariate_normal_distribution

# global parameters of the function to be minimized:
gsigs = []
#gerrs = []
# covariances between sigma_ij
gSigmaCov = []
gSigmaCovInv = []

# correlation between bars:
gcorrsTrue = []
gcorrsExp = []

# number of studied correlated variables
gN = -1
gcans = []
stuff = []

#################################
# for Minuit:
# https://root-forum.cern.ch/t/numerical-minimization-with-root-math-functor/13286/2

class MyFunction( ROOT.TPyMultiGenFunction ):
    def __init__( self ):
        print "CREATED"
        ROOT.TPyMultiGenFunction.__init__( self, self )

    def NDim( self ):
        print 'PYTHON NDim called'
        return gN

    def DoEval(self, args):
        chi2 = 0.
        actualSigs = []
        index = -1
        for i in range(0,gN):
            for j in range(i+1,gN):
                index = index+1
                s1 = args[i]
                s2 = args[j]
                # no correlations:
                #actualSigs.append( sqrt(s1*s1 + s2*s2) )
                # using experimentally measured correlations:
                actualSigs.append( sqrt(s1*s1 + s2*s2 - 2*gcorrsExp[index]*s1*s2) )
                # using true (injected) correlations:
                #actualSigs.append( sqrt(s1*s1 + s2*s2 - 2*gcorrsTrue[i][j]*s1*s2) )
                
        #for x,sig,err in zip(actualSigs,gsigs,gerrs):
        #    chi2 = chi2+pow( (x-sig)/err, 2)
        diff = []
        for i in range(0, len(actualSigs)):
            diff.append(actualSigs[i] - gsigs[i])
        chi2 = Chi2(diff, gSigmaCovInv)
        return chi2
    
#################################

def Chi2(x, A):
    # computes x^T A x
    n = len(x)
    yy = [0] * n
    for i in range(0,n):
        for j in range(0,n):
            yy[i] = yy[i] + A[i][j]*x[j]
    val = 0.
    for i in range(0,n):
        val = val + x[i]*yy[i]
    return val

#################################

def multigauss(vecx, CovInv):
    return exp(-Chi2(vecx, CovInv)/2.)

#################################

def GenerateN(n, t0, t1, rand):
    x = []
    for i in range(0,n):
        x.append(rand.Uniform(t0, t1))
    return x


#################################

def FillHists(h1, x):
    for h,val in zip(h1,x):
        h.Fill(val)
    return

#################################

def FillDeltas(h1, x):
    n = len(x)
    ih = 0
    for i in range(0,n):
        for j in range(i+1,n):
            h1[ih].Fill(x[i] - x[j])
            ih = ih+1
    return

#################################

def FillH2s(h2, x):
    n = len(x)
    ih = 0
    for i in range(0,n):
        for j in range(i+1,n):
            h2[ih].Fill(x[i],x[j])
            ih = ih+1
    return


#################################
def GetSigma_ij(nEvt, t0, t1, gN, rand, Sinv,  Draw, itoy = 0):

    h1 = []
    for i in range(0,gN):
        name = 't{:}_{:}'.format(i,itoy)
        title = 't{:}'.format(i,)
        hist = ROOT.TH1D(name, title, nbins, t0, t1)
        #hist.SetStats(0)
        h1.append(hist)

    delta1 = []
    h2 = []
    
    for i in range(0,gN):
        for j in range(i+1,gN):
            name = 'deltat_{:}_{:}_{:}'.format(i,j,itoy)
            title = 'deltat_{:}_{:}'.format(i,j)
            hist = ROOT.TH1D(name, title + ';#Delta_{' + '{:}{:}'.format(i,j) + '};', nbins, t0, t1)
            hist.SetStats(0)
            delta1.append(hist)
            name = 't{:}_vs_t{:}_{:}'.format(j,i, itoy)
            title = 't{:}_vs_t{:}'.format(j,i)
            hist = ROOT.TH2D(name, title + ';t{:};t{:}'.format(i,j), nbins/4, t0, t1, nbins/4, t0, t1)
            hist.SetStats(0)
            h2.append(hist)


    empty = [0.]*gN
    maxy = multigauss(empty, Sinv)
    #print maxy

    # bootstrap?
    # Nreplicas = 1000
    # TODO?
    # write a class of TH1D bootstrap for delta histos to be fitted replica by replica
    # then build Cov between fitted sigmas of the delta histos
    # use it in the global fit


    ngen = 0
    while (ngen < nEvt):
        x = GenerateN(gN, t0, t1, rand)
        if multigauss(x, Sinv) > rand.Uniform(0.,maxy):
            # von Neumann accepts
            FillHists(h1, x)
            FillDeltas(delta1,x)
            FillH2s(h2,x)

            # fill bootsrap replicas!
            # random number inside the bootsrap class/global?


            ngen = ngen + 1
            if ngen % (nEvt / 5) == 0:
                print '  evt {:}/{:}'.format(ngen,nEvt)


    # end of event loop

    if Draw:
        
        stuff.append(h1)
        stuff.append(h2)
        stuff.append(delta1)
        
        canname = 'Bars'   
        can = ROOT.TCanvas(canname, canname, 0, 0, 1600, 1200)
        gcans.append(can)
        can.Divide(2,2)
        ican = 0
        for h in h1:
            ican = ican+1
            can.cd(ican)
            h.Draw('hist')

        canname = 'Deltas'
        can = ROOT.TCanvas(canname, canname, 0, 0, 1600, 1200)
        gcans.append(can)
        can.Divide(3,2)
        ican = 0

        for h in delta1:
            ican = ican+1
            can.cd(ican)
            h.Draw('hist')

            txt = ROOT.TLatex(0.2, 0.82, '#sigma^{exp}  = ' + '{:2.1f}'.format(h.GetRMS()) )
            txt.SetTextColor(ROOT.kBlue)
            txt.SetNDC()
            txt.Draw()
            stuff.append(txt)

            # get indices from hname:
            ind = h.GetTitle().split(';')[0].replace('deltat_', '').replace('_',' ').split()
            i = int(ind[0])
            j = int(ind[1])
            s1 = BarSigma[i]
            s2 = BarSigma[j]
            s = sqrt(s1*s1 + s2*s2 - 2.*s1*s2*gcorrsTrue[i][j])
            txt = ROOT.TLatex(0.2, 0.75, '#sigma^{theor} = '+ '{:2.1f}'.format(s) )
            txt.SetTextColor(ROOT.kRed)
            txt.SetNDC()
            txt.Draw()
            stuff.append(txt)

            s = sqrt(s1*s1 + s2*s2)
            txt = ROOT.TLatex(0.2, 0.68, '#sigma^{no corr} = '+ '{:2.1f}'.format(s) )
            txt.SetTextColor(ROOT.kMagenta)
            txt.SetNDC()
            txt.Draw()
            stuff.append(txt)

        canname = 'Covs'
        can = ROOT.TCanvas(canname, canname, 0, 0, 1600, 1200)
        gcans.append(can)
        can.Divide(3,2)

        # prepare the measured correlation between bars!
        ican = 0
        for h in h2:
            ican = ican+1
            can.cd(ican)
            h.Draw('colz')

            corr = h.GetCorrelationFactor()
            gcorrsExp.append(corr)
            txt = ROOT.TLatex(0.2, 0.82, '#rho^{exp}  = ' + '{:1.2f}'.format(corr))
            txt.SetTextColor(ROOT.kBlue)
            txt.SetNDC()
            txt.Draw()
            stuff.append(txt)

            # get indices from hname:
            ind = h.GetTitle().split(';')[0].replace('_vs_', ' ').replace('t','').split()
            #print ind
            txt = ROOT.TLatex(0.2, 0.75, '#rho^{theor} = '+ '{:1.2f}'.format(gcorrsTrue[int(ind[0])][int(ind[1])]))
            txt.SetTextColor(ROOT.kRed)
            txt.SetNDC()
            txt.Draw()
            stuff.append(txt)
        print 'True correlation between bars:'
        PrettyPrintMatrix(gcorrsTrue)
        print 'Measured nontrivial sub-correlation between bars:'
        print gcorrsExp
    # draw
    sigma_ij = []
    for h in delta1:
        # get indices from hname:
        ind = h.GetTitle().split(';')[0].replace('deltat_', '').replace('_',' ').split()
        i = int(ind[0])
        j = int(ind[1])
        if i != j:
            sigma_ij.append(h.GetRMS())
    #print 'Done, returning ', sigma_ij    
    return sigma_ij


#################################
#################################
#################################

# time sigma in ps:
#sigma = [10, 12, 8]
#gcorrsTrue = [ [1.,    0.30, 0.25 ],
#         ['a',   1.,   0.55],
#         ['a',   'a',  1.],
#]

BarSigma = [15, 10, 20, 12]
#gcorrsTrue = [ [1., 0.35, 0.15, 0.0],
#               ['a',   1., 0.25, 0.15],
#               ['a',   'a',   1., 0.30],
#               ['a',   'a',   'a',  1.],
#]

gcorrsTrue = [ [1., 0.20, 0.05, 0.0],
               ['a',   1., 0.15, 0.05],
               ['a',   'a',   1., 0.20],
               ['a',   'a',   'a',  1.],
]

gN = len(BarSigma)

# symmetrize the corr matrix:
for i in range(0,gN):
    for j in range(0,gN):
        if gcorrsTrue[i][j] == 'a':
            gcorrsTrue[i][j] = gcorrsTrue[j][i]
        # safety:
        if i == j:
            gcorrsTrue[i][j] = 1.
print gcorrsTrue

# covariance matrix between times of individual bars:
# (to generate the multi gauss)
Cov = []
for i in range(0,gN):
    sigrow = []
    for j in range(0,gN):
        sigrow.append(BarSigma[i]*BarSigma[j]*gcorrsTrue[i][j])
    Cov.append(sigrow)

print Cov
Sinv = getMatrixInverse(Cov)
#PrintMatrix(Sinv)
print Sinv

# some ranges and sane values:
nbins = 100
t0 = -100.
t1 = 100.

# hits to generate for each toy
nEvt = 300
rand = ROOT.TRandom3()
        

############################################################
# Run toys!

nToys = 300
covEngine = CovEngine(gN*(gN-1)/2, 1000, t0, t1)

for itoy in range(0, nToys):
    if itoy % 10 == 0:
        print 'Toy {:}/{:}'.format(itoy,nEvt)

    sigma_ij = GetSigma_ij(nEvt, t0, t1, gN, rand, Sinv, (itoy == 0), itoy)
    # keep first run as single data result:
    if itoy == 0:
        # make the global observed sigma_ij in one single experiment
        gsigs = sigma_ij
    # add current result to the Cov computational engine:
    covEngine.Add(sigma_ij)


# Analyze: minimize big chi2 between sigma_ij for the solution of sigma_i
# https://root-forum.cern.ch/t/numerical-minimization-with-root-math-functor/13286#p58684

# not returning errors:
# minimizer = ROOT.Math.Factory.CreateMinimizer("GSLMultiMin", "BFGS")
minimizer = ROOT.Math.Factory.CreateMinimizer('Minuit2', 'Minuit2' )
minimizer.SetMaxFunctionCalls(1000000)
minimizer.SetMaxIterations(100000)
minimizer.SetTolerance(0.001)
minimizer.SetPrintLevel(1)
myfun = MyFunction()

steps = [0.01] * gN
variables = [10.] * gN
varnames = [ 'sigma{:}'.format(i) for i in range(0,gN) ]
minimizer.SetFunction(myfun)

can1,can2 = covEngine.DrawAll()
gcans.append(can1)
gcans.append(can2)
#ROOT.gApplication.Run()

gSigmaCov = covEngine.GetCovariance()
print 'Grand Cov matrix:'
PrettyPrintMatrix(gSigmaCov)
print 'Inverting the big Cov matrix for big chi2...'
gSigmaCovInv = getMatrixInverse(gSigmaCov)

## TODO: make the global Cov between sigma_ij and invert it!
#for i in range(0,len(h2)):
#    # mage the global errors:
#    gerrs.append(h2[i].GetRMSError())

print 'gsigmas : ', gsigs
print gSigmaCovInv

#print 'gerrs   : ', gerrs

# Set the free variables to be minimized!
ivar = -1
for varname,var,step in zip(varnames,variables,steps):
    ivar = ivar+1
    minimizer.SetLimitedVariable(ivar,varname,var, step, 5., 30.)

########################
### !!! MINIMIZE !!! ###
########################
print 'Extracted correlations:'
print gcorrsExp
minimizer.Minimize()

status = minimizer.Status()
# minval = minimizer.MinValue()  
             
if minimizer.Status() == 0:
    SigmaFitted = minimizer.X()
    Errs = minimizer.Errors()
    print 'OK, FOUND Minimum'
    ip = -1
    for fitpar,err,inpar in zip (SigmaFitted,Errs,BarSigma):
        ip = ip+1
        #print 'Par{:} input {:2.2f} fitpar {:2.2f}'.format(ip, inpar,fitpar)
        print 'Par{:} input {:2.2f} fitpar {:2.2f} ratio {:1.2f}   shift {:2.1f} sigma'.format(ip, inpar,fitpar, fitpar/inpar, (fitpar-inpar)/err) 

else:
    print 'FAILED MINIMIZATION!'

for can in gcans:
    can.Print(can.GetName() + '.png')

ROOT.gApplication.Run()
