void can2()
{
//=========Macro generated from canvas: can2/can2
//=========  (Wed Nov  6 18:54:53 2019) by ROOT version 6.14/04
   TCanvas *can2 = new TCanvas("can2", "can2",643,64,600,600);
   can2->SetHighLightColor(2);
   can2->Range(-7.5,4.505076e+07,7.5,4.511516e+07);
   can2->SetFillColor(0);
   can2->SetBorderMode(0);
   can2->SetBorderSize(2);
   can2->SetFrameBorderMode(0);
   can2->SetFrameBorderMode(0);
   
   TH1D *histo__1 = new TH1D("histo__1","histo",12,-6,6);
   histo__1->SetBinContent(1,4.508952e+07);
   histo__1->SetBinContent(2,4.51036e+07);
   histo__1->SetBinContent(3,4.510626e+07);
   histo__1->SetBinContent(4,4.510252e+07);
   histo__1->SetBinContent(5,4.509528e+07);
   histo__1->SetBinContent(6,4.505953e+07);
   histo__1->SetBinContent(7,4.506443e+07);
   histo__1->SetBinContent(8,4.507738e+07);
   histo__1->SetBinContent(9,4.508997e+07);
   histo__1->SetBinContent(10,4.509529e+07);
   histo__1->SetBinContent(11,4.510376e+07);
   histo__1->SetBinContent(12,4.509582e+07);
   histo__1->SetEntries(5.410834e+08);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   TText *ptstats_LaTex = ptstats->AddText("histo");
   ptstats_LaTex->SetTextSize(0.0368);
   ptstats_LaTex = ptstats->AddText("Entries =   5.410834e+08");
   ptstats_LaTex = ptstats->AddText("Mean  = -0.0001079");
   ptstats_LaTex = ptstats->AddText("Std Dev   =  3.464");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   histo__1->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(histo__1);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   histo__1->SetLineColor(ci);
   histo__1->SetMarkerStyle(20);
   histo__1->SetMarkerSize(0.7);
   histo__1->GetXaxis()->SetLabelFont(42);
   histo__1->GetXaxis()->SetLabelSize(0.035);
   histo__1->GetXaxis()->SetTitleSize(0.035);
   histo__1->GetXaxis()->SetTitleFont(42);
   histo__1->GetYaxis()->SetLabelFont(42);
   histo__1->GetYaxis()->SetLabelSize(0.035);
   histo__1->GetYaxis()->SetTitleSize(0.035);
   histo__1->GetYaxis()->SetTitleOffset(0);
   histo__1->GetYaxis()->SetTitleFont(42);
   histo__1->GetZaxis()->SetLabelFont(42);
   histo__1->GetZaxis()->SetLabelSize(0.035);
   histo__1->GetZaxis()->SetTitleSize(0.035);
   histo__1->GetZaxis()->SetTitleFont(42);
   histo__1->Draw("P");
   
   TPaveText *pt = new TPaveText(0.431723,0.94,0.568277,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   TText *pt_LaTex = pt->AddText("histo");
   pt->Draw();
   can2->Modified();
   can2->cd();
   can2->SetSelected(can2);
}
