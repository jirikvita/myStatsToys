#!/usr/bin/python

# jiri kvita, 30.9.2014, 14.10.2015



from myAll import *
from PdfTools import *
from GraphicsTools import *


############################################
canname = "GaussCauchy"
can = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)
#can.Divide(2,2)
#can.cd(1)
ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

xmin = -5
xmax = 5

gaus = MakeGauss('Gauss', xmin, xmax, 0, 1)
SetColStyle(gaus, ROOT.kRed, 1, 2)

cauchy = MakeCauchy('Cauchy', xmin, xmax, 0, 1)
SetColStyle(cauchy, ROOT.kBlue, 2, 3)

student = MakeStudent('Student', xmin, xmax, 1)
SetColStyle(student, ROOT.kBlack, 4, 3)

cauchy.Draw()
gaus.Draw("same")
student.Draw("same")

leg = nextCan.nextLeg(0.64,0.70, 0.88, 0.88)
gopt = 'L'
leg.AddEntry(cauchy, 'Cauchy', gopt)
leg.AddEntry(gaus, 'Gauss', gopt)
leg.AddEntry(student, 'Student', gopt)
leg.Draw()

can.Print("GaussCauchy" + ".png")
can.Print("GaussCauchy" + ".pdf")
can.SetLogy(1)
can.Print(can.GetName() + "_log.png")
can.Print(can.GetName() + "_log.pdf")

############################################
# Poisson-Gauss
canname = "PoissonGauss"
canP = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)
#canP.Divide(2,2)
#canP.cd(1)
#ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

xmin = 1
xmax = 100
Poiss = []
Gauss = []
Mu = [1., 5., 10., 30., 50.]
Col = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+2]
Mark = [20, 21, 22, 23, 33]
DualMark = {i : i+4 for i in range(20, 24)}
DualMark[33] = 27

legP = nextCan.nextLeg(0.3,0.65, 0.5, 0.88)
legP.SetHeader('Poisson')
legG = nextCan.nextLeg(0.52,0.65, 0.75, 0.88)
legG.SetHeader('Gauss')

popt = 'Psame'
gopt = 'L'
for col,mark,mu in zip(Col,Mark,Mu):
    Gauss.append(MakeGauss('gauss%f' % (mu,), xmin, xmax, mu, math.sqrt(mu)) )
    SetColStyle(Gauss[-1],col,2)
    #SetMarkStyle(Gauss[-1],col,mark)
    Gauss[-1].Draw(gopt)
    Gauss[-1].GetHistogram().GetXaxis().SetMoreLogLabels()
    Gauss[-1].GetXaxis().SetMoreLogLabels()
    gopt = 'Lsame'
    legG.AddEntry(Gauss[-1], '#sigma=%2.1f #mu=%2.2f' % (mu,math.sqrt(mu),), 'L')

    Poiss.append( MakePoisson('pois%f' % (mu,), xmin, xmax, mu) )
    SetColStyle(Poiss[-1],col)
    SetMarkStyle(Poiss[-1],col,mark)
    Poiss[-1].Draw(popt)
    legP.AddEntry(Poiss[-1], '#mu=%2.1f' % (mu,), 'P')


legP.Draw()
legG.Draw()
canP.Print(canP.GetName() + ".png")
canP.Print(canP.GetName() + ".pdf")

canP.SetLogx(1)
canP.SetLogy(1)
Gauss[0].SetMaximum(1e10)
Gauss[0].SetMinimum(1e-17)
Gauss[0].GetHistogram().GetXaxis().SetMoreLogLabels()
Gauss[0].GetXaxis().SetMoreLogLabels()
ROOT.gPad.Update()
canP.Print(canP.GetName() + "_log.png")
canP.Print(canP.GetName() + "_log.pdf")



############################################
# Binomial-Poisson-Gauss

canname = "BinomialPoisson"
canB = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)

canname = "BinomialGauss"
canBG = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)

Pois = []
Binomial = []
BinomialClone = []
Gaus = []
N = [2, 5, 10, 30, 100]
Col = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+2]

