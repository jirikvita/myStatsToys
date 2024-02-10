#!/usr/bin/python


from ROOT import *


rand = TRandom3()
a=0
b=1
tau = 1
N=10000

hists = []

u1 = 0
u2 = 20
hist = TH1D("gen", "gen", 100, u1, u2)
hists.append(hist)

for i in range(0,N):
    x = rand.Uniform(a,b)
    u = -1/tau * log(1-x)
    print(x,u)
    hist.Fill(u)

hist.Draw()
fun = TF1('fun', '[0]*exp(-[1]*x)', u1, u2)
fun.SetParameters(1, 1)
hist.Fit('fun')
gPad.SetLogy(1)
gApplication.Run()
