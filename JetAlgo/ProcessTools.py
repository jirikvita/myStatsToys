#!/usr/bin/python

from __future__ import print_function

from math import *
import ROOT

maxN=256
rdef = 10 # default alfa circle radius
ghlist = []
gcans = []
junk = []

gZERO = 1.e-6
gInfty = 1e24

ObjNames = ['alfa', 'beta', 'gamma', 'muon', 'heavy']
iAlfa = ObjNames.index('alfa')
iBeta = ObjNames.index('beta')
iGamma = ObjNames.index('gamma')
iMuon = ObjNames.index('muon')
iHeavy = ObjNames.index('heavy')



##############################################
def GetNnonNegative(hist):
    n = 0
    for ii in range(1,maxN+1):
        for jj in range(1,maxN+1):
            val = hist.GetBinContent(ii,jj)
            if val > 0:
                n = n + 1
    return n


##############################################
def MakeNegative(hist, tag = ''):
    neg = hist.Clone(hist.GetName() + '_neg' + tag)
    neg.SetTitle('negative')
    neg.Scale(1.)
    hmax = neg.GetMaximum()
    for ii in range(1,maxN+1):
        for jj in range(1,maxN+1):
            val = hist.GetBinContent(ii,jj)
            neg.SetBinContent(ii,jj, hmax-val)
    return neg

##############################################
def MakeSmeared(hist, npix = 2, thrToSmear = 0.1, tag = ''):
    smear = hist.Clone(hist.GetName() + '_smear' + tag)
    hmax = hist.GetMaximum()
    # TO FINISH using the threshold to merge!!!
    # or introduce some gaussian convolution?
    for ii in range(1,maxN+1, npix):
        for jj in range(1,maxN+1, npix):
            sum = 0
            nn=0
            for xi  in range(0,npix):
                for xj  in range(0,npix):
                    if ii+xi > maxN: continue
                    if jj+xj > maxN: continue
                    nn=nn+1
                    val = hist.GetBinContent(ii+xi,jj+xj)
                    sum = sum+val
            sum = sum/nn
            for xi  in range(0,npix):
                for xj  in range(0,npix):
                    smear.SetBinContent(ii+xi,jj+xj, sum)
    return smear


##############################################

def CheckRange(i):
    return i >= 1 and i <= maxN
def InCircle(i, j, ii, jj, r):
    return sqrt( pow(i-ii,2) + pow(j-jj,2) ) < r
def InEllipse(i, j, ii, jj, rx, ry):
    return sqrt( pow((i-ii)/rx,2) + pow((j-jj)/ry,2) ) < 1.

##############################################
def GetAverAroundPixel(hist, i, j, d=1):
    aver = 0.
    n = 0
    for ii in range(i-d,i+d+1):
        for jj in range(j-d,j+d+1):
            if ii == jj:
                continue
            aver = aver + hist.GetBinContent(ii, jj)
            n = n+1
    if n > 0:
        aver = aver/n
    return aver
  

##############################################
def IsLocalMaximum(hist, i, j, d=1):
    maxval = -1
    maxi = -1
    maxj = -1
    for ii in range(i-d,i+d+1):
        for jj in range(j-d,j+d+1):
            val = hist.GetBinContent(ii, jj)
            if val > maxval:
                maxi = ii
                maxj = jj
                maxval = val
    return i == maxi and j == maxj

##############################################
def GetGamma(hist, usedMap, i, j, d, thr = gZERO):
    pixels = []
    for ii in range(i-d,i+d+1):
        for jj in range(j-d,j+d+1):
            if usedMap.GetBinContent(ii,jj) > gZERO:
                continue
            val = hist.GetBinContent(ii, jj)
            if val > thr:
                pixels.append([ii,jj])
    return pixels

##############################################    
def MarkAsUsed(hist, pixels, val = 1.):
    for pix in pixels:
        hist.SetBinContent(pix[0], pix[1], val)

##############################################

