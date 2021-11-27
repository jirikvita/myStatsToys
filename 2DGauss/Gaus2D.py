#!/usr/bin/python
# jk 30.10.2017, 3.11.2017



import ROOT
import array
ROOT.gStyle.SetOptTitle(0)
from math import pi,atan,sqrt

import ctypes


# https://en.wikipedia.org/wiki/Multivariate_normal_distribution
# https://en.wikipedia.org/wiki/Gaussian_function
form = '[0]*exp( -1/(2*(1-[5]^2)) * (  (x-[1])^2 / [2]^2 + (y-[3])^2/[4]^2 - 2*[5]*(x-[1])*(y-[3]) / ([2]*[4]) )  )'
#npx = 500
npx = 100
AddWidth = 0

### STEERING!!! ###
#Print = False
Print = True
#SingleExample = True
SingleExample = False

ii = -1
jj = -1
if SingleExample:
    ii = 1
    jj = 2
    AddWidth = 2

# theoretical fun:
# https://stats.stackexchange.com/questions/32464/how-does-the-correlation-coefficient-differ-from-regression-slope
# https://www.thoughtco.com/slope-of-regression-line-3126232
# https://en.wikipedia.org/wiki/Multivariate_normal_distribution
# https://en.wikipedia.org/wiki/Best_linear_unbiased_prediction

# not needed in the end;-)
# TPrincipal:
# https://root.cern.ch/doc/master/classTPrincipal.html

# some nasty globals;)
xmin = 40
xmax = 170.
ymin = 40
ymax = 170.
mux = 110.
muy = 110.
rho = 0.65
nbins = 30
mus = [mux, muy]

objs = []
Grs = []
Profs = []
H2s = []
#Principals = []
#principal = ROOT.TPrincipal(2)


def MakeGenFunction(name, mux, muy, sx, sy, rho):
    gen = ROOT.TF2(name, form, xmin, xmax, ymin, ymax)
    gen.SetParameters(1., mux, sx, muy, sy, rho)
    gen.SetNpx(npx)
    gen.SetNpy(npx)
    gen.GetXaxis().SetTitle('X')
    gen.GetYaxis().SetTitle('Y')
    objs.append(gen)
    return gen

def MakeEllipseAxes(mu, sig, vect, eigenvals, nsig=1.0, width = 0.005, opt = '<>'):
    mux = mu[0]
    muy = mu[1]
    lines = []
    n = 2

    sf1=1.
    sf2=sqrt(eigenvals[1]/eigenvals[0])
    if sig[0] == sig[1]:
        sf1,sf2 = sf2,sf1
    #sf1 = 1.
    #sf2 = sf1*sqrt(eigenvals[1]/eigenvals[0])
    #if sig[0] == sig[1]:
    #sf1,sf2 = sf2,sf1
    sf = [sf1, sf2]
    # HACK! sf = [1., 1.]
    for i in range(0,n):
        #thissig=sig[n-i-1]
        a1 = sig[1]
        a2 = a1
        dx = sf[i]*nsig*a1*vect[i][0]
        dy = sf[i]*nsig*a2*vect[i][1]
        line = ROOT.TArrow(mux - dx, muy - dy, mux + dx, muy + dy, width, opt)
        lines.append(line)
    return lines

def MakeEllipses(mu, sig, vect, eigenvals, nsigs=[1., 2.], width = 0.005, opt = '>'):
    mux = mu[0]
    muy = mu[1]
    ells = []
    n = 2
    #eig = [eigenvals[0], eigenvals[1]]
    for nsig in nsigs:
        for i in range(0,n):
            #a1 = sig[0]
            #a2 = a1*sqrt(eigenvals[1]/eigenvals[0])
            a1=sig[1]
            a2=a1*sqrt(eigenvals[1]/eigenvals[0])
            if sig[0] == sig[1]:
                a1,a2 = a2,a1
            theta = atan(vect[0][1] / vect[0][0])/pi*180.
            ell = ROOT.TEllipse(mux, muy, nsig*a1, nsig*a2, 0., 360., theta)
            ell.SetFillStyle(0)
            ells.append(ell)
    return ells

