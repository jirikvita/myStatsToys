#include <fstream>
#include <iostream>

#include "TF1.h"
#include "TH1D.h"
#include "TCanvas.h"

void io_test() {

  // some example
  TF1* fit = new TF1("fun", "gaus", -1, 1);
  fit -> SetParameters(1, 0, 1);
  TH1D *h1 = new TH1D("h1", "h1", 100, -1, 1);
  h1 -> FillRandom("fun", 1000);
  h1 -> Fit(fit);
  cout << "fitmean: " << fit -> GetParameter(1) << endl;
  
  // ascii write to a file
  TString outfilename = "out.txt";
  ofstream *infile = 0;
  infile = new ofstream(outfilename.Data());
  (*infile) << "fitmean: " << fit -> GetParameter(1) << endl;
  if (infile)
    infile->close();

  // ascii read from a file

  ifstream outfile;
  TString inputfilename = outfilename;
  outfile.open(inputfilename.Data());
  if (outfile.is_open()) {
    string s;
    while (outfile >> s) if ((! outfile.fail()) && (s.size())) {
	cout << "Read: " << s.c_str() << endl;
      }
    outfile.close();
  }


}
  
