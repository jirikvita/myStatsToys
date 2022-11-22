# include <iostream>

#include "TF1.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TString.h"

#include "TStyle.h"
//#include "T.h"

using std::cout;
using std::cerr;
using std::endl; 


void fitGauss_params(int Ngen = 1000)

{

  
  TString fname = "myfun";
  TString formula = "[0]*exp(-(x-[1])^2 / (2*[2]^2))";
  double x1 = -5;
  double x2 = 5;

  TF1* fun = new TF1(fname, formula, x1, x2);
  fun -> SetParameters(1.,  0.,  2);

  TString hname = "myhist";
  TString title = "gauss rnd;x[aux];y[arb];";
  int nbins = 32;
  TH1D *h1 = new TH1D(hname, title, nbins, x1, x2);
  h1 -> FillRandom(fname, Ngen);

  int cw = 1000;
  int ch = 800;
  TString canname = "gfit";
  TCanvas *can = new TCanvas(canname, canname, 0, 0, cw, ch);
  can -> cd();
  h1 -> SetMarkerStyle(20);
  h1 -> SetMarkerSize(2);
  h1 -> SetMarkerColor(kBlack);

  gStyle -> SetOptFit(111);

  h1 -> Draw("e1");

  h1 -> Fit(fname);
  fun -> SetLineStyle(1);
  fun -> Draw("same");

  can -> Update();
  // as in printf
  can -> Print(TString(can -> GetName()) + Form("_%i.png", Ngen));
  can -> Print(TString(can -> GetName()) + Form("_%i.pdf", Ngen));
  

  //  gApplication -> Run();

}
