
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

// ______________________________________________________________________


void MakeStyle()
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

}

// ______________________________________________________________________


TH1D *DivideHistoByTF(TH1D *hist, TF1 *fun, TString title = "", int mode = 0)
{
  if (not fun or not hist)
    return 0;

  TH1D *ratio = (TH1D*) hist -> Clone("ratio" + title); 
  ratio -> GetYaxis() -> SetTitle(title);
  //  ratio -> GetYaxis() -> SetMoreLogLabels(true);
  ratio -> Reset();

  for (int i = 1; i <= ratio -> GetXaxis() -> GetNbins(); ++i) {
    double val = hist -> GetBinContent(i) / fun -> Eval(hist -> GetBinCenter(i));
    double err = hist -> GetBinError(i) / fun -> Eval(hist -> GetBinCenter(i));
    if (mode > 0 and hist -> GetBinError(i) > 0.) {
      val = (hist -> GetBinContent(i) - fun -> Eval(hist -> GetBinCenter(i))) / hist -> GetBinError(i);
      err = 0.;
    }
    ratio -> SetBinContent(i, val);
    ratio -> SetBinError(i, err);
  }

  if (mode > 0) {
    ratio -> SetMaximum(5.);
    ratio -> SetMinimum(-5.);
  } else {
    ratio -> Scale(1.);
    //    ratio -> SetMaximum(5.);
    //    ratio -> SetMinimum(-5.);
  }

  ratio -> SetMarkerStyle(hist -> GetMarkerStyle());
  ratio -> SetMarkerColor(hist -> GetMarkerColor());
  ratio -> SetMarkerSize(hist -> GetMarkerSize());
    
  return ratio;
}

// ______________________________________________________________________

TCanvas* CreateFitResiduals(TH1D *hist, TF1 *fit)
{


  hist -> Fit(fit);
  hist -> Fit(fit);

  double bsize = 0.; // border size
  TCanvas *can = new TCanvas("datamcratio", "datamcratio", 0, 0, 600, 700);
  can -> Draw();

  TPad *pad1 = new TPad("pad1","histos",0.,0.66+bsize,1.,1.);
  pad1 -> SetBottomMargin(0.); // important!
  pad1 -> Draw();

  TPad *pad2 = new TPad("pad2","ratio",0.,0.33-bsize,1.,0.66-bsize);
  pad2 -> SetTopMargin(0.); // important!
  pad2 -> SetGridx(true);
  pad2 -> SetGridy(true);
  pad2 -> Draw();

  TPad *pad3 = new TPad("pad3","ratio",0.,0.,1.,0.33-bsize);
  pad3 -> SetTopMargin(0.); // important!
  pad3 -> SetGridx(true);
  pad3 -> SetGridy(true);
  pad3 -> Draw();

  hist -> SetStats(0);
  hist -> SetMarkerStyle(20);
  hist -> SetMarkerSize(1);
  hist -> SetMarkerColor(kBlack);

  double SF = 1.5; // 10. for logy?
  hist -> SetMaximum(SF * hist -> GetMaximum());
  hist -> SetMinimum(0.11);

  // draw
  pad1 -> cd();
  //  pad1 -> SetLogy();
  hist -> Draw("e1");
  fit -> Draw("same");

  // make fit residuals as ratio
  TH1D *hist3 = DivideHistoByTF(hist, fit, "Fit residuals", 0);
  //  hist3 -> SetLineColor(kBlue);
  //  hist3 -> SetLineStyle(2);
  //  hist3 -> SetLineWidth(2);
  //  hist3 -> SetFillColor(kYellow);
  //  hist3 -> SetFillStyle(1111);
  hist3 -> SetMarkerStyle(20);
  //hist3 -> SetMarkerSize(0.1);
  //double ymax = 25.;
  //double ymin = 0.2;
  //hist3 -> SetMaximum(ymax);
  //hist3 -> SetMinimum(ymin);

  pad2 -> cd();
  //  pad2 -> SetLogy();
  hist3 -> Draw("e");

  double x1 = hist -> GetXaxis() -> GetXmin();
  double x2 = hist -> GetXaxis() -> GetXmax();
  TLine *line1 = new TLine(x1, 1., x2, 1.);
  line1 -> SetLineColor(kRed);
  line1 -> Draw();
  

  // make fit residuals significance
  TH1D *hist4 = DivideHistoByTF(hist, fit, "Residuals significance", 1);
  hist4 -> SetFillStyle(0);
 
  pad3 -> cd();
  hist4 -> Draw("histsame");
  TLine *line0 = new TLine(x1, 0., x2, 0.);
  line0 -> SetLineColor(kRed);
  line0 -> Draw();

  TLine *linePlusOne = new TLine(x1, 1., x2, 1.);
  linePlusOne -> SetLineColor(kBlue);
  linePlusOne -> SetLineStyle(2);
  linePlusOne -> Draw();

  TLine *lineMinusOne = new TLine(x1, -1., x2, -1.);
  lineMinusOne -> SetLineColor(kBlue);
  lineMinusOne -> SetLineStyle(2);
  lineMinusOne -> Draw();


 //  gPad -> RedrawAxis();
  //  pad1 -> RedrawAxis();

  

  return can;

}

// ______________________________________________________________________
// ______________________________________________________________________
// ______________________________________________________________________

void FitResiduals(int Nevts = 1000)
{

  MakeStyle();

  double x1 = 0.;
  double x2 = 100.;
  int nbins = 20;

  TString form = "[0]*x^[1]*exp(-[2]*x)";
  TF1 *fun = new TF1("fun", form, x1, x2);
  fun -> SetParameters(Nevts, 2, 0.1);

  TF1 *fitfun = new TF1("fitfun", form, x1, x2);
  fitfun -> SetParameters(Nevts, 1.8, 0.11);


  TString axes = Form(";X;events / %3.1f GeV;", (x2-x1)/nbins);
  TH1D *hist = new TH1D("data", "data" + axes, nbins, x1, x2);
  hist -> SetDefaultSumw2();
  hist -> FillRandom("fun", Nevts);


  TCanvas *can = CreateFitResiduals(hist, fitfun);
  can -> Print("pretty.eps");
 
}

// ______________________________________________________________________
// ______________________________________________________________________
// ______________________________________________________________________