def RemoveSpikes(hist, bgthr=0.2, maskWithAver = True, debug = 0):
    newhist = hist.Clone('processed')
    for ii in range(1,maxN+1):
        for jj in range(1,maxN+1):
            val = hist.GetBinContent(ii,jj)
            averAround = GetAverAroundPixel(hist, ii, jj)
            if val > 0:
                if averAround / val < bgthr:
                    if maskWithAver:
                        if debug: print ('masking spike {:f} at {:},{:} with aver={:f}'.format(val,ii,jj,averAround) )
                        newhist.SetBinContent(ii,jj,averAround)
                    else:
                        if debug: print ('removing spike {:f} at {:},{:} aver={:f}'.format(val,ii,jj,averAround) )
                        newhist.SetBinContent(ii,jj,0.)
                else:
                    newhist.SetBinContent(ii,jj,val)

    newhist.Scale(1.)
    return newhist

def AverInCircle(hist, i, j, params):
    aver = 0.
    n = 0.
    r = params[0]
    for ii in range(i-r-1,i+r+1):
        if not CheckRange(ii):
            continue
        for jj in range(j-r-1,j+r+1):
            if not CheckRange(jj):
                continue
            if not InCircle(i, j, ii, jj, r):
                continue
            aver = aver + hist.GetBinContent(i,j)
            n=n+1
    return aver/n

##############################################
def GetChi2CmpAlfa(hist, i, j, params = [rdef]):
    chi2 = -1
    r = params[0]
    aver = GetAverInCircle(hist,i,j,para,s)
    ndf = 0
    for ii in range(i-r-1,i+r+1):
        if not CheckRange(ii):
            continue
        for jj in range(j-r-1,j+r+1):
            if not CheckRange(jj):
                continue
            if not InCircle(i, j, ii, jj, r):
                continue
            chi2 = chi2 + pow(aver - hist.GetBinContent(i,j), 2)
            ndf = ndf + 1
    if ndf > 0:
        chi2 = chi2 / ndf
    return chi2

##############################################
def GetChi2Comp(hist, i, j, objId = iAlfa, params = [rdef]):
    chi2 = -1
    if objId == iAlfa:
        chi2 = GetChi2CmpAlfa(hist, i, j, params)

    return chi2


##############################################
def MakeEmptyHisto(hist, name = '_usedpixels'):
    newh = hist.Clone(hist.GetName() + name)
    newh.Reset()
    ghlist.append(newh)
    return newh


##############################################
def GetGammas(hist, d=1):
    usedMap = MakeEmptyHisto(hist)
    gammas = []
    for ii in range(1,maxN+1):
        for jj in range(1,maxN+1):
            if usedMap.GetBinContent(ii,jj) > gZERO:
                continue
            val = hist.GetBinContent(ii,jj)
            # if point is not a local maximum, skip it
            if not IsLocalMaximum(hist, ii, jj, d):
                continue
            # if is a local maximum, count this as gamma, and mark pixels around as used
            pixels = GetGamma(hist, usedMap, ii, jj, d)
            MarkAsUsed(usedMap, pixels)
            gamma = [ii, jj]
            gammas.append(gamma)
    return gammas

##############################################

def GetNgamma(hist):
    gammas = GetGammas(hist)
    ng = len(gammas)
    return ng


##############################################
def DrawCircleAroundObjects(objects, d=10, width=1, col = ROOT.kGray):
    for obj in objects:
        i = obj[0]
        j = obj[1]
        circ = ROOT.TEllipse(i,j,d,d)
        circ.SetLineColor(col)
        circ.SetLineWidth(width)
        circ.SetFillStyle(0)
        circ.Draw()
        junk.append(circ)
        
        

