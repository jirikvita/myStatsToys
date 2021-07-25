//
// File: ShapeLHood.C
// jiri kvita
// Fri Dec  4 11:54:00 CET 2009
// Apr 2010
//
// ideas: comapre also to simple fit of generated s+b to the s+b fit function?;-)
//
// running:
// root -l ShapeLHood.C+
// 

#include <vector>
#include <string>
#include <iostream>

#include "TROOT.h"
#include "TStyle.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TF1.h"
#include "TF3.h"
#include "TMinuit.h"
#include "TFitter.h"
#include "TRandom3.h"
#include "TMath.h"

using std::cout;
using std::endl;
using std::cerr;
using std::vector;
using std::string;

const int maxNpars = 100;
int maxNCalls = 200;
int gnPars;

double gLogLHmin;
double gLogLHmax;

TRandom3 *grand;

int Debug = 3;
bool ghistosReady = false;

int gCall = 0;
double gPenalty = 1.e20;
TH1D **gHparevolution;
TH2D **gHLHvspar;

TH1D *genHall;
TH1D *genHsig;
TH1D *genHbg;

double gNsigFit;
double gNbgFit;
// choose expected signal entries:
double gNsig;
// choose expected bg entries:
double gNbg;


// input top mass
double gmtop;
// fitted top mass
double gmtopFit;

double gtopMin; 
double gtopMax;

// error on bg events count (ofton very precise, from simlation)
double gNbgError;


// events
int gNevents;
vector<double> gRecoMassEvt;

// shape templates:
TF1* gsigshape;
TF1* gbgshape;

// __________________________________________
// __________________________________________
// __________________________________________

void Normalise(TF1 *fun)
{
  fun -> SetParameter(0, fun -> GetParameter(0) / fun -> Integral(fun -> GetXmin(), fun -> GetXmax()));
}
// __________________________________________

void Init(double min, double max, double mtop, double sigreso, double bgmean, double bgreso)
{

  cout << "Creating signal teplate within top mass max,min: " <<  min << " " << max << endl;
  gsigshape = new TF1("SigShape", "[0]*exp(-(x-[1])^2/(2*[2]^2))", min, max);
  gsigshape -> SetParameters(1., mtop, sigreso);
  cout << "Creating background teplate within top mass max,min: " <<  min << " " << max << endl;
  gbgshape = new TF1("BgShape", "[0]/x*exp(-(x-[1])^2/(2*[2]^2))", min, max);
  gbgshape -> SetParameters(1., bgmean, bgreso);

  Normalise(gsigshape);
  Normalise(gbgshape);

}


// _____________________

inline unsigned long Factorial(int n)
{
  if (n <= 1)
    return 1;
  unsigned long fact = 1;
  for (unsigned long i = 1; i <= n; ++i)
    fact *= i;
  return fact;
}


// __________________________________________

inline double PoissonLog(double n, double mu)
{
      
  if (Debug > 2)
    cout << "PoissonLog: n=" << n
	 << " mu=" << mu 
	 << endl;
  if (mu > 0.)
    return (-mu + n*log(mu));
  else
    return (-gPenalty);
}
// __________________________________________

double Poisson(double n, double mu)
{
  cout << "Poisson: Factorial(" << n << ")=" << Factorial(int(n))
       << " pow(" << mu << ", " << n << ")=" << pow(mu, n)
       << " exp(-" << mu << ")=" <<  exp(-mu)
       << endl;
  return (exp(-mu) * pow(mu, n) / Factorial(int(n)));
}
// __________________________________________

double GaussianLog(double x, double mu, double sigma)
{
  if (Debug > 2) 
    cout << " x=" << x
	 << " mu=" << mu
	 << " sigma=" << sigma
	 << " val=" << (-pow(x-mu, 2) / (TMath::TwoPi() * sigma*sigma))
	 << endl;

  return (-pow(x-mu, 2) / (TMath::TwoPi() * sigma*sigma));
}

// __________________________________________

double Gaussian(double x, double mu, double sigma)
{
  return exp(-pow(x-mu, 2) / (TMath::TwoPi() * sigma*sigma));
}


// __________________________________________

