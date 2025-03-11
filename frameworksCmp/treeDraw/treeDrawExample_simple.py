#!/usr/bin/python

# jk 11.3.2025

import os, sys

import ROOT

ican = 1

hs = []

###############################################################

def adjustTitle(name, title):
    h = ROOT.gROOT.FindObject(name)
    h .SetTitle(title)
    return h

###############################################################

def cd(can):
  can.cd(globals()['ican'])
  globals()['ican'] += 1
  ROOT.gPad.SetLogz(1)


###############################################################

def drawHisto(tree, can, var, title, cuts = "", axisrange="", opt = ""):
# range can be e.g. "(50, 0, 5, 50, 0, 5)"

  cd(can)
  hname = can.GetName() + f"_histo{globals()['ican']}"

  # the drawing itself)
  tree.Draw(var + " >> " + hname + axisrange, cuts, opt)

  h = adjustTitle(hname, title)
  globals()['hs'].append(h)




###############################################################
def drawHisto1d(tree, can, var, cuts = "", axisrange="", title = ""):

    if title == "":
        title = cuts + (";" + var + ";Events").replace(".", " ")
    drawHisto(tree, can, var, title, cuts, axisrange, "hist")


###############################################################
def drawHisto2d(tree, can, varx, vary, cuts = "", axisrange="", title = ""):

  if title == "":
    title = cuts + (";" + varx + ";" + vary + ";Events").replace("."," ")
  var = vary + " : " + varx
  drawHisto(tree, can, var, title, cuts, axisrange, "colz")



###############################################################

def treeDraw():

  rfile = ROOT.TFile("output/ntuple_000409.root", "read")
  tree = rfile.Get("ACT0L")

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

  # vars
  t0  = "(TOF00.PeakTime + TOF01.PeakTime + TOF02.PeakTime + TOF03.PeakTime) / 4"
  t1  = "(TOF10.PeakTime + TOF11.PeakTime + TOF12.PeakTime + TOF13.PeakTime) / 4"

  can2 = ROOT.TCanvas("plots2d", "plots2d", 0, 0, 1200, 800)
  can2.Divide(3,2)
  globals()['ican'] = 1

  # fullest choice:
  # varx, vary, cuts, axisrange:
  drawHisto2d(tree, can2, "ACT3L.PeakVoltage", "ACT3L.IntCharge", "PbGlass.PeakVoltage > 0.5", "(50, 0, 3, 50, 0, 3)")
  drawHisto2d(tree, can2, "ACT3L.IntCharge", "ACT3R.IntCharge", "")
  drawHisto2d(tree, can2, "ACT2L.IntCharge", "ACT2R.IntCharge")
  drawHisto2d(tree, can2, "PbGlass.PeakVoltage", "ACT3L.IntCharge", "")
  drawHisto2d(tree, can2, "PbGlass.PeakVoltage", "ACT2L.IntCharge")
  drawHisto2d(tree, can2, "TOF00.PeakVoltage", "TOF10.PeakVoltage")
  # one can access last histogram by hs[-1]
  print(hs[-1])
  
  can1 = ROOT.TCanvas("plots1d", "plots1d", 200, 200, 1200, 800)
  can1.Divide(3,2)
  globals()['ican'] = 1
  drawHisto1d(tree, can1, "TOF00.PeakVoltage")
  drawHisto1d(tree, can1, "TOF11.PeakVoltage")
  drawHisto1d(tree, can1, "PbGlass.PeakVoltage", "PbGlass.PeakVoltage > 0.1")
  drawHisto1d(tree, can1, t1 + " - " + t0, "", "(40, 8, 28)", ";t1-t0 [ns]")
  drawHisto2d(tree, can1, t1 + " - " + t0, "PbGlass.PeakVoltage", "", "(40, 8, 28, 100, 0, 2.)", ";t1-t0 [ns];Lead Glass Peak Voltage")
  

  cans = [can1, can2]
  for can in cans:
      can.Update()
      can.Print(can.GetName() + '.png')

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