##############################################
def HoughTransf(hist, relthr = 0., nbins = int(maxN*sqrt(2.))):
    # theta, r
    hough = ROOT.TH2D(hist.GetName() + '_hough', 'Hough transfromed;#theta;r;', maxN, -pi, pi, 2*nbins, -nbins, nbins)
    # loop over points
    newhist = RemoveSpikes(hist)
    for ii in range(1,maxN+1):
        for jj in range(1,maxN+1):
            val = newhist.GetBinContent(ii,jj)
            # vary theta
            if val > 0:
                for itheta in range(0,hough.GetNbinsX()):
                    theta = hough.GetXaxis().GetBinCenter(itheta)
                    # compute r of closest approach of the line to the origin
                    r = ii*sin(theta)+jj*cos(theta)
                    # fill hough
                    hough.Fill(theta, r)
                
    return hough

##############################################
def FindMaximumAndKillAround(hist, minx,maxx,miny,maxy, dtheta,dr):
    zmax = -gInfty
    imax = -1
    jmax = -1
    # find global max:
    for ii in range(minx,maxx):
        for jj in range(miny,maxy):
            val = hist.GetBinContent(ii,jj)
            if val > zmax:
                imax = ii
                jmax = jj
                zmax = val
    # now kill region around the max:
    for ii in range(imax-dtheta-1,imax+dtheta+1):
        if ii < minx or ii > maxx:
            continue
        for jj in range(jmax-dr-1,jmax+dr+1):
            if jj < miny or jj > maxy:
                continue
            if not InEllipse(imax, jmax, ii, jj, dtheta, dr):
                continue
            hist.SetBinContent(ii,jj,0.)
    thetaStep = 2*pi/maxN
    point = [-pi + imax*thetaStep, -int(maxN*sqrt(2.)) + jmax, zmax]
    return point

##############################################
# default maxima separation of 5 degree, converted to nu,ber of theta bins, and dr of 15 pixels:
def FindMaximaOverAbsThr(hough, abstrh = 60., dr = 15, dtheta = int(pi/18./2./(2*pi/maxN)), maxNRes = 10):
    hist = hough.Clone(hough.GetName() + '_clone')
    nx = hough.GetNbinsX()
    ny = hough.GetNbinsY()
    for ii in range(1,nx+1):
        for jj in range(1,ny+1):
            if hist.GetBinContent(ii,jj) < abstrh:
                hist.SetBinContent(ii,jj, 0.)
    # focus on 1st quadrant only, the rest is duplicite:
    Points = []
    gotResult = True
    while gotResult:
        point = FindMaximumAndKillAround(hist, 1,nx+1,ny/2,ny+1,dtheta,dr)
        if len(point) > 0 and len(Points) < maxNRes and point[2] >= abstrh:
            gotResult = True
            Points.append(point)
        else:
            gotResult = False
            
    return Points



##############################################
def InvHoughTransf(hough, absthr = 60.):
    # theta, r
    hist = ROOT.TH2D(hough.GetName() + '_inv_hough', 'Hough inverse transfromed;x;y;', maxN, 0, maxN, maxN, 0, maxN)
    # loop over spikes:
    spikeList = FindMaximaOverAbsThr(hough,absthr)
    print ('  spikes list: ', spikeList)
    nlines = len(spikeList)
    for spike in spikeList:
        theta = spike[0]
        r = spike[1]
        for ii in range(1,maxN+1):
            jj = -tan(theta) * ii + r/cos(theta)
            if CheckRange(int(jj)):
                #print ('   filling ', ii,jj)
                hist.Fill(ii, int(jj) )
    return spikeList,hist


##############################################
def MakeGraph(spikeList, name, index):
    gr = ROOT.TGraph()
    gr.SetName(name)
    i = 0
    for spike in spikeList:
        gr.SetPoint(i, i, spike[index])
        i = i+1
    return gr
##############################################
def MakeListFromGraph(gr):
    spikeList = []
    x = ROOT.Double(0.)
    y = ROOT.Double(0.)
    for i in xrange(0,gr.GetN()):
        gr.GetPoint(i, x, y)
        llist = [y, -1, -1.]
        spikeList.append(llist)
    return spikeList

##############################################
##############################################
##############################################

