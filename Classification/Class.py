#!/usr/bin/python

# jiri kvita, 29.1.2018
# illustrational purposes only;)
import ROOT
#from myAll import *

from math import pi
import ctypes

lines = []
funs = []
Grs = []

cols = [ROOT.kRed, ROOT.kBlue]
marks = [32,26]

xmin = 0.
xmax = 10.
ymin = 0.
ymax = 10.

x0 = 0.
r1 = 4.
r2 = 10.
sx = 3.
sy = 3.
y0 = 0.
rho = 0.45

ROOT.gStyle.SetOptTitle(0)

unit = 400
name = 'ClassDemo'
can = ROOT.TCanvas(name, name, 0, 0, 3*unit,1*unit)
can.Divide(3,1)

# probability distribution for the signal
fun_sig = ROOT.TF2('fun_sig', '(sqrt(x^2+y^2) > [5]) * (sqrt(x^2+y^2) < [6]) * (y > 0) * ([5]-sqrt(x^2+y^2))*(sqrt(x^2+y^2)-[6])*[0]*exp(-(x-[1])^2/(2*[2]^2)-(y-[3])^2/(2*[4]^2)+[7]*(x-[1])*(y-[3])/([2]*[4]))', xmin, xmax, ymin, ymax)
fun_sig.SetParameters(1., x0, sx, y0, sy, r1, r2, rho)
funs.append(fun_sig)
gr_sig = ROOT.TGraph()
gr_sig.SetName('gr_sig')
Grs.append(gr_sig)

# probability distribution for the signal
fun_bg = ROOT.TF2('fun_bg', '(sqrt(x^2+y^2) < [5] )*[0]*exp(-(x-[1])^2/(2*[2]^2)-(y-[3])^2/(2*[4]^2)+[6]*(x-[1])*(y-[3])/([2]*[4]))', xmin, xmax, ymin, ymax)
fun_bg.SetParameters(1., x0, sx, y0, sy, r1*1.5, rho )
funs.append(fun_bg)
gr_bg = ROOT.TGraph()
gr_bg.SetName('gr_bg')
Grs.append(gr_bg)

Nsig = 300
Nbg = 2*Nsig
N = [Nsig, Nbg]

xx = ctypes.c_double(0.)
yy = ctypes.c_double(0.)

Data = []

ii=-1
for fun,n,gr,col,mark in zip(funs,N,Grs,cols,marks):
    data = []
    ii = ii+1
    ig = 0
    for i in range(0,Nsig):
        fun.GetRandom2(xx,yy)
        gr.SetPoint(ig,xx.value,yy.value)
        data.append([xx.value, yy.value])
        #print xx,yy
        ig = ig + 1
    gr.SetMarkerColor(col)
    gr.SetMarkerStyle(mark)
    #can.cd(ii+1)
    #fun.Draw('surf')
    Data.append(data)
# print Data

can.cd(1)
temp = ROOT.TH2D('tmp', 'tmp;x_{1};x_{2}', 100, xmin, xmax, 100, ymin, ymax)
temp.SetStats(0)

# separation graphics objects, for illustration:
Objs = []

# one line separator
line = ROOT.TLine(xmin, y0+2*sy, r1+sx, 0.)
Objs.append([line])

# two rectangular cuts:
line1 = ROOT.TLine(xmin, y0+sy, xmax, y0+sy)
line2 = ROOT.TLine(r1, ymin, r1, ymax)
Objs.append([line1, line2])

# circular cut:
rr = r1 + 0.35*sx
circ = ROOT.TEllipse(x0, y0, rr, rr, 0., 90.)
circ.SetFillStyle(0)
Objs.append([circ])

ican = 1
for obj in Objs:
    can.cd(ican)
    ican = ican+1
    temp.DrawCopy()
    for gr in Grs:
        gr.Draw('P')

    for oo in obj:
        oo.SetLineColor(ROOT.kBlack)
        oo.SetLineWidth(2)
        oo.SetLineStyle(1)
        oo.Draw()


# compute the empiraical means, use them as taus
#      H0, H1:
mux = [0., 0.]
muy = [0., 0.]
id = -1
for data in Data:
    id = id+1
    ts = []
    for evt in data:
        x = evt[0]
        y = evt[1]
        #print x,y
        mux[id] = mux[id] + x
        muy[id] = muy[id] + y

print(mux)
print(muy)
# normalize:
id = -1
for mx in mux:
    id = id+1
    mux[id] = mx / (1.*len(Data[id]))
id = -1
for my in muy:
    id = id+1
    muy[id] = my / (1.*len(Data[id]))
print(mux)
print(muy)
# construct the Fisher discriminant
Ts = []

tmin = -1
tmax = 6.
tbins = 28
h_t0 = ROOT.TH1D('t0', 't0;t', tbins, tmin, tmax)
h_t1 = ROOT.TH1D('t1', 't1;t', tbins, tmin, tmax)
h_ts = [h_t0, h_t1]
id = -1

# this is crude as this assumes gauss-distributed data, but
# let's try, simple and analytical;-)
a1 = 1./(1.-rho*rho) *(     (mux[0] - mux[1])/(sx*sx) - rho*(muy[0]-muy[1])/(sx*sy) )
a2 = 1./(1.-rho*rho) *( rho*(mux[0] - mux[1])/(sx*sy) +     (muy[0]-muy[1])/(sy*sy))
# test statistics separation cut:
tc = 2.65
a1 = a1*2.8
separationLine = ROOT.TF1('separationLine', '[0] + [1]*x', xmin, xmax)
separationLine.SetParameters(tc/a2, -a1/a2)
separationLine.SetLineColor(ROOT.kBlack)
separationLine.SetLineWidth(2)
separationLine.SetLineStyle(1)

for data in Data:
    id = id+1
    ts = []
    ig = 0
    for evt in data:
        x = evt[0]
        y = evt[1]
        t =  ( x * a1  + y*a2 )
        ts.append(t)
        h_ts[id].Fill(t)
        ig = ig+1
    Ts.append(ts)
    print(ts)


unit = 600
name = 'FisherDemo'
canF = ROOT.TCanvas(name, name, 0, 0, 2*unit, unit)
canF.Divide(2,1)
canF.cd(1)
temp.DrawCopy()
for gr in Grs:
    gr.Draw('P')
separationLine.Draw('same')

canF.cd(2)
opt = ''
id = -1
for h in h_ts:
    id = id+1
    h.SetMaximum(1.35*h.GetMaximum())
    h.SetStats(0)
    h.Draw(opt + 'hist')
    opt = 'same'
    #h.SetMarkerColor(cols[id])
    h.SetLineColor(cols[id])
    h.SetLineWidth(2)
    #h.SetMarkerStyle(marks[id])

    
can.Print(can.GetName()+'.pdf')
can.Print(can.GetName()+'.png')
canF.Print(canF.GetName()+'.pdf')
canF.Print(canF.GetName()+'.png')

ROOT.gApplication.Run()

