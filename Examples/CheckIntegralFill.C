// jiri kvita 5.6.2013
// usage: 
// root -l 'CheckIntegralFill.C+(0, true)'
// root -l 'CheckIntegralFill.C+(0, false)'
// where is the problem, i.e. why are the integrals of the histograms, filled with the same events and weighrs, different?? See also the effect of guarding th over/under-flows.

#include "StandardRootIncludes.h"

TRandom3 *grand = 0;

// ________________________________________________________________

void MyFill(TH1F *h, float val, double weight)
{
  if (val >= h -> GetXaxis() -> GetBinUpEdge(h -> GetXaxis() -> GetNbins()))
    val = h -> GetXaxis() -> GetBinCenter(h -> GetXaxis() -> GetNbins()); 
  if (val <= h -> GetXaxis() -> GetBinLowEdge(1))
    val = h -> GetXaxis() -> GetBinCenter(1);   
  h -> Fill(val, weight);
}

// ________________________________________________________________
// ________________________________________________________________
// ________________________________________________________________

void CheckIntegralFill(int debug = 0, bool UseNormalFill = false)
{
  
  gStyle -> SetPalette(1);
  gStyle -> SetCanvasColor(0);
  
  const int Nbins = 4;
  const int Nfinebins = 100;
  double min = 0.;
  double max = 800;
  grand = new TRandom3();
  grand -> SetSeed(8736542);

  double bins[] = {min, 100, 300., 550., max};

  TH1F *histo_fine = new TH1F("fine", "fine", Nfinebins, min, max);
  TH1F *histo_coarse1 = new TH1F("coarse1", "coarse1", Nbins, min, max);
  TH1F *histo_coarse2 = new TH1F("coarse2", "coarse2", Nbins, (double*)bins);
  TH1F *histo_onebin = new TH1F("onebin", "onebin", 2, min, max);
  histo_fine -> SetLineColor(kRed);
  histo_coarse1 -> SetLineColor(kBlue);
  histo_coarse2 -> SetLineColor(kBlack);
  histo_onebin -> SetLineColor(kMagenta);

  int Nevts = 600000;
  double weight = 0.171043;
  for (int i = 0; i < Nevts; i++) {
    double val =  TMath::Abs(grand -> Gaus(100.,200.));
    // weight =  TMath::Abs(grand -> Gaus(0,1.));
    // weight =  // floor(10.*weight) / 10.;
   

    if (UseNormalFill) {
      histo_fine -> Fill(val, weight);
      histo_coarse1 -> Fill(val, weight);
      histo_coarse2 -> Fill(val, weight);
      histo_onebin -> Fill(val, weight);
    } else {
      MyFill(histo_fine, val, weight);
      MyFill(histo_coarse1, val, weight);
      MyFill(histo_coarse2, val, weight);
      MyFill(histo_onebin, val, weight);
    }
  }

    TCanvas *can1 = new TCanvas("master1", "master1", 800, 100, 600, 400);
    can1 -> cd();
    histo_coarse1 -> Draw("e1hist");
    histo_fine -> Draw("e1histsame");
    histo_coarse2 -> Draw("e1histsame");

    cout << "Forced under/overflows inside: " << (not UseNormalFill) << endl;

  cout << "Fine:    I=" << histo_fine -> Integral() << endl;  
  cout << "Coarse1: I=" << histo_coarse1 -> Integral() << endl;  
  cout << "Coarse2: I=" << histo_coarse2 -> Integral() << endl;  
  cout << "OneBin I=" << histo_onebin -> Integral() << endl;  
  cout << " Ratios to fine: Coarse1/Fine=" << histo_coarse1 -> Integral() /  histo_fine -> Integral()
       << " Coarse2/Fine=" << histo_coarse2 -> Integral() /  histo_fine -> Integral()
       << " OneBin/Fine=" << histo_onebin -> Integral() /  histo_fine -> Integral()
       << endl;
  cout << "Theoretical integral=" << Nevts*weight << endl;
  cout << "Fine/Theory=" <<  histo_fine -> Integral()  / ( Nevts*weight) << endl;


  cout << "DONE!;-)" << endl;

}

// ________________________________________________________________

