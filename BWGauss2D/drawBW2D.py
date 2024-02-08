#!/snap/bin/pyroot

import ROOT
import sys, os

from math import sqrt, pow

stuff = []

####################################################

# Jiri Kvita 8.2.2024
# upon question by Hana Zitnanska, Slovanske Gymnazium Olomouc

####################################################


def adjustStats(h):
    ROOT.gPad.Update()
    st = h.GetListOfFunctions().FindObject("stats")
    st = ROOT.gPad.GetPrimitive("stats")
    #st.SetX1NDC(0.7)
    #st.SetX2NDC(0.9)
    #st.SetY1NDC(0.65)
    #st.SetY2NDC(0.9)
    
    st.SetX1NDC(0.13)
    st.SetX2NDC(0.32)
    st.SetY1NDC(0.13)
    st.SetY2NDC(0.32)
    ROOT.gPad.Update()

    return st
    

####################################################
####################################################
####################################################

def drawBW2D(argv):
    
  ROOT.gStyle.SetOptTitle(0)

  m1 = 30.
  m2 = 120.
  m0 = 90
  sigma = 2
  sf = 2
  
  Nevts = 50000
  nb = 90
  npx1d = 1000
  npx2d = 100
  
  ####################################################
  # relativistic 2D
  nonrelbw2 = ROOT.TF2("nonrelbw2", "1/TMath::Pi() * [1]/2 / ( (x-[0])^2 + [1]^2/4 ) * 1/TMath::Pi() * [1]/2 / ( (y-[0])^2 + [1]^2/4 )", m1, m2, m1, m2)
  nonrelbw2.SetParameters(m0, sf*sigma)
  #nonrelbw2.Draw()
  #nonrelbw2.Draw("lego2")
  #nonrelbw2.Draw("surf")
  nonrelbw2.SetNpx(npx2d)
  nonrelbw2.SetNpy(npx2d)
  nonrelhh2 = ROOT.TH2D("2DnonrelBW", "2D non-rel. Breit-Wigner", nb, m1, m2, nb, m1, m2)
  nonrelhh2.FillRandom("nonrelbw2", Nevts)
  # nonrelhh2.SetStats(0)

  cname = "nonrelBW2"
  nonrelcan = ROOT.TCanvas(cname, cname)
  nonrelhh2.Draw("colz")
  st0 = adjustStats(nonrelhh2)
  ROOT.gPad.Update()
  

  
  ####################################################
  # relativistic 2D
  relbw2 = ROOT.TF2("relbw2", "[0]*1/( (x^2 - [1]^2)^2 + ([1]*[2])^2 ) * 1/( (y^2 - [1]^2)^2 + ([1]*[2])^2 )", m1, m2, m1, m2)
  relbw2.SetParameters(1., m0, sf*sigma)
  #relbw2.Draw()
  #relbw2.Draw("lego2")
  #relbw2.Draw("surf")
  relbw2.SetNpx(npx2d)
  relbw2.SetNpy(npx2d)
  relhh2 = ROOT.TH2D("2DBW", "2D relat. Breit-Wigner", nb, m1, m2, nb, m1, m2)
  relhh2.FillRandom("relbw2", Nevts)
  # relhh2.SetStats(0)

  cname = "relBW2"
  relcan = ROOT.TCanvas(cname, cname)
  relhh2.Draw("colz")
  st1 = adjustStats(relhh2)
  ROOT.gPad.Update()
  

  ####################################################
  # Voigtian 2D
  voigt2 = ROOT.TF2("voigt2", "TMath::Voigt(x - [0], [1], [1]) * TMath::Voigt(y - [0], [1], [1])", m1, m2, m1, m2)
  voigt2.SetParameters(m0, sigma)
  #voigt2.Draw()
  #voigt2.Draw("lego2")
  #voigt2.Draw("surf")
  voigt2.SetNpx(npx2d)
  voigt2.SetNpy(npx2d)
  voigthh2 = ROOT.TH2D("2DnonrelVoigt", "2D non-rel. Breit-Wigner", nb, m1, m2, nb, m1, m2)
  voigthh2.FillRandom("voigt2", Nevts)
  # voigthh2.SetStats(0)

  cname = "voigt2"
  voigtcan = ROOT.TCanvas(cname, cname)
  voigthh2.Draw("colz")
  st2 = adjustStats(voigthh2)
  ROOT.gPad.Update()
  


  
  ####################################################
  cname = "GG2"
  cang2 = ROOT.TCanvas(cname, cname)
  cang2.cd()
  
  g2 = ROOT.TF2("g2", "1/sqrt(2*TMath::Pi() * [1]^2) * exp( -(x-[0])^2/(2*[1]^2)) * 1/sqrt(2*TMath::Pi() * [1]^2) * exp( -(y-[0])^2/(2*[1]^2))", m1, m2, m1, m2)
  g2.SetParameters(m0, sigma)
  #g2.Draw()
  #g2.Draw("lego2")
  #g2.Draw("surf")
  g2.SetNpx(npx2d)
  g2.SetNpy(npx2d)
  gg2 = ROOT.TH2D("2DG", "2D Gauss", nb, m1, m2, nb, m1, m2)
  gg2.FillRandom("g2", Nevts)
  # gg2.SetStats(0)
  gg2.Draw("colz")
  st3 = adjustStats(gg2)
  ROOT.gPad.Update()
  
  ####################################################
  # 1D cmp
  
  cname = "BWGaussCmp"
  canbw2 = ROOT.TCanvas(cname, cname)
  canbw2.cd()

  # non-relativistic BW:
  nonrelBW = ROOT.TF1("relBW", "1/TMath::Pi() * [1]/2 / ( (x-[0])^2 + [1]^2/4 )", m1, m2)
  nonrelBW.SetParameters(m0, sf*sigma)

  # relativistic BW:
  # https://en.wikipedia.org/wiki/Relativistic_Breit%E2%80%93Wigner_distribution
  relBW = ROOT.TF1("relBW", "2*sqrt(2)*[0]^2*[1]*sqrt([0]^2+[1]^2)/(TMath::Pi()*sqrt([0]^2 + [0]*sqrt([0]^2+[1]^2))) * 1/( (x^2 - [0]^2)^2 + ([0]*[1])^2 )", m1, m2)
  relBW.SetParameters(m0, sf*sigma)

  # Gauss
  G = ROOT.TF1("G", "1/sqrt(2*TMath::Pi() * [1]^2) * exp( -(x-[0])^2/(2*[1]^2))", m1, m2)
  G.SetParameters(m0, sigma)

  # Voigt
  V = ROOT.TF1("V", "TMath::Voigt(x - [0], [1], [1])", m1, m2)
  V.SetParameters(m0, sqrt(sigma), sqrt(sigma))
  
  nonrelBW.SetNpx(npx1d)
  nonrelBW.SetLineColor(ROOT.kGreen+1)

  relBW.SetNpx(npx1d)
  relBW.SetLineColor(ROOT.kBlue)
  
  G.SetNpx(npx1d)
  G.SetLineColor(ROOT.kRed)

  V.SetNpx(npx1d)
  V.SetLineColor(ROOT.kBlack)
  
  
  G.Draw("")
  relBW.Draw("same")
  nonrelBW.Draw("same")
  V.Draw("same")
  
  ROOT.gPad.Update()

  
  stuff.append([nonrelBW, relBW, G, V,
                nonrelcan, relcan, voigtcan, cang2, canbw2,
                nonrelbw2, relbw2, g2, gg2,
                nonrelhh2, relhh2, voigthh2, st0, st1, st2, st3])
  

##########################################
def main(argv):
    drawBW2D(argv)
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

