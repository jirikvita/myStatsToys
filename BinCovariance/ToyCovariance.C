// jiri kvita 7.4.2013

#include "ToyCovariance.h"

// ________________________________________________________________

ToyCovariance::ToyCovariance(int Nbins, int HistBins,
			     double Min, double Max, 
			     double Min2, double Max2, // axis ranges for products
			     int debug, int Mode) : _Nbins(Nbins),
						    _nHistBins(HistBins),
						    _Zmin(Min), _Zmax(Max),
						    _Zmin2(Min2), _Zmax2(Max2),
						    _Cov(0), _Corr(0), _debug(debug), _mode(Mode)
						    
						    // Mode:
						    // 0: build the covariance from <x*y> - <x>*<y>
						    // otherwise it is assumed that the covariance was filled directly, so we just need to take means


{
  this -> Init();
}

// ________________________________________________________________

void ToyCovariance::Init()
{

  for (unsigned int i = 0; i < _Nbins; ++i) {
    string name = Form("hmean_%i", i);
    _hmeans.push_back(new TH1D(name.c_str(), name.c_str(), _nHistBins, _Zmin, _Zmax));

    vector<TH1D*> vecprod;
    vector<TH2D*> veccorr;
    double diffSF = 10;
    for (unsigned int j = 0; j <= i; ++j) {
      name = Form("hprod_%i_%i", i, j);
      if (_Zmin2 < _Zmax2)
	vecprod.push_back(new TH1D(name.c_str(), name.c_str(), _nHistBins, _Zmin2,  _Zmax2));
      else
	vecprod.push_back(new TH1D(name.c_str(), name.c_str(), _nHistBins, (_Zmin < 0 ? -1. : 1.)*_Zmin*_Zmin,  (_Zmax < 0 ? -1. : 1.)*_Zmax*_Zmax));
      name = Form("hcorr2d_%i_%i", i, j);
      if (_mode != 0)
	veccorr.push_back(new TH2D(name.c_str(), name.c_str(), 2*_nHistBins, -_Zmax/diffSF, _Zmax/diffSF, _nHistBins, -_Zmax/diffSF, _Zmax/diffSF));
      else
	veccorr.push_back(new TH2D(name.c_str(), name.c_str(), 2*_nHistBins, _Zmin/diffSF, _Zmax/diffSF, _nHistBins, _Zmin/diffSF, _Zmax/diffSF));
    }
    _hproducts.push_back(vecprod);
    _hcorr2d.push_back(veccorr);
  }

}
// ________________________________________________________________
void ToyCovariance::GetIndices(int &ii, int &jj) 
{
  if (ii < jj) {
    int kk = ii;
    ii = jj;
    jj = kk;
  }
}

// ________________________________________________________________

void ToyCovariance::Fill(int i, double z1, int j, double z2, int FillMode)
{

  // FillMode:
  // 0: old way of filling both means and products
  // 1: Fill only means
  // 2: Fill directly the Covariances using the means obtained by running the first pass of toys

  if (_mode == 0 and (FillMode == 1 or FillMode == 2) ) {
    cerr << "ERROR, class NOT initialized for direct covariance filling and the two passes scheme!" << endl;
    return;
  }
  if ( _mode != 0 and (FillMode != 1 and FillMode != 2) )  {
    cerr << "ERROR, class initialized for direct covariance filling and the two passes scheme, but atempted to be filled in old way!" << endl; 
    return;
  }
  
  if (FillMode == 1 or FillMode == 0) {
    if (_debug > 1) 
      cout << "fill mean z1=" << z1 << " z2=" << z2 << endl;
    if (i < _hmeans.size()) 
      _hmeans[i]->Fill(z1);
    else cerr << "ERROR accesing diagonal i=" << i << endl;
    if (i < _hmeans.size()) 
      _hmeans[j]->Fill(z2);
    else cerr << "ERROR accesing diagonal j=" << j << endl;
  }
  if (FillMode == 1)
    return;
  if (FillMode == 2) {
    // ensure the triangularity:
    int ii = i;
    int jj= j;
    this -> GetIndices(ii, jj);
    if (ii < _hproducts.size()) {
      if (jj < _hproducts[ii].size()) {
	if (_debug > 1) 
	  cout << "fill cov "
	       << " " << (z1 - _hmeans[ii] -> GetMean())
	       << " " << (z2 - _hmeans[jj] -> GetMean())
	       << " " << (z1 - _hmeans[ii] -> GetMean())*(z2 - _hmeans[jj] -> GetMean())
	       << endl;
	_hproducts[ii][jj]->Fill((z1 - _hmeans[ii] -> GetMean())*(z2 - _hmeans[jj] -> GetMean()));
	_hcorr2d[ii][jj]->Fill(z1 - _hmeans[ii] -> GetMean(), z2 - _hmeans[jj] -> GetMean());
      } else cerr << "ERROR accesing column " << jj << endl;
    } else cerr << "ERROR accesing line " << ii << endl;
    return;
  }
  
  // fill all in case FillMode is not 1 nor 2:
    
  // ensure the triangularity:
  int ii = i;
  int jj= j;
  this -> GetIndices(ii, jj);
    
  if (ii < _hproducts.size()) {
    if (jj < _hproducts[ii].size()) {
      if (_debug > 1) 
	cout << "fill prod" << endl;
      _hproducts[ii][jj]->Fill(z1*z2);
      _hcorr2d[ii][jj]->Fill(z1, z2);
	
    } else cerr << "ERROR accesing column " << jj << endl;
  } else cerr << "ERROR accesing line " << ii << endl;
    
  if (_debug > 1) 
    cout << "Done Fill" << endl;
    
} // Fill

