// jiri kvita 8.4.2013
// usage: root -l RunToyCovariance.C+
// root -l 'RunToyCovariance.C+(1, true, 0)'
// root -l 'RunToyCovariance.C+(1, true, 1)'

#include "StandardRootIncludes.h"
#include "ToyCovariance.C"
#include "Utils.C"

TRandom3 *grand = 0;

// ________________________________________________________________
// 2019:
TH2D *MakeCorrHisto(TMatrixD *m, TString name = "hCorr2D", TString title = "")
{

  if (!m)
    return 0;
  if (name == "")
    name = "Corr2D";
  if (title == "")
    title = name;
  
  int nrows = m->GetNrows();
  int ncols = m->GetNcols();

  cout << "OK, got " << nrows << " rows and " << ncols << " columns!" << endl;
  
  TH2D *h2 = new TH2D(name, title, ncols, 0, ncols, nrows, 0, nrows);
    
  for (int i = 0; i < nrows; ++i) {
    for (int j = 0; j < ncols; ++j) {
      double val = (*m)[i][j];
      cout << " " << val << " ";
      h2 -> SetBinContent(j+1, i+1, val);
    }
    cout << endl;
  }
  h2 -> Scale(1.);
  return h2;
  

}

// ________________________________________________________________


TH1D* GetSmeared(TH1D *hist)
{
  if (not hist)
    return 0;
  TH1D *toy = (TH1D*)hist ->Clone("mytoy");
  toy->Reset();
  for (int i = 1; i <= hist->GetXaxis()->GetNbins(); i++) {
    toy -> SetBinContent(i, hist->GetBinContent(i) + grand -> Gaus(0, hist->GetBinError(i)));
    toy -> SetBinError(i, hist->GetBinError(i));
  }
  toy -> Scale(1.);
  return toy;
}

// ________________________________________________________________


TH1D* GetSmearedSpecial(TH1D *hist)
{
  if (not hist)
    return 0;
  TH1D *toy = (TH1D*)hist ->Clone("mytoy");
  toy->Reset();
  int Nbins = hist->GetXaxis()->GetNbins();
    // main correlation over bins, coherent shift over bins:
  double rand = grand -> Gaus(0, 0.75);
  double sign = -1;
  for (int i = 1; i <= Nbins; i++) {
    // smear little bit independently in each bin as well:
    double rand2 = grand -> Gaus(0, 0.25);
    // size of the main shift:
    double corr = 0.15;
    // flip the correlation sign over bins, see the sign of the measure correlations as a cross-check all works fine;)
    //for (int k = 0; k < i;++k)
    sign *= -1;
    toy -> SetBinContent(i, hist->GetBinContent(i) + sign*i*(rand*corr+rand2)*hist->GetBinError(i));
    toy -> SetBinError(i, hist->GetBinError(i));
  }
  toy -> Scale(1.);
  return toy;
}


// ________________________________________________________________

void RunToys(TCanvas *can1, int Ntoys, int Nbins, TH1D *master, TH2D *alltoys,  bool InjectCorrelation, ToyCovariance *toy, int debug, int Mode)
{

  cout << "OK, running "<< Ntoys << " toys..." << endl;
  cout << " can1=" << can1
       << " Ntoys=" << Ntoys
       << " Nbins=" << Nbins
       << " master=" << master
       << " alltoys=" << alltoys
       << " InjectCorrelation=" << InjectCorrelation
       << " toy=" << toy
       << " debug=" << debug
       << " Mode=" << Mode
       << endl;

  grand -> SetSeed(65485);

 for (int it = 0; it < Ntoys; it++) {
    if (debug > 1)
      cout << "Processing toy " << it << endl;
    // make a toy
    TH1D *htoy = 0;
    if (InjectCorrelation) {
      // injected correlation:
      htoy = GetSmearedSpecial(master);
    } else { 
      // random fluctuations:
      htoy = GetSmeared(master);
    }
    if (not htoy) {
      cout << "Error getting smeared histo!" << endl;
      continue;
    }
    if (Ntoys < 1001) {
      htoy -> SetLineColor(grand -> Uniform(1,50));
      htoy -> SetLineWidth(1);
      can1 -> cd();
      htoy -> DrawCopy("histSAME");
    } 
    for (int i = 1; i < Nbins+1; ++i)
      alltoys -> Fill(htoy -> GetXaxis() -> GetBinCenter(i), htoy -> GetBinContent(i), Mode);

    if (debug > 1)
      cout << "Filling..." << endl;

    // fill by current toy:
    toy -> Fill(htoy, Mode);

    delete htoy;

  } // toys
}

// ________________________________________________________________
// ________________________________________________________________
// ________________________________________________________________

