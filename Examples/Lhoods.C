

// jk
// Fri Feb 11 14:27:57 CET 2011


void Lhoods()

{


 
  double mean = 10.;
  double x1 = 0.;
  double x2 = 4*mean;
  double sigma = 2.;
  
  TF1 *logPois = new TF1("logPois", "[0]*log(x)-x", x1, x2);
  logPois -> SetParameter(0, mean);
  logPois -> SetLineColor(kBlue);

  TF1 *logGaus = new TF1("logPois", "-(x-[0])^2/(2*[1]^2)", x1, x2);
  logGaus -> SetParameters(mean, sigma);
  logGaus -> SetLineColor(kRed);
  
  TCanvas *can = new TCanvas("logLh");

  can -> cd();
  logPois -> Draw();
  logGaus -> Draw("same");

}