double GetShapeLhoodLog(TF1 *bgshape, TF1 *sigshape)
{

  double lhoodlog = 0.;

  sigshape -> SetParameter(1, gmtopFit);
  Normalise(sigshape);

  for (int i = 1; i < gNevents; ++i) {
    // get the values of the normalised probability distributions:
    // this has to depend on the fitted top mass!!!


    double mtopReco = gRecoMassEvt[i];
    double ProbSig = sigshape -> Eval(mtopReco);
    double ProbBg = bgshape -> Eval(mtopReco);


    if (Debug > 3)
      cout << " mtopFit=" << gmtopFit
	   << " mtopReco=" << mtopReco
	   << " ProbSig=" << ProbSig
	   << " ProbBg=" << ProbBg
	   << endl;
    

    //    double ProbSig = sigshape -> GetBinContent(i);
    //    double SigSig = bgshape -> GetBinContent(i);
    double addlh = 1./(gNsigFit + gNbgFit) * (gNsigFit * ProbSig + gNbgFit * ProbBg); 
    if (addlh > 0.)
      lhoodlog += log(addlh);
    else 
      lhoodlog += -gPenalty;
  }

  return lhoodlog;

}

// __________________________________________
/*
double ComputeLHood(double *x)
{

  double lhood_normalisation  = Poisson(gNbgFit + gNsiFig, gNbg + gNsig);
  double lhood_bg = Gaussian(gNbgFit, gNb); // smaller bg uncert., therefore NOT: Poisson(gNbgFit, gNbg);
  double lhood_shape = GetShapeLhood();

  double lhood = lhood_normalisation * lhood_bg * lhood_shape;

  return lhood;

}
*/
// __________________________________________

 //double GetNegLhoodLog(Double_t *x, Double_t *par)
double GetNegLhoodLog(Double_t *par)
{
 
  gNsigFit = par[0];
  gNbgFit = par[1];
  gmtopFit = par[2];

  if (gCall < maxNCalls) {
    for (int i = 0; i < gnPars; ++i) {
      if (ghistosReady) gHparevolution[i] -> Fill(gCall, par[i]);
    }
  }

  if (ghistosReady && Debug > 1)
    cout << "*** Call " << gCall << " Pars: " 
	 << par[0] << " "
	 << par[1] << " "
	 << par[2]
	 << endl;

  if (Debug > 1)
    cout << "Calling PoissonLog with gNbgFit + gNsigFit, gNbg + gNsig: "
	 << " gNbgFit=" << gNbgFit
	 << " gNsigFit=" << gNsigFit
	 << " gNbg=" << gNbg
	 << " gNsig=" << gNsig
	 << endl;

  double lhood_normalisation  = PoissonLog(gNevents, gNbgFit + gNsigFit);
  double lhood_bg = GaussianLog(gNbgFit, gNbg, gNbgError);
  double lhood_shape = GetShapeLhoodLog(gbgshape, gsigshape);
  double lhood = - lhood_normalisation - lhood_bg - lhood_shape;

  if (Debug > 0)
    cout << " lhood_normalisation=" << lhood_normalisation
	 << " lhood_bg=" << lhood_bg
	 << " lhood_shape=" << lhood_shape
	 << " -lhood=" << lhood
	 << endl;

  if (gCall < maxNCalls) {
    for (int i = 0; i < gnPars; ++i) {
      if (ghistosReady) gHLHvspar[i] -> Fill(par[i], lhood);
    }
  }

  if (ghistosReady) {
    gHparevolution[gnPars] -> Fill(gCall, -lhood);
    gHparevolution[gnPars+1] -> Fill(gCall, -lhood_normalisation);
    gHparevolution[gnPars+2] -> Fill(gCall, -lhood_bg);
    gHparevolution[gnPars+3] -> Fill(gCall, -lhood_shape);
  }

  gCall++;

  return lhood;

}
// __________________________________________

// wrapper for minuit:

void fcn(Int_t &npar, Double_t *gin, Double_t &f, Double_t *par, Int_t iflag)
{

  f = GetNegLhoodLog(par);

}
// __________________________________________

double GetMyRandom(TF1* normfun) {
  
  // function is expected to be already normalised!
  if (!normfun)
    return 0.;
  if (!grand)
    grand = new TRandom3();
  
  bool accept = 0;
  double xval = 0.;
  double yval = 0.;
  while(!accept) {
    xval = grand -> Uniform(normfun -> GetXmin(), normfun -> GetXmax());
    yval = grand -> Uniform(0., 1.);;
    accept = yval < normfun -> Eval(xval);
  }
  return xval;

}

