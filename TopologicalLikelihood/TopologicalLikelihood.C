//
// jiri kvita
// Jan 19th 2010
// usage: root -l TopologicalLikelihood.C+
//
// generated several discriminating variables (see config file)
// generates simulated signal and bkg-like shapes
// generates data events based on purity
// builds and plots the likelihood
// signal fraction fitting using TFractionFitter

// _________________________________________
// _________________________________________
// _________________________________________

#include <iostream>

#include "standardsetup.C"

#include "TF1.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"
#include "TRandom3.h"
#include "TSystem.h"
#include "Config.cpp"
#include "TStyle.h"
#include "TLegend.h"
#include "TObjArray.h"
#include "TFractionFitter.h"
//#include "T.h"
//#include "T.h"

using std::cout;
using std::endl;
using std::cerr;


// _________________________________________

void GenerateTemplates(Config *config, TF1 **&templates, int &ntemplates, int color = kBlack, int lstyle = 1)
{

  templates = new TF1*[ntemplates];
  std::vector<std::string> fitname = config -> getVString("FitName");
  std::vector<std::string> fitformula = config -> getVString("FitFormula",";");
  std::vector<int> npars = config -> getVInt("nFitPars");

  ntemplates = fitname.size();

  std::vector< std::vector<double> > pars;
  int maxnpars = config -> get("mxnpars", 4);
  for (int i = 0; i < maxnpars; ++i) {
    std::vector<double> parsx = config -> getVDouble(Form("FitPars%i", i));
    pars.push_back(parsx);
  }

  std::vector<double> rangeDown = config -> getVDouble("rangeDown");
  std::vector<double> rangeUp = config -> getVDouble("rangeUp");
  
  for (int i = 0; i < ntemplates; ++i) {
    templates[i] = new TF1(fitname[i].c_str(), fitformula[i].c_str(), 
			   rangeDown[i], rangeUp[i]);
    for (int j = 0; j < npars[i]; ++j) {
      templates[i] -> SetParameter(j, pars[j][i]); // important!
    }
    templates[i] -> SetLineColor(color);
    templates[i] -> SetLineStyle(lstyle);
    templates[i] -> GetXaxis()->SetTitle((fitname[i] + " variable").c_str());

    // now normalise so that we have pdf's:
    double area = templates[i] -> Integral(rangeDown[i], rangeUp[i]);
    if (area > 0.)
      templates[i] -> SetParameter(0, templates[i] -> GetParameter(0) / area);
    else {
      cerr << "ERROR:GenerateTemplates: cannot normalise the area of " << fitname[i].c_str() << " as the integral is negative!" << endl;
    }
  }

}
// _________________________________________

void PrepareHistos(TF1 **&templates, TH1D **&histos, int ntemplates, 
		   int bins, TString tag = "_histo", int color = kBlack, int lstyle = 1)
{

 histos = new TH1D*[ntemplates];
 for (int i = 0; i < ntemplates; ++i) {

   TString tmp = templates[i] -> GetName();
   TString name = tmp + tag;
   TString title = tmp + tag + TString(";") + tmp;
   histos[i] = new TH1D(name, title, 
			bins, templates[i] -> GetXmin(), templates[i] -> GetXmax());
   histos[i] -> SetLineColor(color);
   histos[i] -> SetFillColorAlpha(color, 0.33);
   histos[i] -> SetLineStyle(lstyle);
   histos[i] -> Sumw2();
   histos[i] -> SetStats(0);

 }
}


// _________________________________________

int GenerateFromTemplates(Config *config,
			  TF1 **&templates, 
			  double *&data, 
			  int ntemplates)
{
  for (int i = 0; i < ntemplates; ++i) {
    data[i] = templates[i] -> GetRandom();
  }
  return 1;
}
// _________________________________________

double ComputeSumLog(TF1 **&templates_sig, TF1 **&templates_bkg, 
		     double *&data, int ntemplates)
{
  double xi = 0.;
  for (int i = 0; i < ntemplates; ++i) {
    double val_sig = templates_sig[i] -> Eval(data[i]);
    double val_bkg = templates_bkg[i] -> Eval(data[i]);
    double val = 1.;
    if (val_bkg > 0.)
      val = val_sig / val_bkg;
    if (val > 0.)
      xi += log(val);
  }
  return xi;
}