// ________________________________________________________________

void ToyCovariance::Fill(TH1D *htoy, int FillMode)
{
  for (int i = 0; i < _Nbins; ++i) {
    for (int j = 0; j <= i; ++j) {
      if (_debug > 1) {
	cout << htoy -> GetName() << endl;
	cout << i << " " << htoy -> GetBinContent(i+1) << endl;
	cout << j << " " << htoy -> GetBinContent(j+1) << endl;
      }
      this -> Fill(i, htoy -> GetBinContent(i+1), j, htoy -> GetBinContent(j+1), FillMode);
    }
  }
} // Fill




// ________________________________________________________________

TCanvas* ToyCovariance::DrawProductHistos()
{

  TString name = "canproducts";
  TCanvas *can = new TCanvas(name, name, 0, 400, 500, 500);
  can -> Divide(_Nbins, _Nbins);
  for (int i = 0; i < _Nbins; ++i) {
    for (int j = 0; j <= i; ++j) {
      can -> cd(1+i*_Nbins + j);
      gPad -> SetLogy();
      _hproducts[i][j] -> Draw("hist");
    }
  }
  return can;
}

// ________________________________________________________________

TCanvas* ToyCovariance::DrawCorr2d()
{

  TString name = "can2d";
  TCanvas *can = new TCanvas(name, name, 800, 500, 800, 600);
  can -> Divide(_Nbins, _Nbins);
  for (int i = 0; i < _Nbins; ++i) {
    for (int j = 0; j <= i; ++j) {
      can -> cd(1+i*_Nbins + j);
      _hcorr2d[i][j] -> Draw("col");
    }
  }
  return can;
}


// ________________________________________________________________

TCanvas* ToyCovariance::DrawMeanHistos()
{
  TString name = "canmean";
  TCanvas *can = new TCanvas(name, name, 0, 0, 1000, 400);
  can -> Divide(_Nbins, 1);
  for (int i = 0; i < _Nbins; ++i) {
    can -> cd(1+i);
    _hmeans[i] -> Draw("hist");
  }
  return can;
}

// ________________________________________________________________

TMatrixD *ToyCovariance::GetCovariance()
{
  this -> EnsureCov();
  return _Cov;
}

// ________________________________________________________________

TMatrixD *ToyCovariance::GetCorrelation()
{
  this -> EnsureCorr();
  return _Corr;
}



// ________________________________________________________________
 TMatrixD * ToyCovariance::MakeEmptyCov()
  {
    return  new TMatrixD(_Nbins, _Nbins);
  }

// ________________________________________________________________
  void ToyCovariance::EnsureCov()
  {
    if (_Cov)
      return;

    _Cov = this -> MakeEmptyCov();

    if (_mode == 0) {
	for (int i = 0; i < _Nbins; ++i) {
	  for (int j = 0; j < _Nbins; ++j) {
	    int ii = i;
	    int jj = j;
	    this -> GetIndices(ii, jj);
	    (*_Cov)[i][j] = _hproducts[ii][jj] -> GetMean() - _hmeans[ii] -> GetMean() * _hmeans[jj] -> GetMean();
	  }
	}
    } else {
      	for (int i = 0; i < _Nbins; ++i) {
	  for (int j = 0; j < _Nbins; ++j) {
	    int ii = i;
	    int jj = j;
	    this -> GetIndices(ii, jj);
	    (*_Cov)[i][j] = _hproducts[ii][jj] -> GetMean();
	  }
	}
    }

  }
// ________________________________________________________________
  void ToyCovariance::EnsureCorr()
  {
    if (_Corr)
      return;
    
    this -> EnsureCov();

   _Corr = new TMatrixD(_Nbins, _Nbins);
    for (int i = 0; i < _Nbins; ++i) {
      for (int j = 0; j < _Nbins; ++j) {
	(*_Corr)[i][j] = (*_Cov)[i][j] / sqrt((*_Cov)[i][i]*(*_Cov)[j][j]);
      }
    }
    

  }

// ________________________________________________________________
// ________________________________________________________________
