



// Jiri Kvita 8.2.2024
// upon question by Hana Zitnanska, Slovanske Gymnazium


void adjustStats(TH1D* h)
{
  gPad -> Update();
  //auto st = h.GetListOfFunctions().FindObject("stats");
  auto st =  (TPaveStats*) gPad -> GetPrimitive("stats");
  st -> SetX1NDC(0.7);
  st -> SetX2NDC(0.9);
  st -> SetY1NDC(0.65);
  st -> SetY2NDC(0.9);
}



// ________________________________________________________________________________________________________________________________
// ________________________________________________________________________________________________________________________________
// ________________________________________________________________________________________________________________________________

void drawBW2D() {

  gStyle->SetOptTitle(0);
  
  TString cname = "BW2";
  TCanvas can(cname, cname);


  // ________________________________________________________________________________________________________________________________
  
  TF2 bw2("bw2", "[0]*1/( (x^2 - [1]^2)^2 + ([1]*[2])^2 ) * 1/( (y^2 - [1]^2)^2 + ([1]*[2])^2 )", 40, 100, 40, 100);
  bw2.SetParameters(1., 90., 2.);
  bw2.Draw();
  bw2.Draw("lego2");
  bw2.Draw("surf");
  bw2.SetNpx(100);
  bw2.SetNpy(100);
  TH2D hh2("hh2", "2D Breit-Wigner", 100, 40, 100, 100, 40, 100);
  hh2.FillRandom("bw2", 50000);
  // hh2.SetStats(0);
  hh2.Draw("colz");

  cname = "GG2";
  TCanvas cang(cname, cname);
  cang.cd();

  // ________________________________________________________________________________________________________________________________
  
  TF2 g2("g2", "1/sqrt(2*TMath::Pi() * [1]^2) * exp( -(x-[0])^2/(2*[1]^2)) * 1/sqrt(2*TMath::Pi() * [1]^2) * exp( -(y-[0])^2/(2*[1]^2))", 40, 100, 40, 100);
  g2.SetParameters(90., 2.);
  g2.Draw();
  g2.Draw("lego2");
  g2.Draw("surf");
  g2.SetNpx(100);
  g2.SetNpy(100);
  TH2D gg2("gg2", "2D Gauss", 100, 40, 100, 100, 40, 100);
  gg2.FillRandom("g2", 50000);
  // hh2.SetStats(0);
  gg2.Draw("colz");

 
  // ________________________________________________________________________________________________________________________________

  cname = "BWGaussCmp";
  TCanvas can2(cname, cname);
  can2.cd();

  // https://en.wikipedia.org/wiki/Relativistic_Breit%E2%80%93Wigner_distribution
  TF1 BW("BW", "2*sqrt(2)*[0]^2*[1]*sqrt([0]^2+[1]^2)/(TMath::Pi()*sqrt([0]^2 + [0]*sqrt([0]^2+[1]^2))) * 1/( (x^2 - [0]^2)^2 + ([0]*[1])^2 )", 40, 100);
  BW.SetParameters(90., 2.);
    
  TF1 G("", "1/sqrt(2*TMath::Pi() * [1]^2) * exp( -(x-[0])^2/(2*[1]^2))", 40, 100);
  G.SetParameters(90., 2.);

  BW.SetNpx(1000);
  BW.SetLineColor(kBlue);
  G.SetNpx(1000);
  G.SetLineColor(kRed);


  BW.Draw();
  G.Draw("same");  
  


  
  
}
