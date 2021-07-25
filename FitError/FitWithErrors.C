// #include ".h"

// jiri kvita, 2009-2014

#include "TMatrixD.h"
#include "TMinuit.h"

#include "StandardRootIncludes.h"

using std::cout;
using std::cerr;
using std::endl;

// global variables for fit errors:

const int MaxNFitPars = 4;
const int MaxNFitParsDer = 5;
const int NFits = 5;


 // fit formulas
const int NFitPars[NFits] = {3, 1, 3, 4, 3};

TString FitFormulasTag[NFits];

// fit and derivatives w.r.t. parameters:
TString FitFormulas[NFits][MaxNFitParsDer];


int gnpars;
TString gFitFormula;
TString gDerivativesFormula[MaxNFitPars];
TF1 *gfit;
TF1 *gderivatives[MaxNFitPars];
TMatrixD *gmnemat;
double gSigma = 1.;



void FillFitFormulas()
{
  FitFormulasTag[0] =  "exponential"; 
  FitFormulasTag[1] =  "constant"; 
  FitFormulasTag[2] =  "quadratic"; 
  FitFormulasTag[3] =  "cubic"; 
  FitFormulasTag[4] =  "gauss";

// fit and derivatives w.r.t. parameters:
  FitFormulas[0][0] =  "[0]*(1 - [1]*exp(-[2]*x))"; 
  FitFormulas[0][1] = "1 - [1]*exp(-[2]*x)"; 
  FitFormulas[0][2] =  "-[0]*exp(-[2]*x)"; 
  FitFormulas[0][3] = "x*[0]*[1]*exp(-[2]*x)";
  
  FitFormulas[1][0] = "[0]"; FitFormulas[1][1] =  "1.";

  FitFormulas[2][0] = "[0] + [1]*x + [2]*x^2"; 
  FitFormulas[2][1] = "1"; 
  FitFormulas[2][2] = "x"; 
  FitFormulas[2][3] = "x^2";;

  FitFormulas[3][0] = "[0] + [1]*x + [2]*x^2 + [3]*x^3"; 
  FitFormulas[3][1] =  "1"; 
  FitFormulas[3][2] = "x"; 
  FitFormulas[3][3] =  "x^2"; 
  FitFormulas[3][4] =  "x^3";

  FitFormulas[4][0] = "[0]*exp(-(x - [1])^2 / (2*[2]^2))"; 
  FitFormulas[4][1] =  "exp(-(x - [1])^2 / (2*[2]^2))"; 
  FitFormulas[4][2] = "(x-[1])/[2]^2*[0]*exp(-(x - [1])^2 / (2*[2]^2))"; 
  FitFormulas[4][3] = "(x-[1])^2/[2]^3*[0]*exp(-(x - [1])^2 / (2*[2]^2))";


}


// ___________________________________________________________


// get the statistical df
double GetFitStatErrorX (int npars, double *par, TMatrixD *mnemat, double x, TF1 *fit, TF1 **derivatives, bool verbose = false)
{
  
  /* analytical approach: */
  double df = 0.;
  for(int j = 0; j < npars; ++j) {
    for(int k = 0; k < npars; ++k) {
      //      cout << "*** (j,k)=" << "(" << j <<"," << k << ") ***" << endl;
      double ddf = (derivatives[k] -> Eval(x))
	* (derivatives[j] -> Eval(x))
	*  (*mnemat)(j,k); 
      df += ddf;
      
    } // k
  } // j
  //  cout << "df=" << df << endl;
  return  sqrt(df);
  
}
// ___________________________________________________________

double ShiftedFitUp(double *x, double *par)
{
  
  double df = GetFitStatErrorX (gnpars, par, gmnemat, x[0], gfit, gderivatives, false);
  double value = (gfit -> Eval(x[0]) + gSigma*df);
  /*
    if (value < 0.)
    return 0.;
    if (value > 1.)
    return 1.;
  */
  return value;
}
// ___________________________________________________________

double ShiftedFitDown(double *x, double *par)
{
  
  double df = GetFitStatErrorX (gnpars, par, gmnemat, x[0], gfit, gderivatives, false);
  double value = (gfit -> Eval(x[0]) - gSigma*df);
  /*
    if (value < 0.)
    return 0.;
    if (value > 1.)
    return 1.;
  */
  return value;

}
// ___________________________________________________________


class MyFitResult {
public:
  TF1 *fit;
  TF1 *fitUp;
  TF1 *fitDown;

  MyFitResult()
  {
    fit = 0;
    fitUp = 0;
    fitDown = 0;
  };
  
  ~MyFitResult() {};
 
};

// ___________________________________________________________