legP = nextCan.nextLeg(0.3,0.65, 0.5, 0.88)
legP.SetHeader('Poisson')
legB = nextCan.nextLeg(0.52,0.65, 0.75, 0.88)
legB.SetHeader('Binomial')
legG = nextCan.nextLeg(0.3,0.65, 0.5, 0.88)
legG.SetHeader('Gauss')

nb = 100
nmax = 50 
htmp = ROOT.TH2D('htmp', 'htmp', nb, 0, nmax, nb, 0, 0.75)
htmp.SetStats(0)
htmp.GetXaxis().SetMoreLogLabels()

canB.cd()
htmpB = htmp.DrawCopy()

canBG.cd()
htmpBG = htmp.DrawCopy()

Hists = []
Hists.append(htmp)

gopt = 'Lsame'
popt = 'CP'
bopt = 'CP'
prob = 0.25
for col,mark,n in zip(Col,Mark,N):
    Binomial.append(MakeBinomial('binom%i_%f' % (n,prob,), n, prob, ) )
    SetMarkStyle(Binomial[-1],col,mark)
    SetColStyle(Binomial[-1],col,1)
    legB.AddEntry(Binomial[-1], 'n=%i p=%1.2f' % (n,prob,), 'LP') 
    
    mu = n*prob
    Pois.append( MakePoisson('pois%f' % (mu,), xmin, xmax, mu) )
    SetMarkStyle(Pois[-1],col,DualMark[mark])
    SetColStyle(Pois[-1],col,2)
    legP.AddEntry(Pois[-1], '#mu=%2.1f' % (mu,), 'LP')

    sigma = math.sqrt(n*prob*(1-prob))
    Gaus.append(MakeGauss('gaus%f' % (mu,), xmin, xmax, mu, sigma) )
    SetColStyle(Gaus[-1],col,2)
    legG.AddEntry(Gaus[-1], '#sigma=%2.1f #mu=%2.1f' % (mu,sigma,), 'L')
    
    canB.cd()
    Binomial[-1].Draw(bopt)
    Pois[-1].Draw(popt)

    canBG.cd()
    BinomialClone.append(Binomial[-1].Clone(Binomial[-1].GetName() + '_clone'))
    BinomialClone[-1].Draw(bopt)
    Gaus[-1].Draw(gopt)

    gopt = 'Lsame'
    
canB.cd()    
legP.Draw()
legB.Draw()
canB.Print(canB.GetName() + ".png")
canB.Print(canB.GetName() + ".pdf")
canB.SetLogx(1)
#htmpB.GetXaxis().SetMoreLogLabels()
canB.Print(canB.GetName() + "_log.png")
canB.Print(canB.GetName() + "_log.pdf")


canBG.cd()    
legG.Draw()
legB.Draw()
canBG.Print(canBG.GetName() + ".png")
canBG.Print(canBG.GetName() + ".pdf")
canBG.SetLogx(1)
#htmpBG.GetXaxis().SetMoreLogLabels()
canBG.Print(canBG.GetName() + "_log.png")
canBG.Print(canBG.GetName() + "_log.pdf")


############################################
canname = "Chi2"
can = nextCan.nextTCanvas(canname, canname, 0, 0, 800, 800)
ROOT.gPad.SetGridx()
#ROOT.gPad.SetGridy()

xmin = 0.
xmax = 9.5
cols = [ROOT.kRed, ROOT.kBlack, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta]
legc = nextCan.nextLeg(0.64,0.70, 0.88, 0.88)
gopt = 'L'
opt=''
Chi2 = []
N = [1, 2, 3, 4, 5]
for col,n in zip(cols,N):
    name = 'Chi2{:}'.format(n)
    chi2 = MakeChi2(name, xmin, xmax, n)
    chi2.SetNpx(200)
    Chi2.append(chi2)
    print chi2.GetTitle(), chi2.GetParameter(0)
    SetColStyle(chi2, col, 1, 2)
    chi2.Draw(opt)
    opt = 'same'
    legc.AddEntry(chi2, '#chi^{2}(x,%i)' % (n,), gopt)
legc.Draw()


can.Print("Chi2" + ".png")
can.Print("Chi2" + ".pdf")
can.SetLogy(1)
can.Print(can.GetName() + "_log.png")
can.Print(can.GetName() + "_log.pdf")


############################################


ROOT.gApplication.Run()
