// jk 11.3.2025


// ________________________________________________________________

TH2F* adjustTitle(TString name, TString title) {
  TH2F* h = (TH2F*)gROOT->FindObject(name);
  h ->SetTitle(title);
  return h;
}

// ________________________________________________________________

void cd(TCanvas *can, int &i) {
  can -> cd(i);
  i++;
  gPad->SetLogz(1);
}

// ________________________________________________________________

TH1* drawHisto(TTree* tree, TCanvas *can, int &ican, TString var, TString title, TString cuts = "", TString range="", TString opt = "")
// range can be e.g. "(50, 0, 5, 50, 0, 5)"
{
  cd(can, ican);
  TString hname = TString(can->GetName()) + Form("_histo%i", ican);

  // the drawing itself;)
  tree->Draw(var + " >> " + hname + range, cuts, opt);

  TH2F* h = adjustTitle(hname, title);
  return h;

}


// ________________________________________________________________
TH1F* drawHisto1d(TTree* tree, TCanvas *can, int &ican, TString var, TString cuts = "", TString range="", TString title = "")
{
  if (title == "")
    title = cuts + (";" + var + ";Events").ReplaceAll(".", " ");
  return (TH1F*) drawHisto(tree, can, ican, var, title, cuts, range, "hist");
}

// ________________________________________________________________
TH2F* drawHisto2d(TTree* tree, TCanvas *can, int &ican, TString varx, TString vary, TString cuts = "", TString range="", TString title = "")
{
  if (title == "")
    title = cuts + (";" + varx + ";" + vary + "'Events").ReplaceAll("."," ");
  TString var = vary + " : " + varx;
  return (TH2F*) drawHisto(tree, can, ican, var, title, cuts, range, "colz");
}


// ________________________________________________________________

void treeDrawExample()
{

  TFile *file = new TFile("output/ntuple_000409.root", "read");


  TTree* tree = (TTree*) file -> Get("ACT0L");

  TString friendNames[] = {"ACT0R",
			   "ACT1L", "ACT1R",
			   "ACT2L", "ACT2R",
			   "ACT3L", "ACT3R",
			   "TOF00", "TOF01", "TOF02", "TOF03",
			   "TOF10", "TOF11", "TOF12", "TOF13",
			   "Hole0", "Hole1",
			   "PbGlass"
  };

  for (auto friendName : friendNames) {
    tree -> AddFriend(friendName);
  }

  // vars
  TString t0  = "(TOF00.PeakTime + TOF01.PeakTime + TOF02.PeakTime + TOF03.PeakTime) / 4";
  TString t1  = "(TOF10.PeakTime + TOF11.PeakTime + TOF12.PeakTime + TOF13.PeakTime) / 4";

  TCanvas *can2 = new TCanvas("plots2d", "plots2d", 0, 0, 1200, 800);
  can2 -> Divide(3,2);
  int ican = 1;

  // fullest choice:
  // varx, vary, cuts, range:
  auto h1 = drawHisto2d(tree, can2, ican, "ACT3L.PeakVoltage", "ACT3L.IntCharge", "PbGlass.PeakVoltage > 0.5", "(50, 0, 3, 50, 0, 3)");
  auto h2 = drawHisto2d(tree, can2, ican, "ACT3L.IntCharge", "ACT3R.IntCharge", "");
  auto h3 = drawHisto2d(tree, can2, ican, "ACT2L.IntCharge", "ACT2R.IntCharge");
  auto h4 = drawHisto2d(tree, can2, ican, "PbGlass.PeakVoltage", "ACT3L.IntCharge", "");
  auto h5 = drawHisto2d(tree, can2, ican, "PbGlass.PeakVoltage", "ACT2L.IntCharge");
  auto h6 = drawHisto2d(tree, can2, ican, "TOF00.PeakVoltage", "TOF10.PeakVoltage");
  
  TCanvas *can1 = new TCanvas("plots1d", "plots1d", 200, 200, 1200, 800);
  can1 -> Divide(3,2);
  ican = 1;
  auto h7 = drawHisto1d(tree, can1, ican, "TOF00.PeakVoltage");
  auto h8 = drawHisto1d(tree, can1, ican, "TOF11.PeakVoltage");
  auto h9 = drawHisto1d(tree, can1, ican, "PbGlass.PeakVoltage", "PbGlass.PeakVoltage > 0.1");
  auto h10 = drawHisto1d(tree, can1, ican, t1 + " - " + t0, "", "(40, 8, 28)", "t1-t0 [ns]");


}
