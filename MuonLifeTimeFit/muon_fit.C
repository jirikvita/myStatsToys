// JK 3.2.2017

#include <TH2D.h>
#include <TH1D.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TF1.h>
#include <TLine.h>
#include <TFile.h>

// Usage: root -l muon_fit.C++g


const double gfact = 10.;
const double gunitf = 1000.;
// for unconverted file from the root file, which is in tens of ns:
// cont double gfact = 1.;
// const double gunitf = 100.;


// __________________________________________________________

TH1D* UnitsConvert(TH1D *histo, double fact, TString tag)
// works only for uniformly binned histograms!
{

  int nb = histo -> GetNbinsX();
  double xmin = histo->GetXaxis()->GetXmin();
  double xmax = histo->GetXaxis()->GetXmax();
  TH1D *hc = new TH1D(TString(histo->GetName()) + tag,
		      histo -> GetTitle(),
		      nb, xmin*fact, xmax*fact);
  for (int i = 0; i <= nb+1; ++i) {
    hc -> SetBinContent(i, histo -> GetBinContent(i));
    hc -> SetBinError(i, histo -> GetBinError(i));
    //    cout << "x=" << hc -> GetBinCenter(i) << " " << hc -> GetBinContent(i) << endl;
  }
  hc -> SetEntries(histo -> GetEntries());
  hc -> Scale(1.);
  return hc;
  
}

// __________________________________________________________

void FitHisto(TH1D *histo, TF1 *fit, double fitmin, double fitmax, int ntimes, int par, double unitf, TH1D *mean, TH1D *chi2,
	      TString opt1 = "Q0", TString opt2 = "Q0", TCanvas *can = 0, TString fopt = "same")
{
  //  cout << "In FitHisto " << endl;
  //cout << "Fitting " << histo->GetName() << " by " << fit->GetName() << endl;
  for (int i = 0; i < ntimes; ++i) {
    histo -> Fit(fit->GetName(),opt1, opt2, fitmin, fitmax);
    //    cout << "Filling by " << 1/fit -> GetParameter(par)/unitf << endl;
  }
  // BREAK!!!:)
  //  TH1D *aa = 0;
  //  aa -> GetName();
  if (mean) {
    if (fit -> GetChisquare() / fit -> GetNDF() < 5.)
      mean -> Fill(1/fit -> GetParameter(par)/unitf);
  }
  if (chi2) {
    double val = fit -> GetChisquare() / fit -> GetNDF();
    if (val > chi2 -> GetXaxis() -> GetXmax())
      val = chi2 -> GetBinCenter(chi2 -> GetNbinsX());
    chi2 -> Fill(val);
  }
  if (can) {
    can -> cd();
    fit -> DrawCopy(fopt);
  }
}

// __________________________________________________________

double GetLastNonemptyX(TH1D *histo)
{
  int n = histo -> GetNbinsX();
  double val = -1;
  while (n > 0 and val <= 0) {
    val = histo -> GetBinContent(n);
    n--;
  }
  return histo -> GetBinLowEdge(n) + histo->GetBinWidth(n);
}

// __________________________________________________________

void PrintResult(TF1 *fit, int pari, double unitf)
{
  cout << "  tau = " << 1./fit->GetParameter(pari)/unitf << " +/- " << fit->GetParError(pari)/ pow(fit->GetParameter(pari), 2) / unitf  << " microseconds."<< endl;
}

// __________________________________________________________
// __________________________________________________________
// __________________________________________________________