void RunToyCovariance(int debug = 1, bool InjectCorrelation = true, int Mode = 1)
{
  
  // Mode:
  // 0: build the covariance from <x*y> - <x>*<y>
  // otherwise it is assumed that the covariance was filled directly, so we just need to take means

  gStyle -> SetPalette(1);
  gStyle -> SetCanvasColor(0);
  
  int Nbins = 4;
  grand = new TRandom3();

  int nFineBins = 400;
  double zmin = 0.;
  double zmax = 1.;
  // zoom to zmin/max:
  double hmin = 0.15;
  double hmax = 0.35;

  double hmin2 = hmin*hmin;
  double hmax2 = hmax*hmax;

  if (Mode != 0) {
    hmin2 = -0.001;  // THIS HAS TO BE NEGATIVE FOR THE DIRECT FILLING OF COVARIANCE, I.E. NON-0 MODE!
    hmax2 = 0.0004;
  }

// initialize the class with number of kinematic bins (say top pT bins), and some binning and limits for storage of the internal cross sections in each bin you provide in each toy
  ToyCovariance *toy = new ToyCovariance(Nbins, nFineBins, hmin, hmax, hmin2, hmax2, debug, Mode);

  int Ntoys = 1000; // 10000
  // make a disribution
  double xmin = 0.;
  double xmax = 1.;
  TH1D *master = new TH1D("test", "test", Nbins, xmin, xmax);
  TH2D *alltoys = new TH2D("toys", "toys", Nbins, xmin, xmax, nFineBins, zmin, zmax);

  master -> Sumw2();
  master -> SetLineWidth(6);
  master -> SetLineColor(kRed);
  master -> FillRandom("gaus", 50000);
  master ->Scale(1/master->Integral());

  TH1D *masterClone = (TH1D*) master -> Clone("Clone");
  masterClone -> Reset();
  masterClone -> FillRandom("gaus", 10000);
  masterClone -> Scale( master -> Integral() /  masterClone -> Integral());
  masterClone -> SetLineWidth(3);
  masterClone -> SetLineColor(kBlack);

  TCanvas *can1 = new TCanvas("master1", "master1", 0, 0, 600, 400);
  TCanvas *can2 = new TCanvas("master2", "master2", 200, 200, 800, 600);
  TCanvas *can3 = new TCanvas("master3", "master3", 400, 400, 800, 600);

  can1 -> cd();
  master -> Draw("e1hist");

  if (Mode > 0) {
    cout << "OK, runnign separate means and direct covariance filling." << endl;
    RunToys(can1, Ntoys, Nbins, master, alltoys,  InjectCorrelation, toy, debug, 1);
    RunToys(can1, Ntoys, Nbins, master, alltoys,  InjectCorrelation, toy, debug, 2);
  } else {
    RunToys(can1, Ntoys, Nbins, master, alltoys,  InjectCorrelation,  toy, debug, 0);
  }

  can2 -> cd();
  cout << "Drawing 2D..." << endl;
  alltoys -> DrawCopy("colz");
  //  master -> DrawCopy("e1histSAME");

  can1 -> cd();
  cout << "Drawing 1D..." << endl;
  if (Ntoys < 1001)  {
    master -> DrawCopy("e1histSAME");
    masterClone  -> DrawCopy("e1histSAME");
  }  else {
    master -> DrawCopy("e1hist");
    masterClone  -> DrawCopy("e1histSAME");
  }
  toy -> DrawProductHistos();
  toy -> DrawMeanHistos();
  toy -> DrawCorr2d();

  TMatrixD * Cov = toy -> GetCovariance();
  TMatrixD * Corr = toy -> GetCorrelation();

  TH2D *hcorr = MakeCorrHisto(Corr);
  can3 -> cd();
  hcorr -> SetStats(0);
  hcorr -> SetMinimum(-1.01);
  hcorr -> SetMaximum(+1.01);
  hcorr -> Draw("colz");
    
  cout << "Covariance matrix: " << endl;
  Cov -> Print();
  cout << "Correlation matrix: " << endl;
  Corr -> Print();

  cout << "Errors comparison:" << endl;
  for (int i = 1; i < Nbins+1; ++i) {
    cout << "Bin" << i-1
	 << " histo error: " << master -> GetBinError(i)
	 << " sqrt(Cov("  << i-1 << "," << i-1 << "): " <<  sqrt((*Cov)[i-1][i-1]) << endl;
  }

  cout << "Chi2 between master and master clone: " << GetChisquared(master, masterClone, Cov, true) << endl;

  cout << "Correlation matrix: " << endl;
  Corr -> Print();

  cout << "DONE!;-)" << endl;

}

// ________________________________________________________________

