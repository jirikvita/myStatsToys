
#include <iostream>
#include <fstream>
#include <string>
#include <vector>


using std::endl;
using std::cerr;
using std::cout;


/*
#include "RooDataSet.h"
#include "RooFormulaVar.h"
#include "RooPlot.h"
#include "RooArgSet.h"
#include "RooGlobalFunc.h"
*/

#include "TLine.h"
#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TMath.h"
#include "TCanvas.h"
#include "TLatex.h"
#include "TSystem.h"
#include "TStyle.h"
#include "TLegend.h"

#include "TH1D.h"
#include "TH2D.h"
#include "TH1F.h"
#include "TH2F.h"

#include "TF1.h"
#include "TGraphErrors.h"



void MultiplePads()
{

  gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetFrameBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetCanvasColor(0);
  //  gStyle->SetTitleColor(0);
  gStyle->SetStatColor(0);

  gStyle->SetPadRightMargin(0.07);
  gStyle->SetPadLeftMargin(0.10);
  gStyle->SetPadBottomMargin(0.16);

  gStyle->SetPalette(1);
  gStyle->SetFillColor(10);
  gStyle->SetOptTitle(0);
  gStyle->SetTitleOffset(0.9,"X");
  gStyle->SetTitleOffset(0.7,"Y");
  gStyle->SetTitleXSize(0.06); 
  gStyle->SetTitleYSize(0.06); 
  gStyle->SetTitleFontSize(0.06); 
  gStyle->SetFrameLineColor(1);

  double bsize = 0.;
  TCanvas *can = new TCanvas("datamcratio", "datamcratio", 0, 0, 600, 700);
  can -> Draw();
  TPad *pad1 = new TPad("pad1","histos",0.,0.50+bsize,1.,1.);
  pad1 -> SetBottomMargin(0.); // important!
  TPad *pad2 = new TPad("pad2","ratio",0.,0.,1.,0.50-bsize);
  pad2 -> SetTopMargin(0.); // important!
  pad2 -> SetGridx(true);
  pad2 -> SetGridy(true);

  pad1 -> Draw();
  pad2 -> Draw();

  double x1 = 0.;
  double x2 = 100.;
  int nbins = 20;

  TString form = "[0]*x^[1]*exp(-[2]*x)";
  TF1 *fun1 = new TF1("fun1", form, x1, x2);
  fun1 -> SetParameters(1000, 2, 0.1);
  TF1 *fun2 = new TF1("fun2", form, x1, x2);
  fun2 -> SetParameters(1000, 1.8, 0.11);


  int N = 1000;
  TString axes = Form(";p_{T};events / %3.1f GeV;", (x2-x1)/nbins);
  TH1F *hist1 = new TH1F("data", "data" + axes, nbins, x1, x2);
  hist1 -> SetDefaultSumw2();
  hist1 -> FillRandom("fun1", N);
  hist1 -> SetStats(0);
  TH1F *hist2 = new TH1F("MC", "MC", nbins, x1, x2);
  // not needed after the default static method called above;  hist2 -> Sumw2();
  hist2 -> FillRandom("fun2", 10*N);
  hist2 -> SetStats(0);
  hist2 -> Scale( hist1 -> Integral() / hist2 -> Integral() );

  hist1 -> SetMarkerStyle(20);
  hist1 -> SetMarkerSize(1);
  hist1 -> SetMarkerColor(kBlack);

  hist2 -> SetLineColor(kRed);
  hist2 -> SetLineWidth(1);

  pad1 -> cd();
  pad1 -> SetLogy();
  double SF = 10.;
  hist1 -> SetMaximum(SF * hist1 -> GetMaximum());
  hist1 -> SetMinimum(0.11);
  hist1 -> Draw("e1");
  hist2 -> Draw("histsame");

  TH1F *hist3 = (TH1F*) hist1 -> Clone("data/MC");
  hist3 -> GetYaxis() -> SetTitle("ratio");
  hist3 -> GetYaxis() -> SetMoreLogLabels(true);
  hist3 -> Divide(hist2);
  hist3 -> SetLineColor(kBlue);
  hist3 -> SetLineStyle(2);
  hist3 -> SetLineWidth(2);
  hist3 -> SetFillColor(kYellow);
  hist3 -> SetFillStyle(1111);
  hist3 -> SetMarkerStyle(20);
  hist3 -> SetMarkerSize(0.1);
  double ymax = 25.;
  double ymin = 0.2;
  hist3 -> SetMaximum(ymax);
  hist3 -> SetMinimum(ymin);

  pad2 -> cd();
  pad2 -> SetLogy();
  hist3 -> Draw("e2");
  TH1F *hist4 = (TH1F*) hist3 -> Clone("ratio2");
  hist4 -> SetFillStyle(0);
  hist4 -> Draw("histsame");
  gPad -> RedrawAxis();
  pad1 -> RedrawAxis();

  pad2 -> cd();
  TLine *line = new TLine(x1, 1., x2, 1.);
  line -> SetLineColor(kRed);
  line -> Draw();
  
  can -> Print("pretty.eps");

}
