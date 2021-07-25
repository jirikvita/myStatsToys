// jk 3.5.2013

#include "TMatrixD.h"
#include "TVectorD.h"
#include "TH1D.h"

#include <iostream>

using std::endl;
using std::cerr;
using std::cout;


// functions provided:
// ________________________________________________________________

void PrettyLaTeXPrintMatrix(TMatrixD *Cov);
TMatrixD* MakeVector(TH1 *hist, bool MakeRow);
double GetChisquared(TH1 *h1, TH1 *h2, TMatrixD *Cov);
// ________________________________________________________________

void PrettyLaTeXPrintMatrix(TMatrixD *Cov)
{
  if (not Cov)
    return;
  
  int nr =Cov->GetNrows();
  int nc =Cov->GetNcols();
  cout << "\\begin{tabular}{";
  for (int i = 0; i < nc; ++i) 
    cout << "l";
  cout << "}" << endl;
  for (int i = 0; i < nr; ++i) {
    for (int j = 0; j < nc; ++j) {
	cout << " " << (*Cov)[i][j];
	if (j < nr-1)
	  cout << " & ";
      }
      cout << " \\\\" << endl;
  }
    cout << "\\end{tabular}" << endl;
  return;

}

// ________________________________________________________________

TMatrixD* MakeVector(TH1 *hist, bool MakeRow)
{

  if (not hist) {
    cerr << "MakeVector: Error getting pointer!" << endl;
    return 0;
  }

  int n = hist -> GetXaxis() -> GetNbins();
  //  TVectorD *vec = new TVectorD(n);
  TMatrixD *vec = 0;
  if (MakeRow)
    vec = new TMatrixD(n, 1);
  else
    vec = new TMatrixD(1, n);
  for (int i = 0; i < n; ++i) {
    if (MakeRow)
      (*vec)[i][0] = hist -> GetBinContent(i+1);
    else
      (*vec)[0][i] = hist -> GetBinContent(i+1);
  }

  return vec;

}


// ________________________________________________________________


 double GetChisquared(TH1 *data, TH1 *theory, TMatrixD *Cov, bool UseTheoryErrors)
{

  if (not data or not theory or not Cov) {
    cerr << "GetChisquared: Error getting pointers!" << data << " " << theory << " " << Cov << endl;
    return -999.;
  }

  // computes generalized chi2 as
  // (data-theory) Cov^{-1} (data-theory)^2,
  // where the covariance is the covariance matrix from data.
  // Option is to add to the Cov the errors from the theory.

  TMatrixD TheoryCov(Cov->GetNrows(), Cov->GetNcols());
  if (UseTheoryErrors) {
    for (int ii = 0; ii < Cov->GetNrows(); ++ii)
      TheoryCov[ii][ii] = pow(theory -> GetBinError(ii+1), 2);
  }
  
  TMatrixD Inv = *Cov + TheoryCov;
  Inv.Invert();

  // row and column vector representations of the histogram
  TMatrixD *datar = MakeVector(data, true);
  TMatrixD *theoryr = MakeVector(theory, true);
  TMatrixD *datac = MakeVector(data, false);
  TMatrixD *theoryc = MakeVector(theory, false);


  cout << "Covariance: " << endl;
  PrettyLaTeXPrintMatrix(Cov);
  cout << "Inversion: " << endl;
  PrettyLaTeXPrintMatrix(&Inv);
  cout << "Vectors: " << endl;
  // PrettyLaTeXPrintMatrix(datar);
  //   PrettyLaTeXPrintMatrix(theoryr);
  PrettyLaTeXPrintMatrix(datac);
  PrettyLaTeXPrintMatrix(theoryc);
 
  // the real meat;-) 
  TMatrixD chi2M = ((*datac)-(*theoryc)) * Inv * ((*datar)-(*theoryr));
  cout << "Chi2 matrix: " <<endl;
  PrettyLaTeXPrintMatrix(&chi2M);

  //   cout << "Returning the chi2..." << endl;
  return chi2M[0][0];

}
