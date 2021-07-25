/* 
 * Author: Oldrich Kepka
 * Modified by: Jiri Kvita
 * Example: BMI - body mass index
 * Given: sample with weight and height of the population
 *
 * Compute: 
 *  1) mean and standard deviation for weight and height variables
 *  2) their covariance and correlation coefficient of mass and weight
 *  3) use 1) and 2) to calculate mean and variance of BMI index (BMI = weight/ (height * height). Hint: Pay attention which variables need to be correlated
 *  4) how does the standard deviation changes if correlation is neglected?
 *  5) compare results of 3) to standard deviation obtained from BMI sample distribution
 */


#include "TH1D.h"
#include "TH2D.h"
#include "TRandom3.h"
#include "TCanvas.h"
#include "TFile.h"
#include "TStyle.h"
#include "TChain.h"

#include <math.h>
#include <iostream>

// jk
#include "ToyCovariance.C"

using std::cout;
using std::endl;

struct Event {

   float bmi;
   float h;
   float w;

};


int main() {


   gStyle-> SetOptStat(1111);
   gStyle-> SetOptTitle(0);

   TFile * f       = TFile::Open("lidska_populace.root");
   TTree * fChain;
   f->GetObject("tree_lidi",fChain);
   if (fChain == 0) return 1;


   Event ev;
   fChain->SetBranchAddress("height", &ev.h);
   fChain->SetBranchAddress("weight", &ev.w);


   double hmin = 150.;
   double hmax = 210.;
   double wmin = 0.;
   double wmax = 150.;

   // histos
   TH2D *h_hw       = new TH2D("h_hw"    , "People Sample;height [cm]; weight [kg]",
				60, hmin, hmax,
				150, wmin, wmax );
   TH1D *h_bmi      = new TH1D("h_bmi"   , "BMI; BMI", 
				100, 15, 50 );

   TH1D *h_height       = new TH1D("h_h"    , "People Sample;height [cm];",
				   60, hmin, hmax);
   TH1D *h_weight       = new TH1D("h_w"    , "People Sample;weight [kg]",
				  150, wmin, wmax);
   // loop
   Long64_t nentries = fChain->GetEntriesFast();
   Long64_t nbytes = 0, nb = 0;

   // jk
   int Nbins = 2; // one for height, one for mass;-)
   int nFineBins = 400;

  double zmin = 0.;
  double zmax = 250.;
  // zoom to zmin/max:
  double zoommin = 0.;
  double zoommax = 250;

  int debug = 0;
  int Mode = 0;

  ToyCovariance *toy = new ToyCovariance(Nbins, nFineBins, zmin, zmax, zmin*zmin, zoommax*zoommax, debug, Mode);
   
  cout << "Loop1..." << endl;
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Long64_t ientry = fChain->LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
 
    if (jentry % 1000 == 0)
      cout << "Processing " << jentry
	   << " ev.h=" << ev.h
	   << " ev.w=" << ev.w
	   << endl;

   // if (Cut(ientry) < 0) continue;
    
    ev.bmi = (ev.h !=0 ) ? ev.w/ev.h/ev.h*1e4 : -999;  //cm -> m
    
    h_hw     -> Fill(ev.h, ev.w);
    h_height     -> Fill(ev.h);
    h_weight     -> Fill(ev.w);
    h_bmi    -> Fill(ev.bmi);
    
    
    toy -> Fill(0, ev.h, 1, ev.w, Mode);
    toy -> Fill(0, ev.h, 0, ev.h, Mode);
    toy -> Fill(1, ev.w, 1, ev.w, Mode);
    
    
  }


  /*
  //  f->Close();
  // second loop
  TFile * g       = TFile::Open("lidska_populace2.root");
  TTree * gChain;
  g->GetObject("tree_lidi",gChain);
  if (gChain == 0) return 1;
  gChain->SetBranchAddress("height", &ev.h);
  gChain->SetBranchAddress("weight", &ev.w);


  // _________________________________

  cout << "Loop2..." << endl;
  Mode = 2;
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
    Long64_t ientry = gChain->LoadTree(jentry);
    if (jentry % 1000 == 0)
      cout << "Processing " << jentry
	   << " ev.h=" << ev.h
	   << " ev.w=" << ev.w
	   << endl;

    toy -> Fill(0, ev.h, 1, ev.w, Mode);
  }

  */

   // plot
   TCanvas *c = new TCanvas("c", "c", 0, 0, 800, 600);
   h_hw-> Draw("colz");
   cout << "Correlation coefficient from the TH2: " << h_hw -> GetCorrelationFactor() << endl;
   c-> SaveAs("hw.pdf");
   c-> SaveAs("hw.png");

   c-> Clear();
   h_height-> Draw();
   c-> SaveAs("height.png");
   c-> SaveAs("height.pdf");

   c-> Clear();
   h_weight-> Draw();
   c-> SaveAs("weight.png");
   c-> SaveAs("weight.pdf");

   c-> Clear();
   h_bmi-> Draw();
   c-> SaveAs("bmi.png");
   c-> SaveAs("bmi.pdf");


   // Olda:) test c++11 
   // auto i = 3;


   toy -> DrawProductHistos();
   toy -> DrawMeanHistos();
   toy -> DrawCorr2d();
   

   TMatrixD * Cov = toy -> GetCovariance();
   TMatrixD * Corr = toy -> GetCorrelation();
   
   cout << "Covariance matrix: " << endl;
   Cov -> Print();
   cout << "Correlation matrix: " << endl;
   Corr -> Print();
   
   double meanh = h_hw -> GetMean(1) / 100.;
   double meanw = h_hw -> GetMean(2);
   double meanB = h_bmi -> GetMean();

   double rmsh = h_hw -> GetRMS(1) / 100.;
   double rmsw = h_hw -> GetRMS(2);
   double rmsB = h_bmi -> GetRMS();
   cout << " meanh: " << meanh << endl 
	<< " meanw: " << meanw << endl 
	<< " meanB: " << meanB << endl 
	<< " rmsh: " << rmsh << endl 
	<< " rmsw: " << rmsw << endl 
	<< " rmsB: " << rmsB << endl 
	<< endl;

   double rho = h_hw -> GetCorrelationFactor();
   double derivatives = -2*meanw/pow(meanh,5);
   double sigmaB = sqrt(  pow(meanB*rmsw/meanw, 2) + pow(2*meanB*rmsh/meanh, 2) + 2*rho*derivatives*rmsh*rmsw );
   double sigmaBnoCorr = sqrt(  pow(meanB*rmsw/meanw, 2) + pow(2*meanB*rmsh/meanh, 2) );
   cout << "Error propagation for B: " << endl
	<< " sigmaBnoCorr: " << sigmaBnoCorr << endl 
	<< " sigmaB: " << sigmaB << endl;
   
}

