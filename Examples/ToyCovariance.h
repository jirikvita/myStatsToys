// jiri kvita 7.4.2013

#ifndef TOYCOVARIANCE_H
#define TOYCOVARIANCE_H

#include <vector>
#include <iostream>
#include <string>

using std::vector;
using std::cout;
using std::endl;
using std::cerr;
using std::string;

#include "TMatrixD.h"

typedef vector< vector<TH1D*> > MyHistoStruct;
typedef vector< vector<TH2D*> > MyHistoStruct2;

class ToyCovariance {

 public:
  ToyCovariance(int Nbins, int HistBins,
		double Min, double Max, 
		double Min2, double Max2, 
		int debug, int Mode);
  ~ToyCovariance() {};


  void Init();
  void GetIndices(int &ii, int &jj);

  void Fill(int i, double z1, int j, double z2, int FillMode);
  void Fill(TH1D *htoy, int FillMode);

  TCanvas* DrawProductHistos();
  TCanvas* DrawMeanHistos();
  TCanvas* DrawCorr2d();
  
  TMatrixD *GetCovariance();
  TMatrixD *GetCorrelation();

 private:

  int _mode;

  int _Nbins;
  int _nHistBins;
  double _Zmin;
  double _Zmax;
  double _Zmin2;
  double _Zmax2;
  int _debug;

  vector<TH1D*> _hmeans; // to be filled with results over toys, to obtain the means of <z_i> in each bin of i
  MyHistoStruct _hproducts; // to be filled by products of z_i*z_j to post-compute the covariance Cov(i,j) = <z_i><z_j> - <z_i*z_j>
  MyHistoStruct2 _hcorr2d;

  TMatrixD *_Cov;
  TMatrixD *_Corr;
  
  TMatrixD * MakeEmptyCov();
  void EnsureCov();
  void EnsureCorr();


};

#endif
