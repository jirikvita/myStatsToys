

#include "StandardRootIncludes.h"
#include "TRandom3.h"

void FillRandom()
{

  TRandom3 rand;
  
  int nbins = 50;
  double x1 = 10.;
  double x2 = 100.;

  TF1 *sigfun = new TF1("sigfun", "[0]*exp(-(x-[1])^2/(2*[2]^2))", x1, x2);
  sigfun -> SetParameters(1., 40., 10.);
  TF1 *bgfun = new TF1("bgfun", "[0]*exp(-[1]*x)", x1, x2);
  bgfun -> SetParameters(1., 0.08);

  int Nsig = 200;
  int Nbg = 1000;

  TH1D *hsig = new TH1D("hsig", "hsig", nbins, x1, x2);
  hsig -> FillRandom("sigfun", rand.Poisson(Nsig));

  TH1D *hbg = new TH1D("hbg", "hbg", nbins, x1, x2);
  hbg -> FillRandom("bgfun", rand.Poisson(Nbg));

  TH1D *hall = (TH1D*) hsig -> Clone("hall");
  hall -> Add(hbg);
  hall -> SetTitle("data");

  TCanvas *can = new TCanvas("can", "can", 0, 0, 1200, 600);
  can -> Divide(3, 1);

  can -> cd(1);
  hsig -> Draw("e1");

  can -> cd(2);  
  hbg -> Draw("e1");

  can -> cd(3);
  gPad -> SetLogy();
  hall -> Draw("e1");

}