MyFitResult* GetFitWithErrors(TH1D *histo, int iFitForm = 4)
{
  
  MyFitResult *results = new MyFitResult();

  int npars = NFitPars[iFitForm]; 
  gnpars = npars;
  gFitFormula = FitFormulas[iFitForm][0];
  for (int j = 0; j < npars; ++j)
    gDerivativesFormula[j] = FitFormulas[iFitForm][j+1];
    
    
  results -> fit = new TF1(Form("central_fit_%s_%i", histo -> GetName(),iFitForm),
			FitFormulas[iFitForm][0].Data(), 
			histo -> GetXaxis() -> GetXmin(),
			histo -> GetXaxis() -> GetXmax());
  gfit = results -> fit; // important!!!
  results -> fit -> SetLineColor(2);
  results -> fit -> SetLineWidth(1);

  // set pars!?
  //  for (int j = 0; j < npars; ++j)
  //    results -> fit -> SetParameter(j, par[j]);

  results -> fit -> SetParameter(0, histo -> GetMaximum());
  results -> fit -> SetParameter(1, histo -> GetMean());
  results -> fit -> SetParameter(2, histo -> GetRMS());
    
  gStyle->SetOptFit(0);
  histo -> SetStats(0);

  // central fit:
  histo -> Fit(results -> fit);


  // now erros:

  TMatrixD *mnemat = new TMatrixD(npars, npars);
  gMinuit -> mnemat(mnemat -> GetMatrixArray(), npars);
  cout << "npars=" << npars << ", Free error matrix: " << endl;
  mnemat -> Print();		    
  gmnemat = mnemat;

  cout << "Setting up derivatives..." << endl;
  TF1 *derivatives[NFitPars[iFitForm]];
  for (int j = 0; j < npars; ++j) {
    cout << "derivative " << j << ": " << gDerivativesFormula[j].Data() << endl;
    derivatives[j] = new TF1(Form("fit_%s_%i", histo -> GetName(),iFitForm),
			     gDerivativesFormula[j].Data(), 
			     histo -> GetXaxis() -> GetXmin(),
			     histo -> GetXaxis() -> GetXmax());
    for (int k = 0; k < npars; ++k)
      derivatives[j] -> SetParameter(k, results -> fit -> GetParameter(k));
    gderivatives[j] = derivatives[j];
  }

  cout << "fit up..." << endl;
  results -> fitUp = new TF1(Form("fitUp_%s_%i", histo -> GetName(),iFitForm),
			     ShiftedFitUp,
			     histo -> GetXaxis() -> GetXmin(),
			     histo -> GetXaxis() -> GetXmax());
  results -> fitUp -> SetLineWidth(1);
  results -> fitUp -> SetLineStyle(2);

  cout << "fit down..." << endl;
  results -> fitDown = new TF1(Form("fitDown_%s_%i", histo -> GetName(),iFitForm),
			       ShiftedFitDown,
			       histo -> GetXaxis() -> GetXmin(),
			       histo -> GetXaxis() -> GetXmax());
  results -> fitDown -> SetLineWidth(1);
  results -> fitDown -> SetLineStyle(2);
   
 

  // results -> fitUp -> Draw("same");
  //  results -> fitDown -> Draw("same");
  // results -> fitUp -> DrawClone("same");
  // results -> fitDown -> DrawClone("same");

  cout << "return..." << endl;

  results -> fit -> SetNpx(400);
  results -> fitUp -> SetNpx(400);
  results -> fitDown -> SetNpx(400);

  return results;


}


// ___________________________________________________________
// ___________________________________________________________
// ___________________________________________________________


void FitWithErrors(int Nevts = 1320, int iFitForm = 4)
{

  FillFitFormulas();

  gStyle->SetOptTitle(0);
  
  double x1 = 0.;
  double x2 = TMath::TwoPi();
  int nbins = 32;

  TString fitform = FitFormulas[iFitForm][0];
  TString fitname = FitFormulasTag[iFitForm];

  cout << " fitform=" << fitform.Data()
       << " fitname=" << fitname.Data()
       << endl;

  TF1 *genFun = new TF1(fitname, fitform, x1, x2);
  genFun -> SetParameters(1., TMath::Pi(), TMath::Pi()/3.);

  TH1D *histo = new TH1D("histo", "histo", nbins, x1, x2);
  histo -> FillRandom(fitname, Nevts);
  histo -> SetMarkerColor(kBlack);
  histo -> SetLineColor(kBlack);
  histo -> SetMarkerSize(1);
  histo -> SetMarkerStyle(20);

  MyFitResult *results = GetFitWithErrors(histo);

  cout << "draw..." << endl;


  TCanvas *can = new TCanvas("GaussFitError");
  can -> cd();
  can -> Draw();
  histo -> Draw("e1");

  cout << "pointers: "
       << " " << results -> fit
       << " " <<  results -> fitUp
       << " " <<  results -> fitDown
       << endl;

  results -> fit -> Draw("same");
  results -> fitUp -> Draw("same");
  results -> fitDown -> Draw("same");

  TLatex* text1 = new TLatex(0.63, 0.83, Form("#chi^{2}/ndf = %2.1f / %i", results->fit->GetChisquare(), results->fit->GetNDF()));
  text1 -> SetNDC();
  text1 -> Draw();
  
  can->Print(TString(can->GetName()) + ".pdf");
  can->Print(TString(can->GetName()) + ".png");


}