// __________________________________________

void GeneratePseudoEvents(int N, double mtop)
{

  grand = new TRandom3();
  double sigfrac = gNsig / (gNsig + gNbg);
  cout << "Input signal fraction: " << sigfrac << endl;
  gsigshape -> SetParameter(1, mtop);
  int nbg = 0;
  int nsig = 0;

  genHall = new TH1D("generated_events_all", "generated_events_all", 30, gtopMin, gtopMax);
  genHsig = new TH1D("generated_events_sig", "generated_events_sig", 30, gtopMin, gtopMax);
  genHbg = new TH1D("generated_events_bg", "generated_events_bg", 30, gtopMin, gtopMax);

  double val = 0.;
  int NgenEvts = grand -> Poisson(N);
  for (unsigned int i = 0; i < NgenEvts; ++i) {
    if (grand -> Uniform(0, 1) < sigfrac) {
      nsig++;
      //      val = gsigshape -> GetRandom();
      val = GetMyRandom(gsigshape);
      gRecoMassEvt.push_back(val);
      genHsig -> Fill(val);
      //      cout << "Generated S: " << val << endl;
    } else {
      nbg++;
      //      val = gbgshape -> GetRandom();
      val = GetMyRandom(gbgshape);
      gRecoMassEvt.push_back(val);
      genHbg -> Fill(val);
      //      cout << "Generated B: " << val << endl;
    }
    genHall -> Fill(val);


  }
  cout << "Generated events: " << NgenEvts << " signal fraction: " << nsig/(1.*nsig + nbg) << endl;
  gNevents = NgenEvts;

}


// __________________________________________
// __________________________________________
// __________________________________________

void LhoodNEventsFit()