// _________________________________________

double ComputeLikelihood(TF1 **&templates_sig, TF1 **&templates_bkg, 
			 double *&data, int ntemplates)
{


  double xi = ComputeSumLog(templates_sig, templates_bkg, data, ntemplates);
  double lhood = exp(xi) / (1 + exp(xi));
  return lhood;

}

// _________________________________________

void CorrectLhood(TH1D *histo, double &lhood, double forcedmax = -9999.)
{
  double min = histo -> GetXaxis() -> GetXmin();
  double wmin = histo -> GetBinWidth(1);
  double max = histo -> GetXaxis() -> GetXmax();
  double wmax = histo -> GetBinWidth(histo -> GetXaxis() -> GetNbins());

  if (lhood < min)
    lhood = min - wmin/2.;
  if (lhood >= max)
    lhood = max - wmax/2.; 
  if (forcedmax > -9990. && lhood >= forcedmax) {
    lhood = forcedmax; 
  }

}


// _________________________________________
// _________________________________________
// _________________________________________
// _________________________________________

void TopologicalLikelihood(TString configname = "config.config")

{


  cout << "=== Running TemplateLHoodFit ===" << endl;

  gStyle -> SetCanvasColor(0);
  setup();
  gStyle->SetOptTitle(0);
  gStyle->SetErrorX(0);
  //  gStyle -> SetOptTitle(0);
  
  gSystem->Setenv("CAFE_CONFIG", configname.Data());
  TString namerealm = "signal";
  Config *config_sig = new Config(namerealm.Data());
  namerealm = "background";
  Config *config_bkg = new Config(namerealm.Data());
  
  // read general settings:
  namerealm = "general";
  Config *config = new Config(namerealm.Data());
  double Purity = config -> get("Purity", 0.8);
  int nEvts = config -> get("nEvts", 100);
  double MCStatsSF = config -> get("MCStatSF", 10);
  int SigCol = config -> get("SigColor", kRed);
  int BkgCol = config -> get("BkgColor", kBlue);
  int SigLineStyle = config -> get("SigLineStyle", 1);
  int BkgLineStyle = config -> get("BkgLineStyle", 2);
  int SumCol = config -> get("SumColor", 7);
  int SumFill = config -> get("SumFill", 1001);
  int DataCol = config -> get("DataCol", kBlack);
  float DataMarkSize = config -> get("DataMarkSize", 1.);
  int DataMark = config -> get("DataMark", 20);
  int bins = config -> get("bins", 20);
  int hlinewidth = config -> get("HistoLineWidth", 2);

  const int maxntemplates = 10;
  int ntemplates = 0;
  TF1 **templates_sig;
  GenerateTemplates(config_sig, templates_sig, ntemplates, SigCol, SigLineStyle);
  TF1 **templates_bkg;
  GenerateTemplates(config_bkg, templates_bkg, ntemplates, BkgCol, BkgLineStyle);
  assert(ntemplates <= maxntemplates);

  TCanvas *can = new TCanvas("templates", "templates", 0, 0, 1000, 600);
  can -> Divide(ntemplates, 2);
  for (int i = 0; i < ntemplates; ++i) {
    can -> cd(i+1);
    templates_sig[i] -> SetMinimum(0.0);
    templates_sig[i] -> Draw();
    templates_bkg[i] -> Draw("same");
  }

  // prepare test histograms for individual variables:
  TH1D **histos_sig;
  PrepareHistos(templates_sig, histos_sig, ntemplates, bins, "_sig", SigCol, SigLineStyle);
  TH1D **histos_bkg;
  PrepareHistos(templates_bkg, histos_bkg, ntemplates, bins, "_bkg", BkgCol, BkgLineStyle);
  TH1D **histos_data;
  PrepareHistos(templates_sig, histos_data, ntemplates, bins, "_data", DataCol);

  cout << "Will use " << nEvts << " pseudoevents." << endl;
  cout << "Will use " << ntemplates << " discriminating variables." << endl;
  cout << "Requested purity is: " << Purity << endl;

  TRandom3 *rand = new TRandom3();
  int nSig = rand -> Poisson(nEvts*Purity);
  int nBkg = rand -> Poisson(nEvts*(1.-Purity));


  double *event_sig = new double[ntemplates];
  double *event_bkg = new double[ntemplates];
  double *event_data = new double[ntemplates];

  double lhood_min = 0.;
  double lhood_max = 1.0;
  int lhood_bins = 10;

  TH1D *likelihood_data_h = new TH1D("likelihood_data", "Likelihood;Likelihood", lhood_bins, lhood_min, lhood_max);
  TH1D *likelihood_sig_h = new TH1D("likelihood_sig", "Likelihood;Likelihood", lhood_bins, lhood_min, lhood_max);
  TH1D *likelihood_bkg_h = new TH1D("likelihood_bkg", "Likelihood;Likelihood", lhood_bins, lhood_min, lhood_max);
  likelihood_sig_h -> SetLineColor(SigCol);
  likelihood_sig_h -> SetFillColorAlpha(SigCol, 0.33);
  likelihood_sig_h -> SetLineStyle(SigLineStyle);
  likelihood_sig_h -> SetLineWidth(hlinewidth);
  likelihood_bkg_h -> SetLineColor(BkgCol);
  likelihood_bkg_h -> SetFillColorAlpha(BkgCol, 0.33);
  likelihood_bkg_h -> SetLineStyle(BkgLineStyle);
  likelihood_bkg_h -> SetLineWidth(hlinewidth);
  likelihood_data_h -> SetLineColor(DataCol);
  likelihood_data_h -> SetMarkerStyle(DataMark);
  likelihood_data_h -> SetMarkerColor(DataCol);
  likelihood_data_h -> SetMarkerSize(DataMarkSize);
  likelihood_data_h -> SetLineWidth(hlinewidth);

  likelihood_sig_h -> SetStats(0);
  likelihood_bkg_h -> SetStats(0);
  likelihood_data_h -> SetStats(0);
   
  // generate high-stat sig and bkg lhood shape predictions:

  // loop over pseudoevents
  for (int i = 0; i < nEvts*MCStatsSF; ++i) {
    GenerateFromTemplates(config_sig, templates_sig, event_sig, ntemplates);
    GenerateFromTemplates(config_sig, templates_bkg, event_bkg, ntemplates);
    double Lhood_sig = ComputeLikelihood(templates_sig, templates_bkg, event_sig, ntemplates);
    double Lhood_bkg = ComputeLikelihood(templates_sig, templates_bkg, event_bkg, ntemplates);
    CorrectLhood(likelihood_sig_h, Lhood_sig, 1.);
    CorrectLhood(likelihood_sig_h, Lhood_bkg, 1.);
    likelihood_sig_h -> Fill(Lhood_sig);
    likelihood_bkg_h -> Fill(Lhood_bkg);
    for (int j = 0; j < ntemplates; ++j) {
      histos_sig[j] -> Fill(event_sig[j]);
      histos_bkg[j] -> Fill(event_bkg[j]);
    }
  } // loop over events

  // now loop over pseudo-generated data:
  for (int i = 0; i < nEvts; ++i) {
    // in each step, decide whether that shall be signal or bg
    // draw a point from each distribution randomly
    // compute the likelihood for the event
    // fill the histogram
    
    bool isSig = ((rand -> Uniform(0., 1.)) < Purity);  

    // draw from each topological distribution:
    if (isSig)
      GenerateFromTemplates(config_sig, templates_sig, event_data, ntemplates);
    else
      GenerateFromTemplates(config_sig, templates_bkg, event_data, ntemplates);
    for (int j = 0; j < ntemplates; ++j) {
      histos_data[j] -> Fill(event_data[j]);
    }
    // build likelihood:
    double Lhood = ComputeLikelihood(templates_sig, templates_bkg, event_data, ntemplates);
    CorrectLhood(likelihood_data_h, Lhood, 1.);
    likelihood_data_h -> Fill(Lhood);

  } // loop over events

  // normalise sig and bg templates to data:
  double nSigPredicted = likelihood_sig_h -> Integral();
  double nBkgPredicted = likelihood_bkg_h -> Integral();
  double nData = likelihood_data_h -> Integral();
  //  double nTotal = nSigPredicted + nBkgPredicted;
  likelihood_sig_h -> Scale(Purity*nData / nSigPredicted);
  likelihood_bkg_h -> Scale((1.-Purity)*nData / nBkgPredicted);
    
  // create a summed prediction:
  TH1D* likelihood_sum_h = (TH1D*) likelihood_sig_h -> Clone("likelihood_sum");
  likelihood_sum_h -> Add(likelihood_bkg_h);
  likelihood_sum_h -> SetLineColor(SumCol);
  likelihood_sum_h -> SetLineWidth (2);
  //likelihood_sum_h -> SetFillColorAlpha(SumCol, 0.33);
  likelihood_sum_h -> SetFillStyle(0); // SumFill);
  //  likelihood_sum_h -> SetFillColor(106);
  likelihood_sum_h -> SetStats(0);

  // plot the histogram and compare to predicted S+B distribtions mixed with proper purity.
  TCanvas *can_lh = new TCanvas("likelihood", "likelihood", 100, 100, 800, 600);
  can_lh -> cd();
  likelihood_sum_h -> SetMinimum(0.0);
  likelihood_sum_h -> Draw("hist");
  likelihood_sig_h -> Draw("hist same");
  likelihood_bkg_h -> Draw("hist same");
  likelihood_data_h -> Draw("e1 same");


  TLegend *leg = new TLegend(0.5, 0.5, 0.85, 0.8);
  leg -> SetBorderSize(0);
  //  leg -> SetFillColor(0);
  leg -> AddEntry(likelihood_sig_h, "Simulated Signal", "F");
  leg -> AddEntry(likelihood_bkg_h, "Simulated Background", "F"); 
  leg -> AddEntry(likelihood_sum_h, "Summed Prediction", "L"); 
  leg -> AddEntry(likelihood_data_h, "Pseudo-Data", "P");
  leg -> Draw();

  // and draw also control plots for each variable:
  // first need to normalise:
  TString opt = "hist";
  for (int j = 0; j < ntemplates; ++j) {
    can -> cd(ntemplates+j+1);
    histos_bkg[j] -> Scale(1./histos_bkg[j] -> Integral());
    histos_sig[j] -> Scale(1./histos_sig[j] -> Integral());
    histos_data[j] -> Scale(1./histos_data[j] -> Integral());
    histos_data[j] -> SetLineWidth(2);
    histos_data[j] -> SetMarkerStyle(20);
    histos_data[j] -> SetMarkerColor(1);
    histos_data[j] -> SetMinimum(0.0);
    histos_data[j] -> Draw("e1");
    histos_bkg[j] -> SetLineWidth(2);
    histos_bkg[j] -> Draw(opt+"same");
    histos_sig[j] -> SetLineWidth(2);
    histos_sig[j] -> Draw(opt+"same");
 
  }


  // try to fit the signal fraction:
  
  TObjArray *mc_histos = new TObjArray(2);      
  mc_histos -> Add(likelihood_sig_h);
  mc_histos -> Add(likelihood_bkg_h);
  TFractionFitter* fit = new TFractionFitter(likelihood_data_h, mc_histos); // initialise
  fit -> Constrain(1,0.0,1.0);               // constrain fraction 1 to be between 0 and 1
  //  fit->SetRangeX(1,8);                    // use only the first 8 bins in the fit
  Int_t status = fit->Fit();               // perform the fit
  cout << "fit status: " << status << endl;
  if (status == 0) {                       // check on fit status
    //    TH1F* result = (TH1F*) fit->GetPlot();
    //    data->Draw("Ep");
    //    result->Draw("same");
    double error = -999, value = -999; int parm = 0;
    fit -> GetResult(parm, value, error);
    cout << "Input fraction:  " << Purity << endl;
    cout << "Fitted fraction: " << value << " +/- " << error << endl;
    
  } else {
    cerr << "ERROR fitting the fraction using TFractionFitter!" << endl;
  }


  can -> Print(TString(can->GetName())+".eps");
  can -> Print(TString(can->GetName())+".pdf");
  can -> Print(TString(can->GetName())+".png");

  can_lh -> Print(TString(can_lh->GetName())+".eps");
  can_lh -> Print(TString(can_lh->GetName())+".pdf");
  can_lh -> Print(TString(can_lh->GetName())+".png");

  cout << "DONE!" << endl;

  return;
  
}
