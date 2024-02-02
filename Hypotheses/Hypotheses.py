#!/snap/bin/pyroot
##/usr/bin/python

# jiri kvita, 15.1.2018
# illustrational purposes only;)

#from myAll import *
import ROOT
stuff = []

tmin = 0.
tmax = 10.
tc = 5.2
tobs = 5.8

ROOT.gStyle.SetOptTitle(0)

# probability distribution for the test statistics given H_0 is true:
tstat0 = ROOT.TF1('tstat0', '[0]*(x-[2])*(x-[3])*exp(-[1]*(x-[1]))', tmin, tmax)
tstat0.SetParameters(-1., 0.55, tmin, tmax)
tstat0.SetParameter(0, tstat0.GetParameter(0) / tstat0.Integral(tmin, tmax) )
tstat0.SetLineColor(ROOT.kRed)
tstat0.SetLineStyle(1)
tstat0.SetLineWidth(2)
tstat0.SetNpx(200)
print(tstat0.Integral(tmin, tmax))

# hashed from tc to tmax:
tstat0_tc = ROOT.TF1('tstat0_tc', '[0]*(x-[2])*(x-[3])*exp(-[1]*(x-[1]))', tobs, tmax)
for i in range(0,tstat0.GetNpar()):
    tstat0_tc.SetParameter(i,tstat0.GetParameter(i))
tstat0_tc.SetFillStyle(3005)
tstat0_tc.SetFillColor(tstat0.GetLineColor())
tstat0_tc.SetLineColor(tstat0_tc.GetFillColor())


# hashed from tobs to tmax:
tstat0_tobs = ROOT.TF1('tstat0_tobs', '[0]*(x-[2])*(x-[3])*exp(-[1]*(x-[1]))', tc, tmax)
for i in range(0,tstat0.GetNpar()):
    tstat0_tobs.SetParameter(i,tstat0.GetParameter(i))
tstat0_tobs.SetFillStyle(3004)
tstat0_tobs.SetFillColor(tstat0.GetLineColor())
tstat0_tobs.SetLineColor(tstat0_tobs.GetLineColor())

tstat1 = ROOT.TF1('tstat1', '[0]*(x-[2])*(x-[3])*exp(-[1]*([3]-x+[2]))', tmin, tmax)
tstat1.SetParameters(-1, 0.45, tmin, tmax)
tstat1.SetParameter(0, tstat1.GetParameter(0) / tstat1.Integral(tmin, tmax) )
tstat1.SetLineColor(ROOT.kBlue)
tstat1.SetLineStyle(2)
tstat1.SetNpx(200)
tstat1.SetLineWidth(2)
print(tstat1.Integral(tmin, tmax))

# hashed from tmin to tc
tstat1_tc = ROOT.TF1('tstat1_tc', '[0]*(x-[2])*(x-[3])*exp(-[1]*([3]-x+[2]))', tmin, tc)
for i in range(0,tstat1.GetNpar()):
    tstat1_tc.SetParameter(i,tstat1.GetParameter(i))
tstat1_tc.SetFillStyle(3005)
tstat1_tc.SetFillColor(tstat1.GetLineColor())
tstat1_tc.SetLineColor(tstat1.GetLineColor())

name = 'HypoDemo'
can = ROOT.TCanvas(name, name, 0, 0, 1200,800)
#can.Divide(2,2)
#can.cd(1)

can.cd()
tstat0.Draw('')
tstat1.Draw('same')

yy = 0.15
dy = 0.012
dx = 0.175

line_tc = ROOT.TLine(tc, 0, tc, yy)
line_tc.SetLineColor(ROOT.kBlack)
line_tc.SetLineWidth(2)
line_tc.SetLineStyle(1)
t_tc = ROOT.TLatex(tc-dx, yy+dy, 't_{c}')

line_tc.Draw()
t_tc.Draw()

line_tobs = ROOT.TLine(tobs, 0, tobs, yy)
line_tobs.SetLineColor(ROOT.kBlack)
line_tobs.SetLineWidth(2)
line_tobs.SetLineStyle(2)
t_obs = ROOT.TLatex(tobs-dx, yy+dy, 't_{obs}')

# axes lmits:
dy = 0.025
#t_min = ROOT.TLatex(tmin-dx, 0.-dy, 't_{min}')
#t_max = ROOT.TLatex(tmax-dx, 0.-dy, 't_{max}')
t_max = ROOT.TLatex(tmax-2*dx, 0.-dy, 't')
#t_min.Draw()
t_max.Draw()

line_tobs.Draw()
t_obs.Draw()


gH0 = ROOT.TLatex(3., 0.22, 'g(t|H_{0})')
gH0.SetTextColor(tstat0.GetLineColor())
gH0.Draw()

gH1 = ROOT.TLatex(6., 0.22, 'g(t|H_{1})')
gH1.SetTextColor(tstat1.GetLineColor())
gH1.Draw()

#ROOT.gPad.SetGridx() ; ROOT.gPad.SetGridy()

print('Drawing filled...')
tstat0_tc.Draw('same')
tstat0_tobs.Draw('same')
tstat1_tc.Draw('same')
stuff.append([tstat0_tc, tstat0_tobs])
stuff.append(tstat1_tc)



can.Update()

can.Print(can.GetName()+'.pdf')
can.Print(can.GetName()+'.png')

ROOT.gApplication.Run()