{


  // choose the top mass
  gmtop = 172.;
  // choose expected signal entries:
  gNsig = 1000;
  // choose expected bg entries:
  gNbg = 500;
  gNbgError = 15.;

  double genTopMass = gmtop;
  double sigreso = 3.;
  double bgmean = 140.;
  double bgreso = 50.;
  gtopMin = 150.; 
  gtopMax = 200.;

  Init(gtopMin, gtopMax, genTopMass, sigreso, bgmean, bgreso);
  // declare fitted m

  int Nevts = gNsig + gNbg;
  GeneratePseudoEvents(Nevts, genTopMass);

  // now, minimize the likelihood as a function of Nsig, Nbg, mtop
  // this should be unbinned, i.e. one should maximize function
  //  TF3 *fitLHood = new TF3("", "", ,  ComputeLhood());
  // fitLHood -> SetParameter();

  // or, for better numerical stability, minimize the following:

  //     http://root.cern.ch/root/html524/TF3.html
  //	TF3(const char* name, void* ptr, Double_t xmin, Double_t xmax, Double_t ymin, Double_t ymax, Double_t zmin, Double_t zmax, Int_t npar, const char* className)

  // prepare the function to minimise:

  double deltaNevts = Nevts / 2;
  double sigMax = Nevts + deltaNevts;
  double bgMax = Nevts + deltaNevts; 
  int nPars = 3;
  gnPars = nPars;

  double mtopStart = 180.;

  gHparevolution=  new TH1D*[nPars+4];
  gHLHvspar = new TH2D*[nPars];  

  assert(nPars < maxNpars);
  string parname[maxNpars] = {"Nsig", "Nbg", "mtop"};
  double parmax[maxNpars] = {Nevts + deltaNevts, Nevts + deltaNevts, gtopMax};
  double parmin[maxNpars] = {0, 0, gtopMin};


  // now minimise:
  //   TF3 *fitLHoodLog = new TF3("FitFun", GetNegLhoodLog, 0, sigMax, 0, bgMax, topMin, topMax, nPars);  
  //   fitLHoodLog -> SetParameters(Nevts, 0., mtopStart);
  //  gFitter=TVirtualFitter::Fitter(histMunfold);
  //  gFitter->SetFCN(GetNegLhoodLog);


  // from  root/tutorials/fit/Ifit.C :

  TMinuit *gMinuit = new TMinuit(nPars);  //initialize TMinuit with a maximum of 5 params
  gMinuit->SetFCN(fcn);

  double arglist[10];
  int ierflg = 0;
  
  arglist[0] = 1;
  gMinuit->mnexcm("SET ERR", arglist ,1,ierflg);

  double *vstart = new double[nPars];
  double *step = new double[nPars];
  
  
    vstart[0] = Nevts;
    vstart[1] = Nevts/100.;
  
  /*
    vstart[0] = gNsig;
    vstart[1] = gNbg;
  */
    /*
  vstart[0] = grand -> Poisson(gNsig);
  vstart[1] = grand -> Poisson(gNbg);
  vstart[2] = mtopStart;
    */

  cout << "Looking for likelihood extremes..." << endl;
  // test the rough lhood returned range for histohram axis:
  int ntestSteps = 20;
  gLogLHmin = 9.e10;
  gLogLHmax = -9.e10;
  double *testpars = new double[nPars];
  double gLogLHmax;
  double lhood = 0.;
  double frac = 4;
  double testparmin[maxNpars] = {gNsig - gNsig/frac, gNbg - gNbg/frac, gmtop - gmtop/frac};
  double testparmax[maxNpars] = {gNsig + gNsig/frac, gNbg + gNbg/frac, gmtop + gmtop/frac};
  int DebugOrig = Debug;
  Debug = 0;
  int count = 0;
  int printout = 1000;
  for (int i = 0; i < ntestSteps; ++i) {
    testpars[0] = testparmin[0] + i*(testparmax[0] - testparmin[0]) / (ntestSteps);
    for (int j = 0; j < ntestSteps; ++j) {
      testpars[1] = testparmin[1] + j*(testparmax[1] - testparmin[1]) / (ntestSteps);
      for (int k = 0; k < ntestSteps; ++k) {
	testpars[2] = testparmin[2] + k*(testparmax[2] - testparmin[2]) / (ntestSteps);

	if ( !(count % printout))
	  cout << count << "/" << ntestSteps*ntestSteps*ntestSteps << endl;

	lhood = GetNegLhoodLog(testpars);
	/*
	  cout << " testpars0=" << testpars[0]
	  << " testpars1=" << testpars[1]
	  << " testpars2=" << testpars[2]
	  << " lhood=" << lhood
	  << endl;
	*/
	if (lhood <  gLogLHmin)
	  gLogLHmin = lhood;
	if (lhood >  gLogLHmax)
	  gLogLHmax = lhood;
	++count;
      }
    }
  }
  if (TMath::Abs(gLogLHmax) < 1.e-9 || gLogLHmax > 0.)
    gLogLHmax = 0.;
  cout << "Found" 
       << " -logLHmin=" << gLogLHmin
       << " -logLHmax=" << gLogLHmax
       << endl;

  double minSF = 1.3;
  if (gLogLHmin < 0.)
    gLogLHmin *= minSF;
  else
    gLogLHmin /= minSF;

  int nbins = 100;
  for (int i = 0; i < nPars; ++i) {
    gHparevolution[i] = new TH1D(parname[i].c_str(), (parname[i] + ";icall;" + parname[i]).c_str(), maxNCalls, 0, maxNCalls);
    gHLHvspar[i] = new TH2D(("-log(L) vs " + parname[i]).c_str(), ("-log(L) vs " + parname[i] + ";" + parname[i]).c_str(), 
			    nbins, parmin[i], parmax[i], nbins, gLogLHmin, gLogLHmax);
  }
  gHparevolution[nPars+0] =  new TH1D("-log(L)", "-log(L);icall", maxNCalls, 0, maxNCalls);
  gHparevolution[nPars+1] =  new TH1D("-log(L_{norm})", "-log(L_{norm});icall", maxNCalls, 0, maxNCalls);
  gHparevolution[nPars+2] =  new TH1D("-log(L_{bg})", "-log(L_{bg});icall", maxNCalls, 0, maxNCalls);
  gHparevolution[nPars+3] =  new TH1D("-log(L_{shape})", "-log(L_{shape});icall", maxNCalls, 0, maxNCalls);

  ghistosReady = true;
  gCall = 0;
  Debug = DebugOrig;

  step[0] = 100.;
  step[1] = 30.;
  step[2] = 0.5;
  for (int i = 0; i < nPars; ++i) {
    gMinuit->mnparm(i, parname[i].c_str(), vstart[i], step[i], parmin[i], parmax[i], ierflg);

  }
  /*  gMinuit->mnparm(0, parname[0].c_str(), vstart[0], step[0], 0, Nevts + deltaNevts, ierflg);
      gMinuit->mnparm(1, parname[1].c_str(),  vstart[1], step[1], 0, Nevts + deltaNevts,ierflg);
      gMinuit->mnparm(2, parname[2].c_str(), vstart[2], step[2], topMin, topMax, ierflg);
  */
  // Now ready for minimization step
  arglist[0] = 500;
  arglist[1] = 1.;
  gMinuit->mnexcm("MIGRAD", arglist, 2, ierflg);
  
  // Print results
   Double_t amin,edm,errdef;
   Int_t nvpar,nparx,icstat;
   gMinuit->mnstat(amin, edm, errdef, nvpar, nparx, icstat);


   cout << " ======================================================" << endl;
   cout << "Input S events    : " << gNsig << endl;
   cout << "Input B events    : " << gNbg << endl;
   cout << "Input S+B events  : " << gNsig + gNbg << endl;
   cout << "Generated events  : " << gNevents << endl;
   double *FitPars = new double[nPars];
   double *FitParErrs = new double[nPars];
   for (int i = 0; i < nPars; ++i) {
     gMinuit -> GetParameter(i, FitPars[i], FitParErrs[i]);
   }
   cout << "Fitted S events   : " <<  FitPars[0]  << " +/- " << FitParErrs[0] << endl;
   cout << "Fitted B events   : " <<  FitPars[1]  << " +/- " << FitParErrs[1] << endl;
   cout << "Fitted S+B events : " <<  FitPars[0]+FitPars[1] << " +/- " << sqrt(FitParErrs[1]*FitParErrs[1] + FitParErrs[0]*FitParErrs[0]) << endl;
   cout << "Generated top mas : " << gmtop << endl;
   cout << "Fitted top mass   : " <<  FitPars[2]  << " +/- " << FitParErrs[2] << endl;
   cout << " ======================================================" << endl;


   // plot

   gStyle->SetPalette(1);
   gStyle->SetCanvasBorderMode(0);
   gStyle->SetPadBorderMode(0);
   gStyle->SetPadColor(0);
   gStyle->SetCanvasColor(0);
   gStyle->SetTitleColor(0);
   gStyle->SetStatColor(0);
   gStyle->SetOptFit(1111);
   gStyle->SetFillColor(10);
   gROOT->ForceStyle();

   TCanvas *can = new TCanvas("pars_evolution", "pars_evolution", 0, 0, 1400, 1000);
   can -> Divide(4, 3);
   int ican = 0;
   for (int i = 0; i < nPars+4; ++i) {
     can -> cd(++ican);
     gHparevolution[i] -> Draw();
   }
   for (int i = 0; i < nPars; ++i) {
     can -> cd(++ican);
     gHLHvspar[i] -> Draw("colz");
   }
   can -> cd(++ican);
   gsigshape -> SetParameter(1, genTopMass);
   gsigshape -> SetLineColor(kRed);
   gbgshape -> SetLineColor(kBlue);
   gsigshape -> Draw();
   gbgshape -> Draw("same");

   // generated events histo:
   can -> cd(++ican);
   genHall -> SetMarkerColor(kBlack);
   genHall -> SetMarkerSize(1);
   genHall -> SetMarkerStyle(20);

   genHsig -> SetMarkerColor(kRed);
   genHsig -> SetMarkerSize(1);
   genHsig -> SetMarkerStyle(20);
   
   genHbg -> SetMarkerColor(kBlue);
   genHbg -> SetMarkerSize(1);
   genHbg -> SetMarkerStyle(20);

   genHall -> Draw("e1");
   genHsig -> Draw("e1same");
   genHbg -> Draw("e1same");
   

   can -> Print(TString(can -> GetName()) + ".eps");

   delete [] vstart;
   delete [] step;
   delete [] testpars;
   delete [] FitParErrs;
   delete [] FitPars;


   cout << " Done! " << endl;

}
