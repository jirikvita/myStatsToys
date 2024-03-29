void ToF_1mm()
{
//=========Macro generated from canvas: ToF_1mm/ToF_1mm
//=========  (Tue Jan 23 13:31:07 2018) by ROOT version6.08/04
   TCanvas *ToF_1mm = new TCanvas("ToF_1mm", "ToF_1mm",0,50,1212,505);
   gStyle->SetOptTitle(0);
   ToF_1mm->SetHighLightColor(2);
   ToF_1mm->Range(0,0,1,1);
   ToF_1mm->SetFillColor(0);
   ToF_1mm->SetBorderMode(0);
   ToF_1mm->SetBorderSize(2);
   ToF_1mm->SetLeftMargin(0.15);
   ToF_1mm->SetBottomMargin(0.15);
   ToF_1mm->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: ToF_1mm_1
   TPad *ToF_1mm_1 = new TPad("ToF_1mm_1", "ToF_1mm_1",0.01,0.01,0.3233333,0.99);
   ToF_1mm_1->Draw();
   ToF_1mm_1->cd();
   ToF_1mm_1->Range(-600,-1.417196,3400,4.475508);
   ToF_1mm_1->SetFillColor(0);
   ToF_1mm_1->SetBorderMode(0);
   ToF_1mm_1->SetBorderSize(2);
   ToF_1mm_1->SetLogy();
   ToF_1mm_1->SetGridx();
   ToF_1mm_1->SetGridy();
   ToF_1mm_1->SetLeftMargin(0.15);
   ToF_1mm_1->SetBottomMargin(0.15);
   ToF_1mm_1->SetFrameBorderMode(0);
   ToF_1mm_1->SetFrameBorderMode(0);
   
   TH1D *Beta = new TH1D("Beta","Beta",100,0,3000);
   Beta->SetBinContent(1,601);
   Beta->SetBinContent(2,2333);
   Beta->SetBinContent(3,3254);
   Beta->SetBinContent(4,3432);
   Beta->SetBinContent(5,2985);
   Beta->SetBinContent(6,2702);
   Beta->SetBinContent(7,2296);
   Beta->SetBinContent(8,2026);
   Beta->SetBinContent(9,1813);
   Beta->SetBinContent(10,1478);
   Beta->SetBinContent(11,1139);
   Beta->SetBinContent(12,841);
   Beta->SetBinContent(13,632);
   Beta->SetBinContent(14,491);
   Beta->SetBinContent(15,362);
   Beta->SetBinContent(16,330);
   Beta->SetBinContent(17,305);
   Beta->SetBinContent(18,252);
   Beta->SetBinContent(19,198);
   Beta->SetBinContent(20,192);
   Beta->SetBinContent(21,166);
   Beta->SetBinContent(22,105);
   Beta->SetBinContent(23,131);
   Beta->SetBinContent(24,93);
   Beta->SetBinContent(25,84);
   Beta->SetBinContent(26,69);
   Beta->SetBinContent(27,84);
   Beta->SetBinContent(28,47);
   Beta->SetBinContent(29,58);
   Beta->SetBinContent(30,41);
   Beta->SetBinContent(31,41);
   Beta->SetBinContent(32,32);
   Beta->SetBinContent(33,27);
   Beta->SetBinContent(34,32);
   Beta->SetBinContent(35,27);
   Beta->SetBinContent(36,20);
   Beta->SetBinContent(37,17);
   Beta->SetBinContent(38,26);
   Beta->SetBinContent(39,14);
   Beta->SetBinContent(40,12);
   Beta->SetBinContent(41,9);
   Beta->SetBinContent(42,9);
   Beta->SetBinContent(43,8);
   Beta->SetBinContent(44,7);
   Beta->SetBinContent(45,5);
   Beta->SetBinContent(46,10);
   Beta->SetBinContent(47,9);
   Beta->SetBinContent(48,7);
   Beta->SetBinContent(49,2);
   Beta->SetBinContent(50,4);
   Beta->SetBinContent(51,4);
   Beta->SetBinContent(52,2);
   Beta->SetBinContent(53,4);
   Beta->SetBinContent(54,3);
   Beta->SetBinContent(55,5);
   Beta->SetBinContent(56,1);
   Beta->SetBinContent(57,1);
   Beta->SetBinContent(58,2);
   Beta->SetBinContent(59,3);
   Beta->SetBinContent(60,2);
   Beta->SetBinContent(61,4);
   Beta->SetBinContent(64,1);
   Beta->SetBinContent(65,5);
   Beta->SetBinContent(66,1);
   Beta->SetBinContent(67,2);
   Beta->SetBinContent(68,1);
   Beta->SetBinContent(69,2);
   Beta->SetBinContent(71,2);
   Beta->SetBinContent(75,1);
   Beta->SetBinContent(76,2);
   Beta->SetBinContent(78,1);
   Beta->SetBinContent(80,1);
   Beta->SetBinContent(81,2);
   Beta->SetBinContent(82,3);
   Beta->SetBinContent(83,2);
   Beta->SetBinContent(85,1);
   Beta->SetBinContent(88,1);
   Beta->SetBinContent(90,1);
   Beta->SetBinContent(91,1);
   Beta->SetBinContent(92,1);
   Beta->SetBinContent(94,1);
   Beta->SetBinContent(99,1);
   Beta->SetBinContent(101,46);
   Beta->SetBinError(1,177.3838);
   Beta->SetBinError(2,429.6196);
   Beta->SetBinError(3,599.1461);
   Beta->SetBinError(4,629.5205);
   Beta->SetBinError(5,547.2102);
   Beta->SetBinError(6,496.532);
   Beta->SetBinError(7,421.0938);
   Beta->SetBinError(8,372.996);
   Beta->SetBinError(9,334.785);
   Beta->SetBinError(10,273.1263);
   Beta->SetBinError(11,212.845);
   Beta->SetBinError(12,156.5024);
   Beta->SetBinError(13,118.6507);
   Beta->SetBinError(14,91.52595);
   Beta->SetBinError(15,69.10861);
   Beta->SetBinError(16,65.14599);
   Beta->SetBinError(17,58.69412);
   Beta->SetBinError(18,48.49742);
   Beta->SetBinError(19,38.91015);
   Beta->SetBinError(20,38.6523);
   Beta->SetBinError(21,32.06244);
   Beta->SetBinError(22,22.78157);
   Beta->SetBinError(23,26.96294);
   Beta->SetBinError(24,20.90454);
   Beta->SetBinError(25,17.02939);
   Beta->SetBinError(26,14.24781);
   Beta->SetBinError(27,17.77639);
   Beta->SetBinError(28,10.34408);
   Beta->SetBinError(29,13.56466);
   Beta->SetBinError(30,10.44031);
   Beta->SetBinError(31,10.90871);
   Beta->SetBinError(32,8.485281);
   Beta->SetBinError(33,7);
   Beta->SetBinError(34,8.717798);
   Beta->SetBinError(35,6.557439);
   Beta->SetBinError(36,5.830952);
   Beta->SetBinError(37,4.795832);
   Beta->SetBinError(38,6.78233);
   Beta->SetBinError(39,4.472136);
   Beta->SetBinError(40,3.741657);
   Beta->SetBinError(41,3.605551);
   Beta->SetBinError(42,3);
   Beta->SetBinError(43,2.828427);
   Beta->SetBinError(44,2.645751);
   Beta->SetBinError(45,2.236068);
   Beta->SetBinError(46,4.242641);
   Beta->SetBinError(47,3.316625);
   Beta->SetBinError(48,2.645751);
   Beta->SetBinError(49,1.414214);
   Beta->SetBinError(50,2);
   Beta->SetBinError(51,2);
   Beta->SetBinError(52,1.414214);
   Beta->SetBinError(53,2);
   Beta->SetBinError(54,2.236068);
   Beta->SetBinError(55,2.236068);
   Beta->SetBinError(56,1);
   Beta->SetBinError(57,1);
   Beta->SetBinError(58,1.414214);
   Beta->SetBinError(59,1.732051);
   Beta->SetBinError(60,1.414214);
   Beta->SetBinError(61,2);
   Beta->SetBinError(64,1);
   Beta->SetBinError(65,2.236068);
   Beta->SetBinError(66,1);
   Beta->SetBinError(67,1.414214);
   Beta->SetBinError(68,1);
   Beta->SetBinError(69,1.414214);
   Beta->SetBinError(71,1.414214);
   Beta->SetBinError(75,1);
   Beta->SetBinError(76,1.414214);
   Beta->SetBinError(78,1);
   Beta->SetBinError(80,1);
   Beta->SetBinError(81,1.414214);
   Beta->SetBinError(82,1.732051);
   Beta->SetBinError(83,2);
   Beta->SetBinError(85,1);
   Beta->SetBinError(88,1);
   Beta->SetBinError(90,1);
   Beta->SetBinError(91,1);
   Beta->SetBinError(92,1);
   Beta->SetBinError(94,1);
   Beta->SetBinError(99,1);
   Beta->SetBinError(101,6.78233);
   Beta->SetEntries(1190);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   TText *AText = ptstats->AddText("Beta");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 1190   ");
   AText = ptstats->AddText("Mean  =  219.4");
   AText = ptstats->AddText("Std Dev   =  196.3");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   Beta->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(Beta);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#cc6600");
   Beta->SetLineColor(ci);

   ci = TColor::GetColor("#cc6600");
   Beta->SetMarkerColor(ci);
   Beta->SetMarkerStyle(20);
   Beta->GetXaxis()->SetTitle("E [keV]");
   Beta->GetXaxis()->SetLabelFont(42);
   Beta->GetXaxis()->SetLabelSize(0.035);
   Beta->GetXaxis()->SetTitleSize(0.035);
   Beta->GetXaxis()->SetTitleFont(42);
   Beta->GetYaxis()->SetTitle("events");
   Beta->GetYaxis()->SetLabelFont(42);
   Beta->GetYaxis()->SetLabelSize(0.035);
   Beta->GetYaxis()->SetTitleSize(0.035);
   Beta->GetYaxis()->SetTitleFont(42);
   Beta->GetZaxis()->SetLabelFont(42);
   Beta->GetZaxis()->SetLabelSize(0.035);
   Beta->GetZaxis()->SetTitleSize(0.035);
   Beta->GetZaxis()->SetTitleFont(42);
   Beta->Draw("colz");
   ToF_1mm_1->Modified();
   ToF_1mm->cd();
  
// ------------>Primitives in pad: ToF_1mm_2
   TPad *ToF_1mm_2 = new TPad("ToF_1mm_2", "ToF_1mm_2",0.3433333,0.01,0.6566667,0.99);
   ToF_1mm_2->Draw();
   ToF_1mm_2->cd();
   ToF_1mm_2->Range(-60,-1.250058,340,4.297157);
   ToF_1mm_2->SetFillColor(0);
   ToF_1mm_2->SetBorderMode(0);
   ToF_1mm_2->SetBorderSize(2);
   ToF_1mm_2->SetLogy();
   ToF_1mm_2->SetGridx();
   ToF_1mm_2->SetGridy();
   ToF_1mm_2->SetLeftMargin(0.15);
   ToF_1mm_2->SetBottomMargin(0.15);
   ToF_1mm_2->SetFrameBorderMode(0);
   ToF_1mm_2->SetFrameBorderMode(0);
   
   TH1D *Gama = new TH1D("Gama","Gama",50,0,300);
   Gama->SetBinContent(1,1007);
   Gama->SetBinContent(2,2039);
   Gama->SetBinContent(3,1612);
   Gama->SetBinContent(4,1280);
   Gama->SetBinContent(5,900);
   Gama->SetBinContent(6,682);
   Gama->SetBinContent(7,578);
   Gama->SetBinContent(8,494);
   Gama->SetBinContent(9,467);
   Gama->SetBinContent(10,417);
   Gama->SetBinContent(11,392);
   Gama->SetBinContent(12,358);
   Gama->SetBinContent(13,356);
   Gama->SetBinContent(14,293);
   Gama->SetBinContent(15,262);
   Gama->SetBinContent(16,199);
   Gama->SetBinContent(17,172);
   Gama->SetBinContent(18,146);
   Gama->SetBinContent(19,133);
   Gama->SetBinContent(20,82);
   Gama->SetBinContent(21,85);
   Gama->SetBinContent(22,57);
   Gama->SetBinContent(23,56);
   Gama->SetBinContent(24,39);
   Gama->SetBinContent(25,42);
   Gama->SetBinContent(26,33);
   Gama->SetBinContent(27,21);
   Gama->SetBinContent(28,21);
   Gama->SetBinContent(29,24);
   Gama->SetBinContent(30,13);
   Gama->SetBinContent(31,6);
   Gama->SetBinContent(32,6);
   Gama->SetBinContent(33,4);
   Gama->SetBinContent(34,3);
   Gama->SetBinContent(35,5);
   Gama->SetBinContent(36,3);
   Gama->SetBinContent(37,4);
   Gama->SetBinContent(38,1);
   Gama->SetBinContent(39,1);
   Gama->SetBinContent(41,1);
   Gama->SetBinContent(42,1);
   Gama->SetBinContent(51,2);
   Gama->SetBinError(1,783.1251);
   Gama->SetBinError(2,877.6668);
   Gama->SetBinError(3,659.662);
   Gama->SetBinError(4,523.9771);
   Gama->SetBinError(5,381.8403);
   Gama->SetBinError(6,287.3952);
   Gama->SetBinError(7,240.6117);
   Gama->SetBinError(8,208.9067);
   Gama->SetBinError(9,194.4145);
   Gama->SetBinError(10,173.052);
   Gama->SetBinError(11,165.6502);
   Gama->SetBinError(12,151.1158);
   Gama->SetBinError(13,146.1711);
   Gama->SetBinError(14,120.7932);
   Gama->SetBinError(15,109.0504);
   Gama->SetBinError(16,81.87185);
   Gama->SetBinError(17,71.37226);
   Gama->SetBinError(18,60.46487);
   Gama->SetBinError(19,55.48874);
   Gama->SetBinError(20,34.46738);
   Gama->SetBinError(21,36.78315);
   Gama->SetBinError(22,23.47339);
   Gama->SetBinError(23,23.66432);
   Gama->SetBinError(24,18.62794);
   Gama->SetBinError(25,18.22087);
   Gama->SetBinError(26,14.10674);
   Gama->SetBinError(27,9.433981);
   Gama->SetBinError(28,10.34408);
   Gama->SetBinError(29,10.29563);
   Gama->SetBinError(30,6.082763);
   Gama->SetBinError(31,3.162278);
   Gama->SetBinError(32,5.09902);
   Gama->SetBinError(33,2.44949);
   Gama->SetBinError(34,2.236068);
   Gama->SetBinError(35,2.645751);
   Gama->SetBinError(36,2.236068);
   Gama->SetBinError(37,3.162278);
   Gama->SetBinError(38,1);
   Gama->SetBinError(39,1);
   Gama->SetBinError(41,1);
   Gama->SetBinError(42,1);
   Gama->SetBinError(51,1.414214);
   Gama->SetEntries(200);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Gama");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 200    ");
   AText = ptstats->AddText("Mean  =  37.89");
   AText = ptstats->AddText("Std Dev   =  35.01");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   Gama->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(Gama);

   ci = TColor::GetColor("#009900");
   Gama->SetLineColor(ci);

   ci = TColor::GetColor("#009900");
   Gama->SetMarkerColor(ci);
   Gama->SetMarkerStyle(22);
   Gama->GetXaxis()->SetTitle("E [keV]");
   Gama->GetXaxis()->SetLabelFont(42);
   Gama->GetXaxis()->SetLabelSize(0.035);
   Gama->GetXaxis()->SetTitleSize(0.035);
   Gama->GetXaxis()->SetTitleFont(42);
   Gama->GetYaxis()->SetTitle("events");
   Gama->GetYaxis()->SetLabelFont(42);
   Gama->GetYaxis()->SetLabelSize(0.035);
   Gama->GetYaxis()->SetTitleSize(0.035);
   Gama->GetYaxis()->SetTitleFont(42);
   Gama->GetZaxis()->SetLabelFont(42);
   Gama->GetZaxis()->SetLabelSize(0.035);
   Gama->GetZaxis()->SetTitleSize(0.035);
   Gama->GetZaxis()->SetTitleFont(42);
   Gama->Draw("colz");
   ToF_1mm_2->Modified();
   ToF_1mm->cd();
  
