
// jk
// using https://root.cern/doc/master/classROOT_1_1RDataFrame.html#crash-course


void rdataFrameAnalysis_simple(TString fname = "output/ntuple_000409.root")
{

  gStyle->SetPalette(kDarkBodyRadiator);
  gStyle -> SetOptStat(0);

  // simple, w/o a friend tree
  //auto infile = TFile::Open(fname);
  //auto df = new ROOT::RDataFrame("PbGlass", infile);

  // get TTrees, make some friends
  auto infile = TFile::Open(fname);
  auto mainTree  = (TTree*) infile -> Get("PbGlass");
  auto otherTree = (TTree*) infile -> Get("ACT2L");
  mainTree -> AddFriend(otherTree, "ACT2L");
  // define the data frame
  auto df = new ROOT::RDataFrame(*mainTree);
  
  // define selections and histograms
  auto h1 = df -> Filter("nPeaks == 1").Histo1D("PeakVoltage");
  auto hall = df -> Filter("nPeaks > 0").Histo1D("PeakVoltage");
  auto hn = df -> Histo1D("nPeaks");
  auto hact2l = df -> Filter("ACT2L.nPeaks > 0").Histo1D("ACT2L.PeakVoltage");

  auto modelH2 = ROOT::RDF::TH2DModel("myh2","myh2", 50, 0, 2, 50, 0, 2);
  auto hact2lvsPbGlass = df -> Filter("ACT2L.nPeaks > 0 && nPeaks > 0").Histo2D(modelH2, "PeakVoltage", "ACT2L.PeakVoltage");

  
  // boring drawing
  
  auto can = new TCanvas();
  can -> Divide(2,2);

  can -> cd(1);
  auto hallcp = hall->DrawCopy("hist");  // event loop is run once here
  auto h1cp = h1->DrawCopy("hist same"); // no need to run the event loop again
  h1cp -> SetLineColor(kRed);
  gPad -> SetLogy(1);
  gPad -> Update();
  
  can -> cd(2);
  auto hncp = hn -> DrawCopy("hist");
  gPad -> Update();

  can -> cd(3);
  auto hact2lcp = hact2l -> DrawCopy();

  can -> cd(4);
  auto hact2lvsPbGlasscp = hact2lvsPbGlass -> DrawCopy("colz");
  gPad -> SetLogz(1);
  gPad -> Update();
  
  can -> Update();

  
}
