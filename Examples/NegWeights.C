#include "StandardRootIncludes.h"

typedef TH1D THist;

void NegWeights()
{
  
  int nbins = 10;
  double x1 = -5, x2 = 5;
  THist *naive = new THist("naive", "naive", nbins, x1, x2);
  naive -> Sumw2();

  std::vector<std::pair<double, double> > values;
  values.push_back(std::make_pair(0., 1));
  values.push_back(std::make_pair(-1., 1));
  values.push_back(std::make_pair(1., 1));
  values.push_back(std::make_pair(1., -1));
  values.push_back(std::make_pair(-2., -1));

  double val, weight;
  for (int i = 0; i < values.size(); ++i) {
    val = values[i].first;
    weight = values[i].second;
    naive -> Fill(val, weight);
    cout << "Filled " << val << " weight=" << weight << "  Mean: " << naive -> GetMean() << endl;
  }

  THist *naive_pos = new THist("naive_pos", "naive_pos", nbins, x1, x2);
  naive_pos -> Sumw2();

  THist *naive_neg = new THist("naive_neg", "naive_neg", nbins, x1, x2);
  naive_neg -> Sumw2();
  

  for (int i = 0; i < values.size(); ++i) {
    val = values[i].first;
    weight = values[i].second;
    if (weight > 0)
      naive_pos -> Fill(val, weight);
    else
      naive_neg -> Fill(val, TMath::Abs(weight));
  }


  cout << "Naive wrong mean: " << naive -> GetMean() << endl;

  THist *combined = (THist*) naive_pos -> Clone("sum");
  combined -> SetTitle("combined");
  combined -> Add(naive_neg, -1.);
  cout << "Combined mean: " << combined -> GetMean() << endl;
  
  TCanvas *can = new TCanvas();
  can -> Divide(2, 1);
  can -> cd(1);
  naive -> Draw();
  can -> cd(2);
  combined -> Draw();
  

}