// ------------>Primitives in pad: ToF_1mm_3
   TPad *ToF_1mm_3 = new TPad("ToF_1mm_3", "ToF_1mm_3",0.6766667,0.01,0.99,0.99);
   ToF_1mm_3->Draw();
   ToF_1mm_3->cd();
   ToF_1mm_3->Range(-3000,-0.9576912,17000,1.871646);
   ToF_1mm_3->SetFillColor(0);
   ToF_1mm_3->SetBorderMode(0);
   ToF_1mm_3->SetBorderSize(2);
   ToF_1mm_3->SetLogy();
   ToF_1mm_3->SetGridx();
   ToF_1mm_3->SetGridy();
   ToF_1mm_3->SetLeftMargin(0.15);
   ToF_1mm_3->SetBottomMargin(0.15);
   ToF_1mm_3->SetFrameBorderMode(0);
   ToF_1mm_3->SetFrameBorderMode(0);
   
   TH1D *Alpha = new TH1D("Alpha","Alpha",100,0,15000);
   Alpha->SetBinContent(2,10);
   Alpha->SetBinContent(3,12);
   Alpha->SetBinContent(4,16);
   Alpha->SetBinContent(5,15);
   Alpha->SetBinContent(6,8);
   Alpha->SetBinContent(7,16);
   Alpha->SetBinContent(8,11);
   Alpha->SetBinContent(9,13);
   Alpha->SetBinContent(10,6);
   Alpha->SetBinContent(11,4);
   Alpha->SetBinContent(12,10);
   Alpha->SetBinContent(13,1);
   Alpha->SetBinContent(14,1);
   Alpha->SetBinContent(17,3);
   Alpha->SetBinContent(18,1);
   Alpha->SetBinContent(23,1);
   Alpha->SetBinContent(31,1);
   Alpha->SetBinContent(32,1);
   Alpha->SetBinContent(34,2);
   Alpha->SetBinContent(35,4);
   Alpha->SetBinContent(36,2);
   Alpha->SetBinContent(39,1);
   Alpha->SetBinContent(40,2);
   Alpha->SetBinContent(41,2);
   Alpha->SetBinContent(42,2);
   Alpha->SetBinContent(43,1);
   Alpha->SetBinContent(44,1);
   Alpha->SetBinContent(45,1);
   Alpha->SetBinContent(46,5);
   Alpha->SetBinContent(47,1);
   Alpha->SetBinContent(48,1);
   Alpha->SetBinContent(49,5);
   Alpha->SetBinContent(50,3);
   Alpha->SetBinContent(51,4);
   Alpha->SetBinContent(52,7);
   Alpha->SetBinContent(53,9);
   Alpha->SetBinContent(54,4);
   Alpha->SetBinContent(55,3);
   Alpha->SetBinContent(56,2);
   Alpha->SetBinContent(57,3);
   Alpha->SetBinContent(58,1);
   Alpha->SetBinContent(59,2);
   Alpha->SetBinContent(60,1);
   Alpha->SetBinContent(61,6);
   Alpha->SetBinContent(62,1);
   Alpha->SetBinContent(93,1);
   Alpha->SetBinError(2,3.162278);
   Alpha->SetBinError(3,3.464102);
   Alpha->SetBinError(4,4);
   Alpha->SetBinError(5,4.123106);
   Alpha->SetBinError(6,2.828427);
   Alpha->SetBinError(7,4.472136);
   Alpha->SetBinError(8,3.605551);
   Alpha->SetBinError(9,3.605551);
   Alpha->SetBinError(10,2.44949);
   Alpha->SetBinError(11,2.44949);
   Alpha->SetBinError(12,3.464102);
   Alpha->SetBinError(13,1);
   Alpha->SetBinError(14,1);
   Alpha->SetBinError(17,1.732051);
   Alpha->SetBinError(18,1);
   Alpha->SetBinError(23,1);
   Alpha->SetBinError(31,1);
   Alpha->SetBinError(32,1);
   Alpha->SetBinError(34,1.414214);
   Alpha->SetBinError(35,2);
   Alpha->SetBinError(36,1.414214);
   Alpha->SetBinError(39,1);
   Alpha->SetBinError(40,1.414214);
   Alpha->SetBinError(41,1.414214);
   Alpha->SetBinError(42,1.414214);
   Alpha->SetBinError(43,1);
   Alpha->SetBinError(44,1);
   Alpha->SetBinError(45,1);
   Alpha->SetBinError(46,2.236068);
   Alpha->SetBinError(47,1);
   Alpha->SetBinError(48,1);
   Alpha->SetBinError(49,2.236068);
   Alpha->SetBinError(50,1.732051);
   Alpha->SetBinError(51,2);
   Alpha->SetBinError(52,2.645751);
   Alpha->SetBinError(53,3);
   Alpha->SetBinError(54,2.44949);
   Alpha->SetBinError(55,1.732051);
   Alpha->SetBinError(56,1.414214);
   Alpha->SetBinError(57,1.732051);
   Alpha->SetBinError(58,1);
   Alpha->SetBinError(59,1.414214);
   Alpha->SetBinError(60,1);
   Alpha->SetBinError(61,2.44949);
   Alpha->SetBinError(62,1);
   Alpha->SetBinError(93,1);
   Alpha->SetEntries(200);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Alpha");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 200    ");
   AText = ptstats->AddText("Mean  =   3437");
   AText = ptstats->AddText("Std Dev   =   3274");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   Alpha->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(Alpha);

   ci = TColor::GetColor("#ff0000");
   Alpha->SetLineColor(ci);

   ci = TColor::GetColor("#ff0000");
   Alpha->SetMarkerColor(ci);
   Alpha->SetMarkerStyle(23);
   Alpha->GetXaxis()->SetTitle("E [keV]");
   Alpha->GetXaxis()->SetLabelFont(42);
   Alpha->GetXaxis()->SetLabelSize(0.035);
   Alpha->GetXaxis()->SetTitleSize(0.035);
   Alpha->GetXaxis()->SetTitleFont(42);
   Alpha->GetYaxis()->SetTitle("events");
   Alpha->GetYaxis()->SetLabelFont(42);
   Alpha->GetYaxis()->SetLabelSize(0.035);
   Alpha->GetYaxis()->SetTitleSize(0.035);
   Alpha->GetYaxis()->SetTitleFont(42);
   Alpha->GetZaxis()->SetLabelFont(42);
   Alpha->GetZaxis()->SetLabelSize(0.035);
   Alpha->GetZaxis()->SetTitleSize(0.035);
   Alpha->GetZaxis()->SetTitleFont(42);
   Alpha->Draw("colz");
   ToF_1mm_3->Modified();
   ToF_1mm->cd();
   ToF_1mm->Modified();
   ToF_1mm->cd();
   ToF_1mm->SetSelected(ToF_1mm);
}