void muon_fit(int nToys = 18)
{

  TFile *infile = new TFile("histo.root");
  TH1D *histo_bad = (TH1D*) infile -> Get("time50");
  TH1D *histo = UnitsConvert(histo_bad, gfact, "_ns");
  histo ->SetXTitle("t [ns]");
  histo -> SetStats(0);
  histo -> GetXaxis() -> SetMoreLogLabels();
  histo -> GetYaxis() -> SetMoreLogLabels();

  double step = histo -> GetBinWidth(3);
  double last = GetLastNonemptyX(histo);
  cout << "Last nonepty time: " << last << endl;

  double xlow = 40*gfact;
  double xhigh = 480*gfact;

  // a bit ugly I mix C arrays and std::vectors...
  const int maxNfits = 3;
  const int maxNpars = 5;
  int nfits = 3;
  int nTimesToFit[] = {2, 1, 3};
  int iPar[] = {1, 1, 1};
  int col[] = {kRed, kBlue, kGreen+3};
  
  double InitialPars[][maxNpars] = { {histo->GetBinContent(3), 1e-3/gfact, 50}, // fit1
				     {histo->GetBinContent(3), 1e-3/gfact, -0.1/gfact, 50}, // fit2
				     {histo->GetBinContent(3), 1e-3/gfact, 1.e-2/gfact, 2e5/gfact} // fit3
  };
  
  TF1 *fit1 = new TF1("fit1", "[0]*exp(-[1]*x)+[2]", xlow, xhigh);
  fit1 -> SetLineColor(col[0]);
  fit1 -> SetParNames("A", "#lambda");
  fit1 -> SetNpx(1000);

  TF1 *fit2 = new TF1("fit2", "[0]*exp(-[1]*x)-exp([2]*x)+[3]", xlow, xhigh);
  fit2 -> SetParNames("A", "#lambda", "#alpha");
  fit2 -> SetLineColor(col[1]);
  fit2 -> SetNpx(1000);
  
  // JK: convolution of a gauss and exp funtion:
  // https://en.wikipedia.org/wiki/Exponentially_modified_Gaussian_distribution
  // lambda/2*exp(lambda/2*(2*mu+lambda*sigma*sigma-2*x))*TMath::Erf((mu+lambda*sigma*sigma-x)/(sqrt(2)*sigma))

  TF1 *fit3 = new TF1("fit3", "[0]*exp([1]/2*(2*[3]+[1]*[2]*[2]-2*x))*TMath::Erf(([3]+[1]*[2]*[2]-x)/(sqrt(2)*[2]))", xlow, xhigh);
  fit3 -> SetLineColor(col[2]);
  fit3 -> SetParNames("A", "#lambda", "#sigma", "#mu");
  fit3 -> SetNpx(1000);
  
  histo->SetMarkerStyle(20);
  histo->SetLineColor(1);
  TF1 *fits[maxNfits] = {fit1, fit2, fit3};
  for (int ih = 0; ih < nfits; ++ih) {
    for (int ip = 0; ip < fits[ih]->GetNpar(); ++ip)
      fits[ih] -> SetParameter(ip, InitialPars[ih][ip]);
  }
  
  double fitmin = xlow;
  double fitmax = xhigh;


  // now gradually remove bins included in the fit
  vector<TH1D*> mean;
  vector<TH1D*> chi2;
  vector<TH1D*> hclone;

  // visualisation of the fit ranges:
  vector<TLine*> line;
  double yline = histo -> GetMaximum();
  double dy = (yline - histo->GetMinimum()) / (3*nToys);

    int nbins = 30;
  for (int ih = 0; ih < nfits; ++ih) {
    TString name = Form("LifeTime%i", ih);
    mean.push_back(new TH1D(name, name + ";#tau_{#mu} [#mus]", nbins, 2.2-1, 2.2+1));
    name = Form("Chi2%i", ih);
    chi2.push_back(new TH1D(name, name + ";#chi^{2}", nbins*2, 0, 5));
  }

  TCanvas *MultiFitsCan = new TCanvas("MultiFitsCan", "MultiFitsCan", 0, 0, 1000, 800);
  MultiFitsCan -> Divide(2,2);
  for (int ih = 0; ih < nfits; ++ih) {
    MultiFitsCan -> cd(ih+1);
    gPad -> SetLogy(); gPad -> SetLogx();
    hclone.push_back((TH1D*)  histo -> DrawCopy(TString(histo->GetName())+Form("_clone_%i", ih)));
    hclone[ih] -> GetXaxis() -> SetRangeUser(500, 5000.);
  }


  // shorten upper fit edge
  TString fopt = "same";
  TString opt = "Q0";
  for (int j = 0; j < nToys; ++j) {
    double tmax = last - j*step;
    if (fitmin < tmax) {
      line.push_back(new TLine(fitmin, yline, tmax, yline));
      yline -= dy;
      for (int ih = 0; ih < nfits; ++ih) {
	MultiFitsCan -> cd(ih+1);
	FitHisto(histo, fits[ih], fitmin, tmax, nTimesToFit[ih], iPar[ih], gunitf, mean[ih], chi2[ih], opt, opt, (TCanvas*)gPad, fopt);
	fopt = "same";
	opt = "Q0";
      }
    }
  }
  // move low fit edge
  fopt = "same";
  opt = "Q0";
  for (int j = 0; j < nToys; ++j) {
    double tmin = xlow + (j+1)*step;
    if (tmin < last) {
      line.push_back(new TLine(tmin, yline, last, yline));
      yline -= dy;
      for (int ih = 0; ih < nfits; ++ih) {
	MultiFitsCan -> cd(ih+1);
	FitHisto(histo, fits[ih], tmin, last, nTimesToFit[ih], iPar[ih], gunitf, mean[ih], chi2[ih], opt, opt, (TCanvas*)gPad, fopt);
	//	fopt = "same";
	//	opt = "Q0";
      }
    }
  }
  //shorten both ends:
  fopt = "same";
  opt = "Q0";
  for (int j = 0; j < nToys; ++j) {
    double tmin = xlow + j*step;
    double tmax = last - j*step;
    if (tmin < tmax) {
      line.push_back(new TLine(tmin, yline, tmax, yline));
      yline -= dy;
      for (int ih = 0; ih < nfits; ++ih) {
	MultiFitsCan -> cd(ih+1);
	FitHisto(histo, fits[ih], tmin, tmax, nTimesToFit[ih], iPar[ih], gunitf, mean[ih], chi2[ih], opt, opt, (TCanvas*)gPad, fopt);
	//	fopt = "same";
	//	opt = "Q0";
      }
    }
  }
  for (int ih = 0; ih < nfits; ++ih) {
    MultiFitsCan -> cd(ih+1);
    hclone[ih] -> Draw("same");
  }
  MultiFitsCan -> Print(TString(MultiFitsCan->GetName()) + ".png");
  MultiFitsCan -> Print(TString(MultiFitsCan->GetName()) + ".pdf");
  MultiFitsCan -> cd(4);
  TH1D *htmp = (TH1D*) histo -> DrawCopy();
  htmp -> SetTitle("Fit ranges");
  cout << "Will print " << line.size() << " lines." << endl;
  for (int il = 0; il < line.size(); ++il) {
    line[il] -> SetLineColor(kRed);
    line[il] -> Draw();
  }

  TCanvas *can2 = new TCanvas("Pars", "Pars", 0, 0, 1000, 800);
  can2->Divide(2,2);
  for (int ih = 0; ih < nfits; ++ih) {
    can2 -> cd(ih+1);
    mean[ih] -> Draw("hist");
  }
  can2 -> Print(TString(can2->GetName()) + ".png");
  can2 -> Print(TString(can2->GetName()) + ".pdf");

  TCanvas *can3 = new TCanvas("Chi2", "Chi2", 0, 0, 1000, 800);
  can3->Divide(2,2);
  for (int ih = 0; ih < nfits; ++ih) {
    can3 -> cd(ih+1);
    chi2[ih] -> Draw("hist");
  }
  can3 -> Print(TString(can3->GetName()) + ".png");
  can3 -> Print(TString(can3->GetName()) + ".pdf");


  // fit the full range
  //  fits needs more care...
  for (int ih = 0; ih < nfits; ++ih) {
    for (int ip = 0; ip < fits[ih]->GetNpar(); ++ip)
      fits[ih] -> SetParameter(ip, InitialPars[ih][ip]);
  }
  TCanvas *can = new TCanvas("Fits", "Fits", 0, 0, 1000, 800);
  can -> cd();
  for (int ih = 0; ih < nfits; ++ih) {
    //    double max = last;
    double xmax = xhigh;
    cout << "Fitrange: " << fitmin << " -- " <<  xmax << endl;
    FitHisto(histo, fits[ih], fitmin, xmax, nTimesToFit[ih], iPar[ih], gunitf, 0, 0, "", "");
  }
  can -> cd();
  histo->SetMarkerStyle(20);
  histo->SetMarkerSize(1);
  histo->SetMarkerColor(kBlack);
  histo->Draw("e1");
  
  fit1->Draw("same");
  //  cfit1->SetName("clone1");
  fit2->Draw("same");
  //fit1->SetName("clone2");
  fit3->Draw("same");
  //fit1->SetName("clone3");
  histo->Draw("e1same");
  can -> Print(TString(can->GetName()) + ".png");
  can -> Print(TString(can->GetName()) + ".pdf");

  gPad -> SetLogy();
  can -> Print(TString(can->GetName()) + "_logy.png");
  can -> Print(TString(can->GetName()) + "_logy.pdf");

  gPad -> SetLogx();
  histo -> GetXaxis() -> SetRangeUser(500, 5000.);
  can -> Print(TString(can->GetName()) + "_logxy.png");
  can -> Print(TString(can->GetName()) + "_logxy.pdf");

  cout << "Total bins : " << histo -> GetNbinsX() << endl;
  cout << "Bin width  : " << histo -> GetBinWidth(3) << endl;
  cout << "Resulting lifetimes in microseconds: " << endl;
  for (int ih = 0; ih < nfits; ++ih) {  
    cout << "===> Fit using " <<  fits[ih]->GetTitle() << endl;
    cout << "    chi2/ndf=" << fits[ih] -> GetChisquare() / fits[ih] -> GetNDF() << endl;
    PrintResult(fits[ih], iPar[ih], gunitf);
    for (int ip = 0; ip < fits[ih]->GetNpar(); ++ip) {
      cout << "  " <<  fits[ih]->GetParName(ip) << ": " <<  fits[ih]->GetParameter(ip) << " +/-" <<  fits[ih]->GetParError(ip) << endl;
    } 
  }
  
  
  
}
