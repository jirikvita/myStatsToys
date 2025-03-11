#!/usr/bin/python

# jk 11.3.2025
# using WCTE test beam data 2023


import os, sys
import ROOT

# globals
ican = 1
hs = []

###############################################################
def adjustStats(h):
    ROOT.gPad.Update()
    st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    st.SetX1NDC(0.7)
    st.SetX2NDC(0.9)
    st.SetY1NDC(0.65)
    st.SetY2NDC(0.9)
    
###############################################################
def adjustTitle(name, title):
    h = ROOT.gROOT.FindObject(name)
    h.SetTitle(title)
    adjustStats(h)
    return h


###############################################################

def cd(can):
  can.cd(globals()['ican'])
  globals()['ican'] += 1
  ROOT.gPad.SetLogz(1)


###############################################################

def drawHisto(tree, can, var, opt, **kwargs):
  # range can be e.g. "(50, 0, 5, 50, 0, 5)"
  cd(can)
  hname = can.GetName() + f"_histo{globals()['ican']}"

  cuts = ''
  if 'cuts' in kwargs:
      cuts = kwargs['cuts']
      
  title = ''
  if 'title' in kwargs:
      title = kwargs['title']

  bins = ''
  if 'bins' in kwargs:
      bins = kwargs['bins']

      
  # the drawing itself)
  tree.Draw(var + " >> " + hname + bins, cuts, opt)

  h = adjustTitle(hname, title)
  globals()['hs'].append(h)

###############################################################
def drawHisto1d(tree, can, var, **kwargs):
    if not 'title' in kwargs:
        title = ''
        cuts = ''
        if 'cuts' in kwargs:
            cuts = kwargs['cuts']
        title = cuts + (";" + var + ";Events").replace(".", " ")
        kwargs['title'] = title
    drawHisto(tree, can, var, "hist", **kwargs)
    
###############################################################
def drawHisto2d(tree, can, varx, vary, **kwargs):
  #print(kwargs)
  if not 'title' in kwargs:
      title = ''
      cuts = ''
      if 'cuts' in kwargs:
          cuts = kwargs['cuts']
      title = cuts + (";" + varx + ";" + vary + ";Events").replace("."," ")
      kwargs['title'] = title
  var = vary + " : " + varx
  drawHisto(tree, can, var, "colz", **kwargs)

###############################################################

def treeDraw():

  rfile = ROOT.TFile("output/ntuple_000409.root", "read")
  tree = rfile.Get("ACT0L")
  ROOT.gStyle.SetPalette(1)

  friendNames = ["ACT0R",
		 "ACT1L", "ACT1R",
		 "ACT2L", "ACT2R",
		 "ACT3L", "ACT3R",
		 "TOF00", "TOF01", "TOF02", "TOF03",
		 "TOF10", "TOF11", "TOF12", "TOF13",
		 "Hole0", "Hole1",
		 "PbGlass"
                 ]
  

  for friendName in friendNames:
    tree.AddFriend(friendName)

  # combined variables:
  # average time in T0 and T1
  t0  = "(TOF00.PeakTime + TOF01.PeakTime + TOF02.PeakTime + TOF03.PeakTime) / 4"
  t1  = "(TOF10.PeakTime + TOF11.PeakTime + TOF12.PeakTime + TOF13.PeakTime) / 4"
  # time of flight
  t1_minus_t0 = t1 + "-" + t0
  # 1 peak in all TOF PMTs:
  OneTofPeak = '(TOF00.nPeaks == 1 && TOF01.nPeaks == 1 && TOF02.nPeaks == 1 && TOF03.nPeaks == 1 && TOF10.nPeaks == 1 && TOF11.nPeaks == 1 && TOF12.nPeaks == 1 && TOF13.nPeaks == 1)'

  act_group2 = "ACT3L.IntCharge + ACT3R.IntCharge + ACT2L.IntCharge + ACT2R.IntCharge"
  act_group1 = "ACT1L.IntCharge + ACT1R.IntCharge"
  
  can2 = ROOT.TCanvas("plots2d", "plots2d", 0, 0, 1400, 1200)
  can2.Divide(3,3)
  globals()['ican'] = 1

  # fullest choice: varx, vary, cuts, bins, title:
  drawHisto2d(tree, can2, "ACT3L.PeakVoltage", "ACT3L.IntCharge", cuts="PbGlass.PeakVoltage > 0.5", bins="(50, 0, 3, 50, 0, 3)")
  drawHisto2d(tree, can2, "ACT3L.IntCharge", "ACT3R.IntCharge")
  drawHisto2d(tree, can2, "ACT2L.IntCharge", "ACT2R.IntCharge")
  drawHisto1d(tree, can2, "ACT3L.IntCharge - ACT3R.IntCharge", bins='(50, -1, 1)')
  drawHisto2d(tree, can2, "PbGlass.PeakVoltage", "ACT3L.IntCharge")
  drawHisto2d(tree, can2, "PbGlass.PeakVoltage", "ACT2L.IntCharge")
  drawHisto2d(tree, can2, "TOF00.PeakVoltage", "TOF10.PeakVoltage")
  # one can access last histogram by hs[-1]
  # print(hs[-1])

  can1 = ROOT.TCanvas("plots1d", "plots1d", 200, 200, 1200, 800)
  can1.Divide(3,2)
  globals()['ican'] = 1
  #drawHisto1d(tree, can1, "TOF00.PeakVoltage")
  #drawHisto1d(tree, can1, "TOF11.PeakVoltage")
  drawHisto1d(tree, can1, "PbGlass.PeakVoltage", cuts="PbGlass.PeakVoltage > 0.1")
  drawHisto1d(tree, can1, t1_minus_t0, bins="(40, 8, 28)", title=";t1-t0 [ns]")
  #drawHisto2d(tree, can1, t1_minus_t0, "PbGlass.PeakVoltage", bins="(40, 8, 28, 100, 0, 2.)", title=";t1-t0 [ns];Lead Glass Peak Voltage")
  drawHisto2d(tree, can1, t1_minus_t0, "PbGlass.PeakVoltage", cuts=OneTofPeak, bins="(40, 8, 28, 100, 0, 2.)", title=";t1-t0 [ns];Lead Glass Peak Voltage")
  drawHisto2d(tree, can1, t1_minus_t0, act_group2, cuts=OneTofPeak, bins="(40, 8, 28, 100, 0, 2.)", title=";t1-t0 [ns];ACT 2+3 Charge")
  drawHisto2d(tree, can1, "PbGlass.PeakVoltage", act_group2, cuts=OneTofPeak + ' && (' + act_group2 + ' > 0.01)', title=";Lead Glass Peak Voltage;ACT group2 Charge")
  drawHisto2d(tree, can1, act_group1, act_group2, cuts=OneTofPeak + ' && (' + act_group2 + ' > 0.01)', bins="(50, 0., 0.5, 50, 0, 3.)", title=";ACT group1 Charge;ACT group2 Charge")

  # printing
  cans = [can1, can2]
  for can in cans:
      can.Update()
      can.Print(can.GetName() + '.png')
      can.Print(can.GetName() + '.pdf')

  return rfile, hs, cans

###############################################################

def main(argv):
    rfile, hs, cans = treeDraw()
    ROOT.gApplication.Run()
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