# sigmas of the 2D gauss:
Sigmas =  [5., 10., 20., 30.]
#Sigmas =  [10., 30.]
Rhos = [-0.1, -0.3, -0.5, -0.8, 0.1, 0.3, 0.5, 0.8]
#Rhos = [ 0.8]

# define a high intelligency:
high = 130

xx = ctypes.c_double(0.) 
yy = ctypes.c_double(0.)
data = array.array('d', 2*[0])

N = 3000
help = ROOT.TH2D('tmp', 'tmp', nbins, xmin, xmax, nbins, ymin, ymax)
help.SetStats(0)
#help.GetXaxis().SetTitle('x')
#help.GetYaxis().SetTitle('yY')

fun = ROOT.TF1('lin', '[0]+[1]*x', xmin, xmax)
fun.SetNpx(npx)
fun.SetLineColor(ROOT.kBlue)
fun.SetLineStyle(2)
fun.SetLineWidth(1+AddWidth)
objs.append(fun)


diag = ROOT.TLine(xmin, xmin, xmax, xmax)


for rho in Rhos:
    canname = 'Gaus2D_{:1.2f}'.format(rho,)
    canname = canname.replace('.', '_')
    can = ROOT.TCanvas(canname, canname, 0, 0, 1000, 1000)
    if not SingleExample:
        can.Divide(4,4)

    hcanname = 'Gaus2D_{:1.2f}_hist'.format(rho,)
    hcanname = hcanname.replace('.', '_')
    hcan = ROOT.TCanvas(hcanname, hcanname, 0, 0, 1000, 1000)
    if not SingleExample:
        hcan.Divide(4,4)
        can.cd(1)
    objs.append(can)
    objs.append(hcan)
    
    ican = -1
    for sx in Sigmas:
        for sy in Sigmas:
            sigmas = [sx, sy]
            if SingleExample:
                if Sigmas.index(sx) != ii or Sigmas.index(sy) != jj:
                    continue

            ican = ican+1
            name='Gaus2D_{:2.0f}_{:2.0f}_{:1.2f}'.format(sx, sy, rho)
            gen = MakeGenFunction(name, mux, muy, sx, sy, rho)
            gr = ROOT.TGraph()
            gr.SetMarkerSize(0.5)
            gr.SetMarkerStyle(20)
            gr.SetMarkerColor(ROOT.kBlack)
            if SingleExample:
                gr.SetMarkerSize(0.7)
            Grs.append(gr)

            h2 = ROOT.TH2D(name+'_hist', name+'_hist', nbins, xmin, xmax, nbins, ymin, ymax)
            H2s.append(h2)

            #principal.Clear()# = ROOT.TPrincipal(2)
            #Principals.append(principal)
            
            for i in range(0,N):
                gen.GetRandom2(xx, yy)
                #print( 'x={0}, y={1}'.format(xx,yy))
                gr.SetPoint(i,xx,yy)
                h2.Fill(xx.value,yy.value)
                data[0] = xx.value
                data[1] = yy.value
                #principal.AddRow(data)
                
            #print ican
            if not SingleExample:
                can.cd(ican+1)
            else:
                can.cd()
            help.DrawCopy()
            gr.Draw('P')
            fun.SetParameters(-rho*sy/sx*mux+muy, rho*sy/sx)
            fun.DrawCopy('same')
            diag.SetLineStyle(2)
            diag.SetLineWidth(1+AddWidth)
            diag.Draw()
            mytext = ROOT.TLatex(0.20, 0.93, '#rho={:1.2f} #sigma_{{x}}={:2.0f} #sigma_{{y}}={:2.0f}'.format(rho, sx, sy))
            ###mytext = ROOT.TLatex(0.20, 0.93, '#rho=%1.2f #sigma_{x}=%2.0f #sigma_{y}=%2.0f' % (rho, sx, sy) )
            mytext.SetNDC();
            mytext.SetTextColor(ROOT.kBlue)
            mytext.SetTextSize(0.085)
            if SingleExample:
                mytext.SetTextSize(0.045)
            mytext.Draw()
            objs.append(mytext)
            print('Injected correlation: {:1.2f} Measured correlation: {:1.2f} sx={:2.0f}, sy={:2.0f}'.format(rho,h2.GetCorrelationFactor(), sx, sy) )
            # analyze the principal components:
            #principal.MakePrincipals()
            #lambdas = principal.GetEigenValues()
            #print( '  Eigenvalues: {:f}, {:f}'.format(lambdas[0], lambdas[1],))
            #vect = principal.GetEigenVectors()

            eigenvals = ROOT.TVectorD(2)
            Cov = ROOT.TMatrixD(2,2) #principal.GetCovarianceMatrix()
            # screw it, make the Cov by hand:
            Cov[0][0] = sx*sx
            Cov[1][1] = sy*sy
            Cov[1][0] = sx*sy*rho
            Cov[0][1] = Cov[1][0]
            vect = Cov.EigenVectors(eigenvals)
            print('  Eigenvalues: {:f}, {:f}'.format(eigenvals[0], eigenvals[1],))
            if sx > sy:
                # need to swap, as the eigen vectors are ordered in eigenvalues;)
                vect.Transpose(vect)
                sigmas.reverse()
                mus.reverse()
            print( '  eigenvector0: ({:f}, {:f})'.format(vect[0][0], vect[0][1], ) )
            print( '  eigenvector1: ({:f}, {:f})'.format(vect[1][0], vect[1][1], ) )
            axes = MakeEllipseAxes(mus, sigmas, vect, eigenvals)
            print( '   ...drawing axes of ellipses...' )
            for axis in axes:
                axis.SetLineColor(ROOT.kRed)
                axis.SetLineWidth(2+AddWidth)
                axis.SetLineStyle(1)
                axis.Draw()
            objs.append(axes)

            ells = MakeEllipses(mus, sigmas, vect, eigenvals)
            for ell in ells:
                ell.SetLineColor(ROOT.kGreen+1)
                ell.SetLineWidth(2+AddWidth)
                ell.SetLineStyle(2)
                ell.Draw()                
            objs.append(ells)
            
            prof = h2.ProfileX()
            Profs.append(prof)
            if not SingleExample:
                hcan.cd(ican+1)
            else:
                hcan.cd()
            h2.SetStats(0)
            h2.Draw('colz')
            mytext.Draw()
            prof.SetMarkerColor(ROOT.kBlack)
            prof.SetLineColor(ROOT.kBlack)
            prof.SetMarkerStyle(33)
            if SingleExample:
                prof.SetMarkerSize(1.)
            else:
                prof.SetMarkerSize(0.7)
            prof.Draw("e1sameX0")
            fun.Draw('same')
            diag.Draw()
            for axis in axes:
                axis.Draw()
            for ell in ells:
                ell.Draw()                

            hcan.Update()
            can.Update()
                            
    if Print:
        print( 'Printing to png/pdf...' )
        tag = ''
        if SingleExample:
            tag = '_example'
        print( 'Printing, this may take a while...' )
        print( 'Making pdfs...' )
        can.Print(can.GetName() + tag + '.pdf')
        hcan.Print(hcan.GetName() + tag + '.pdf')
        print( 'Making pngs...' )
        hcan.Print(hcan.GetName() + tag + '.png')
        can.Print(can.GetName() + tag + '.png')    

print( 'DONE!' )


# fit
#fitfun = ROOT.TF1('linfit', '[0]+[1]*x', xmin, xmax)
#fitfun.SetParameters(0.,1.)
#fitfun.SetNpx(npx)
#fun.SetLineColor(ROOT.kBlue)
#objs.append(fitfun)
#gr.Fit('linfit')
#chi2 = fun.GetChisquare()
#ndf = fun.GetNDF()
#if ndf > 0:
#    print( 'chi2/ndf = {:f} / %i = {:f}'.format(chi2, ndf, chi2/ndf, ) )
#fitfun.Draw('same')


ROOT.gApplication.Run()
