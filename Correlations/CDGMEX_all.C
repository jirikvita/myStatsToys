{
//=========Macro generated from canvas: CDGMEX_all/CDGMEX_all
//=========  (Fri Oct 27 14:29:40 2017) by ROOT version5.34/14
   TCanvas *CDGMEX_all = new TCanvas("CDGMEX_all", "CDGMEX_all",0,50,700,500);
   gStyle->SetOptTitle(0);
   CDGMEX_all->SetHighLightColor(2);
   CDGMEX_all->Range(0,0,1,1);
   CDGMEX_all->SetFillColor(0);
   CDGMEX_all->SetBorderMode(0);
   CDGMEX_all->SetBorderSize(2);
   CDGMEX_all->SetLeftMargin(0.15);
   CDGMEX_all->SetBottomMargin(0.15);
   CDGMEX_all->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: CDGMEX_all_1
   TPad *CDGMEX_all_1 = new TPad("CDGMEX_all_1", "CDGMEX_all_1",0.01,0.51,0.3233333,0.99);
   CDGMEX_all_1->Draw();
   CDGMEX_all_1->cd();
   CDGMEX_all_1->Range(-3000,0.4760452,17000,3.969077);
   CDGMEX_all_1->SetFillColor(0);
   CDGMEX_all_1->SetBorderMode(0);
   CDGMEX_all_1->SetBorderSize(2);
   CDGMEX_all_1->SetLogy();
   CDGMEX_all_1->SetGridx();
   CDGMEX_all_1->SetGridy();
   CDGMEX_all_1->SetLeftMargin(0.15);
   CDGMEX_all_1->SetBottomMargin(0.15);
   CDGMEX_all_1->SetFrameBorderMode(0);
   CDGMEX_all_1->SetFrameBorderMode(0);
   
   TH1D *Dots = new TH1D("Dots","Dots",100,0,15000);
   Dots->SetBinContent(1,2199);
   Dots->SetBinContent(2,20);
   Dots->SetBinContent(101,1230);
   Dots->SetEntries(386);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   TText *text = ptstats->AddText("Dots");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 386    ");
   text = ptstats->AddText("Mean  =  39.75");
   text = ptstats->AddText("RMS   =  33.71");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   Dots->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(Dots);
   Dots->SetMarkerStyle(20);
   Dots->GetXaxis()->SetTitle("E [keV]");
   Dots->GetXaxis()->SetLabelFont(42);
   Dots->GetXaxis()->SetLabelSize(0.035);
   Dots->GetXaxis()->SetTitleSize(0.035);
   Dots->GetXaxis()->SetTitleFont(42);
   Dots->GetYaxis()->SetTitle("events");
   Dots->GetYaxis()->SetLabelFont(42);
   Dots->GetYaxis()->SetLabelSize(0.035);
   Dots->GetYaxis()->SetTitleSize(0.035);
   Dots->GetYaxis()->SetTitleFont(42);
   Dots->GetZaxis()->SetLabelFont(42);
   Dots->GetZaxis()->SetLabelSize(0.035);
   Dots->GetZaxis()->SetTitleSize(0.035);
   Dots->GetZaxis()->SetTitleFont(42);
   Dots->Draw("colz");
   CDGMEX_all_1->Modified();
   CDGMEX_all->cd();
  
// ------------>Primitives in pad: CDGMEX_all_2
   CDGMEX_all_2 = new TPad("CDGMEX_all_2", "CDGMEX_all_2",0.3433333,0.51,0.6566667,0.99);
   CDGMEX_all_2->Draw();
   CDGMEX_all_2->cd();
   CDGMEX_all_2->Range(-300,-0.4769518,1700,0.6958601);
   CDGMEX_all_2->SetFillColor(0);
   CDGMEX_all_2->SetBorderMode(0);
   CDGMEX_all_2->SetBorderSize(2);
   CDGMEX_all_2->SetLogy();
   CDGMEX_all_2->SetGridx();
   CDGMEX_all_2->SetGridy();
   CDGMEX_all_2->SetLeftMargin(0.15);
   CDGMEX_all_2->SetBottomMargin(0.15);
   CDGMEX_all_2->SetFrameBorderMode(0);
   CDGMEX_all_2->SetFrameBorderMode(0);
   
   TH1D *HeavyBlobs = new TH1D("HeavyBlobs","HeavyBlobs",100,0,1500);
   HeavyBlobs->SetBinContent(36,1);
   HeavyBlobs->SetBinContent(80,1);
   HeavyBlobs->SetBinContent(84,1);
   HeavyBlobs->SetBinContent(86,1);
   HeavyBlobs->SetBinContent(88,1);
   HeavyBlobs->SetBinContent(92,2);
   HeavyBlobs->SetBinContent(93,1);
   HeavyBlobs->SetBinContent(101,46);
   HeavyBlobs->SetEntries(51);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   text = ptstats->AddText("HeavyBlobs");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 51     ");
   text = ptstats->AddText("Mean  =   1213");
   text = ptstats->AddText("RMS   =  266.6");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   HeavyBlobs->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(HeavyBlobs);
   HeavyBlobs->SetLineColor(2);
   HeavyBlobs->SetMarkerColor(2);
   HeavyBlobs->SetMarkerStyle(21);
   HeavyBlobs->GetXaxis()->SetTitle("E [keV]");
   HeavyBlobs->GetXaxis()->SetLabelFont(42);
   HeavyBlobs->GetXaxis()->SetLabelSize(0.035);
   HeavyBlobs->GetXaxis()->SetTitleSize(0.035);
   HeavyBlobs->GetXaxis()->SetTitleFont(42);
   HeavyBlobs->GetYaxis()->SetTitle("events");
   HeavyBlobs->GetYaxis()->SetLabelFont(42);
   HeavyBlobs->GetYaxis()->SetLabelSize(0.035);
   HeavyBlobs->GetYaxis()->SetTitleSize(0.035);
   HeavyBlobs->GetYaxis()->SetTitleFont(42);
   HeavyBlobs->GetZaxis()->SetLabelFont(42);
   HeavyBlobs->GetZaxis()->SetLabelSize(0.035);
   HeavyBlobs->GetZaxis()->SetTitleSize(0.035);
   HeavyBlobs->GetZaxis()->SetTitleFont(42);
   HeavyBlobs->Draw("colz");
   CDGMEX_all_2->Modified();
   CDGMEX_all->cd();
  
// ------------>Primitives in pad: CDGMEX_all_3
   CDGMEX_all_3 = new TPad("CDGMEX_all_3", "CDGMEX_all_3",0.6766667,0.51,0.99,0.99);
   CDGMEX_all_3->Draw();
   CDGMEX_all_3->cd();
   CDGMEX_all_3->Range(-300,-116.34,1700,659.26);
   CDGMEX_all_3->SetFillColor(0);
   CDGMEX_all_3->SetBorderMode(0);
   CDGMEX_all_3->SetBorderSize(2);
   CDGMEX_all_3->SetGridx();
   CDGMEX_all_3->SetGridy();
   CDGMEX_all_3->SetLeftMargin(0.15);
   CDGMEX_all_3->SetBottomMargin(0.15);
   CDGMEX_all_3->SetFrameBorderMode(0);
   CDGMEX_all_3->SetFrameBorderMode(0);
   
   TH1D *CurlyTracks = new TH1D("CurlyTracks","CurlyTracks",100,0,1500);
   CurlyTracks->SetBinContent(2,2);
   CurlyTracks->SetBinContent(3,10);
   CurlyTracks->SetBinContent(4,14);
   CurlyTracks->SetBinContent(5,108);
   CurlyTracks->SetBinContent(6,339);
   CurlyTracks->SetBinContent(7,554);
   CurlyTracks->SetBinContent(8,544);
   CurlyTracks->SetBinContent(9,520);
   CurlyTracks->SetBinContent(10,423);
   CurlyTracks->SetBinContent(11,308);
   CurlyTracks->SetBinContent(12,286);
   CurlyTracks->SetBinContent(13,267);
   CurlyTracks->SetBinContent(14,226);
   CurlyTracks->SetBinContent(15,199);
   CurlyTracks->SetBinContent(16,191);
   CurlyTracks->SetBinContent(17,167);
   CurlyTracks->SetBinContent(18,132);
   CurlyTracks->SetBinContent(19,122);
   CurlyTracks->SetBinContent(20,96);
   CurlyTracks->SetBinContent(21,105);
   CurlyTracks->SetBinContent(22,88);
   CurlyTracks->SetBinContent(23,66);
   CurlyTracks->SetBinContent(24,84);
   CurlyTracks->SetBinContent(25,56);
   CurlyTracks->SetBinContent(26,63);
   CurlyTracks->SetBinContent(27,29);
   CurlyTracks->SetBinContent(28,45);
   CurlyTracks->SetBinContent(29,23);
   CurlyTracks->SetBinContent(30,34);
   CurlyTracks->SetBinContent(31,25);
   CurlyTracks->SetBinContent(32,29);
   CurlyTracks->SetBinContent(33,30);
   CurlyTracks->SetBinContent(34,21);
   CurlyTracks->SetBinContent(35,19);
   CurlyTracks->SetBinContent(36,13);
   CurlyTracks->SetBinContent(37,26);
   CurlyTracks->SetBinContent(38,18);
   CurlyTracks->SetBinContent(39,14);
   CurlyTracks->SetBinContent(40,10);
   CurlyTracks->SetBinContent(41,11);
   CurlyTracks->SetBinContent(42,12);
   CurlyTracks->SetBinContent(43,12);
   CurlyTracks->SetBinContent(44,13);
   CurlyTracks->SetBinContent(45,13);
   CurlyTracks->SetBinContent(46,12);
   CurlyTracks->SetBinContent(47,12);
   CurlyTracks->SetBinContent(48,13);
   CurlyTracks->SetBinContent(49,12);
   CurlyTracks->SetBinContent(50,8);
   CurlyTracks->SetBinContent(51,7);
   CurlyTracks->SetBinContent(52,6);
   CurlyTracks->SetBinContent(53,11);
   CurlyTracks->SetBinContent(54,8);
   CurlyTracks->SetBinContent(55,6);
   CurlyTracks->SetBinContent(56,12);
   CurlyTracks->SetBinContent(57,5);
   CurlyTracks->SetBinContent(58,8);
   CurlyTracks->SetBinContent(59,6);
   CurlyTracks->SetBinContent(60,4);
   CurlyTracks->SetBinContent(61,7);
   CurlyTracks->SetBinContent(62,2);
   CurlyTracks->SetBinContent(63,5);
   CurlyTracks->SetBinContent(64,11);
   CurlyTracks->SetBinContent(65,3);
   CurlyTracks->SetBinContent(66,2);
   CurlyTracks->SetBinContent(67,3);
   CurlyTracks->SetBinContent(68,4);
   CurlyTracks->SetBinContent(69,1);
   CurlyTracks->SetBinContent(70,3);
   CurlyTracks->SetBinContent(71,4);
   CurlyTracks->SetBinContent(72,4);
   CurlyTracks->SetBinContent(73,3);
   CurlyTracks->SetBinContent(74,5);
   CurlyTracks->SetBinContent(75,6);
   CurlyTracks->SetBinContent(76,4);
   CurlyTracks->SetBinContent(77,8);
   CurlyTracks->SetBinContent(78,5);
   CurlyTracks->SetBinContent(79,6);
   CurlyTracks->SetBinContent(80,2);
   CurlyTracks->SetBinContent(81,2);
   CurlyTracks->SetBinContent(82,1);
   CurlyTracks->SetBinContent(83,3);
   CurlyTracks->SetBinContent(84,2);
   CurlyTracks->SetBinContent(85,1);
   CurlyTracks->SetBinContent(87,1);
   CurlyTracks->SetBinContent(88,4);
   CurlyTracks->SetBinContent(89,1);
   CurlyTracks->SetBinContent(90,1);
   CurlyTracks->SetBinContent(91,1);
   CurlyTracks->SetBinContent(92,2);
   CurlyTracks->SetBinContent(93,1);
   CurlyTracks->SetBinContent(94,2);
   CurlyTracks->SetBinContent(97,1);
   CurlyTracks->SetBinContent(100,1);
   CurlyTracks->SetBinContent(101,3026);
   CurlyTracks->SetEntries(1646);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   text = ptstats->AddText("CurlyTracks");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 1646   ");
   text = ptstats->AddText("Mean  =  227.5");
   text = ptstats->AddText("RMS   =  191.6");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   CurlyTracks->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(CurlyTracks);
   CurlyTracks->SetLineColor(3);
   CurlyTracks->SetMarkerColor(3);
   CurlyTracks->SetMarkerStyle(23);
   CurlyTracks->GetXaxis()->SetTitle("E [keV]");
   CurlyTracks->GetXaxis()->SetLabelFont(42);
   CurlyTracks->GetXaxis()->SetLabelSize(0.035);
   CurlyTracks->GetXaxis()->SetTitleSize(0.035);
   CurlyTracks->GetXaxis()->SetTitleFont(42);
   CurlyTracks->GetYaxis()->SetTitle("events");
   CurlyTracks->GetYaxis()->SetLabelFont(42);
   CurlyTracks->GetYaxis()->SetLabelSize(0.035);
   CurlyTracks->GetYaxis()->SetTitleSize(0.035);
   CurlyTracks->GetYaxis()->SetTitleFont(42);
   CurlyTracks->GetZaxis()->SetLabelFont(42);
   CurlyTracks->GetZaxis()->SetLabelSize(0.035);
   CurlyTracks->GetZaxis()->SetTitleSize(0.035);
   CurlyTracks->GetZaxis()->SetTitleFont(42);
   CurlyTracks->Draw("colz");
   CDGMEX_all_3->Modified();
   CDGMEX_all->cd();
  
// ------------>Primitives in pad: CDGMEX_all_4
   CDGMEX_all_4 = new TPad("CDGMEX_all_4", "CDGMEX_all_4",0.01,0.01,0.3233333,0.49);
   CDGMEX_all_4->Draw();
   CDGMEX_all_4->cd();
   CDGMEX_all_4->Range(-3000,-0.7061774,17000,1.994805);
   CDGMEX_all_4->SetFillColor(0);
   CDGMEX_all_4->SetBorderMode(0);
   CDGMEX_all_4->SetBorderSize(2);
   CDGMEX_all_4->SetLogy();
   CDGMEX_all_4->SetGridx();
   CDGMEX_all_4->SetGridy();
   CDGMEX_all_4->SetLeftMargin(0.15);
   CDGMEX_all_4->SetBottomMargin(0.15);
   CDGMEX_all_4->SetFrameBorderMode(0);
   CDGMEX_all_4->SetFrameBorderMode(0);
   
   TH1D *StraightTracks = new TH1D("StraightTracks","StraightTracks",1000,0,15000);
   StraightTracks->SetBinContent(15,2);
   StraightTracks->SetBinContent(16,1);
   StraightTracks->SetBinContent(17,5);
   StraightTracks->SetBinContent(18,6);
   StraightTracks->SetBinContent(19,8);
   StraightTracks->SetBinContent(20,12);
   StraightTracks->SetBinContent(21,17);
   StraightTracks->SetBinContent(22,17);
   StraightTracks->SetBinContent(23,17);
   StraightTracks->SetBinContent(24,28);
   StraightTracks->SetBinContent(25,26);
   StraightTracks->SetBinContent(26,13);
   StraightTracks->SetBinContent(27,15);
   StraightTracks->SetBinContent(28,21);
   StraightTracks->SetBinContent(29,11);
   StraightTracks->SetBinContent(30,13);
   StraightTracks->SetBinContent(31,11);
   StraightTracks->SetBinContent(32,12);
   StraightTracks->SetBinContent(33,11);
   StraightTracks->SetBinContent(34,10);
   StraightTracks->SetBinContent(35,6);
   StraightTracks->SetBinContent(36,1);
   StraightTracks->SetBinContent(37,13);
   StraightTracks->SetBinContent(38,5);
   StraightTracks->SetBinContent(39,4);
   StraightTracks->SetBinContent(40,7);
   StraightTracks->SetBinContent(41,4);
   StraightTracks->SetBinContent(42,5);
   StraightTracks->SetBinContent(43,5);
   StraightTracks->SetBinContent(45,1);
   StraightTracks->SetBinContent(46,4);
   StraightTracks->SetBinContent(47,7);
   StraightTracks->SetBinContent(48,5);
   StraightTracks->SetBinContent(49,2);
   StraightTracks->SetBinContent(50,3);
   StraightTracks->SetBinContent(51,4);
   StraightTracks->SetBinContent(52,8);
   StraightTracks->SetBinContent(53,3);
   StraightTracks->SetBinContent(54,5);
   StraightTracks->SetBinContent(55,4);
   StraightTracks->SetBinContent(56,4);
   StraightTracks->SetBinContent(57,2);
   StraightTracks->SetBinContent(58,2);
   StraightTracks->SetBinContent(59,2);
   StraightTracks->SetBinContent(60,4);
   StraightTracks->SetBinContent(61,3);
   StraightTracks->SetBinContent(63,1);
   StraightTracks->SetBinContent(64,2);
   StraightTracks->SetBinContent(65,1);
   StraightTracks->SetBinContent(66,1);
   StraightTracks->SetBinContent(67,2);
   StraightTracks->SetBinContent(68,1);
   StraightTracks->SetBinContent(70,2);
   StraightTracks->SetBinContent(71,1);
   StraightTracks->SetBinContent(72,2);
   StraightTracks->SetBinContent(73,1);
   StraightTracks->SetBinContent(74,2);
   StraightTracks->SetBinContent(76,1);
   StraightTracks->SetBinContent(77,1);
   StraightTracks->SetBinContent(81,1);
   StraightTracks->SetBinContent(83,2);
   StraightTracks->SetBinContent(84,1);
   StraightTracks->SetBinContent(90,1);
   StraightTracks->SetBinContent(92,1);
   StraightTracks->SetBinContent(96,1);
   StraightTracks->SetBinContent(110,1);
   StraightTracks->SetBinContent(111,1);
   StraightTracks->SetBinContent(112,1);
   StraightTracks->SetBinContent(115,1);
   StraightTracks->SetBinContent(126,1);
   StraightTracks->SetBinContent(132,1);
   StraightTracks->SetBinContent(135,1);
   StraightTracks->SetBinContent(148,1);
   StraightTracks->SetBinContent(193,1);
   StraightTracks->SetBinContent(223,1);
   StraightTracks->SetBinContent(618,1);
   StraightTracks->SetBinContent(1001,190);
   StraightTracks->SetEntries(479);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   text = ptstats->AddText("StraightTracks");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 479    ");
   text = ptstats->AddText("Mean  =  572.7");
   text = ptstats->AddText("RMS   =  552.8");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   StraightTracks->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(StraightTracks);
   StraightTracks->SetLineColor(2);
   StraightTracks->SetMarkerColor(2);
   StraightTracks->SetMarkerStyle(25);
   StraightTracks->GetXaxis()->SetTitle("E [keV]");
   StraightTracks->GetXaxis()->SetLabelFont(42);
   StraightTracks->GetXaxis()->SetLabelSize(0.035);
   StraightTracks->GetXaxis()->SetTitleSize(0.035);
   StraightTracks->GetXaxis()->SetTitleFont(42);
   StraightTracks->GetYaxis()->SetTitle("events");
   StraightTracks->GetYaxis()->SetLabelFont(42);
   StraightTracks->GetYaxis()->SetLabelSize(0.035);
   StraightTracks->GetYaxis()->SetTitleSize(0.035);
   StraightTracks->GetYaxis()->SetTitleFont(42);
   StraightTracks->GetZaxis()->SetLabelFont(42);
   StraightTracks->GetZaxis()->SetLabelSize(0.035);
   StraightTracks->GetZaxis()->SetTitleSize(0.035);
   StraightTracks->GetZaxis()->SetTitleFont(42);
   StraightTracks->Draw("colz");
   CDGMEX_all_4->Modified();
   CDGMEX_all->cd();
  
// ------------>Primitives in pad: CDGMEX_all_5
   CDGMEX_all_5 = new TPad("CDGMEX_all_5", "CDGMEX_all_5",0.3433333,0.01,0.6566667,0.49);
   CDGMEX_all_5->Draw();
   CDGMEX_all_5->cd();
   CDGMEX_all_5->Range(-3000,-0.632582,17000,1.577765);
   CDGMEX_all_5->SetFillColor(0);
   CDGMEX_all_5->SetBorderMode(0);
   CDGMEX_all_5->SetBorderSize(2);
   CDGMEX_all_5->SetLogy();
   CDGMEX_all_5->SetGridx();
   CDGMEX_all_5->SetGridy();
   CDGMEX_all_5->SetLeftMargin(0.15);
   CDGMEX_all_5->SetBottomMargin(0.15);
   CDGMEX_all_5->SetFrameBorderMode(0);
   CDGMEX_all_5->SetFrameBorderMode(0);
   
   TH1D *HeavyTracks = new TH1D("HeavyTracks","HeavyTracks",100,0,15000);
   HeavyTracks->SetBinContent(4,1);
   HeavyTracks->SetBinContent(6,3);
   HeavyTracks->SetBinContent(7,3);
   HeavyTracks->SetBinContent(8,3);
   HeavyTracks->SetBinContent(9,12);
   HeavyTracks->SetBinContent(10,7);
   HeavyTracks->SetBinContent(11,2);
   HeavyTracks->SetBinContent(12,12);
   HeavyTracks->SetBinContent(13,1);
   HeavyTracks->SetBinContent(14,8);
   HeavyTracks->SetBinContent(15,4);
   HeavyTracks->SetBinContent(16,8);
   HeavyTracks->SetBinContent(17,3);
   HeavyTracks->SetBinContent(18,2);
   HeavyTracks->SetBinContent(19,5);
   HeavyTracks->SetBinContent(20,1);
   HeavyTracks->SetBinContent(21,1);
   HeavyTracks->SetBinContent(22,4);
   HeavyTracks->SetBinContent(23,1);
   HeavyTracks->SetBinContent(24,2);
   HeavyTracks->SetBinContent(25,1);
   HeavyTracks->SetBinContent(26,1);
   HeavyTracks->SetBinContent(27,1);
   HeavyTracks->SetBinContent(28,2);
   HeavyTracks->SetBinContent(29,1);
   HeavyTracks->SetBinContent(30,1);
   HeavyTracks->SetBinContent(31,1);
   HeavyTracks->SetBinContent(33,1);
   HeavyTracks->SetBinContent(34,2);
   HeavyTracks->SetBinContent(40,1);
   HeavyTracks->SetBinContent(41,1);
   HeavyTracks->SetBinContent(43,1);
   HeavyTracks->SetBinContent(46,2);
   HeavyTracks->SetBinContent(47,1);
   HeavyTracks->SetBinContent(50,1);
   HeavyTracks->SetBinContent(59,1);
   HeavyTracks->SetBinContent(70,1);
   HeavyTracks->SetBinContent(77,1);
   HeavyTracks->SetBinContent(80,1);
   HeavyTracks->SetBinContent(81,1);
   HeavyTracks->SetBinContent(100,1);
   HeavyTracks->SetBinContent(101,46);
   HeavyTracks->SetEntries(151);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   text = ptstats->AddText("HeavyTracks");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 151    ");
   text = ptstats->AddText("Mean  =   3026");
   text = ptstats->AddText("RMS   =   2595");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   HeavyTracks->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(HeavyTracks);
   HeavyTracks->SetLineColor(3);
   HeavyTracks->SetMarkerColor(3);
   HeavyTracks->SetMarkerStyle(26);
   HeavyTracks->GetXaxis()->SetTitle("E [keV]");
   HeavyTracks->GetXaxis()->SetLabelFont(42);
   HeavyTracks->GetXaxis()->SetLabelSize(0.035);
   HeavyTracks->GetXaxis()->SetTitleSize(0.035);
   HeavyTracks->GetXaxis()->SetTitleFont(42);
   HeavyTracks->GetYaxis()->SetTitle("events");
   HeavyTracks->GetYaxis()->SetLabelFont(42);
   HeavyTracks->GetYaxis()->SetLabelSize(0.035);
   HeavyTracks->GetYaxis()->SetTitleSize(0.035);
   HeavyTracks->GetYaxis()->SetTitleFont(42);
   HeavyTracks->GetZaxis()->SetLabelFont(42);
   HeavyTracks->GetZaxis()->SetLabelSize(0.035);
   HeavyTracks->GetZaxis()->SetTitleSize(0.035);
   HeavyTracks->GetZaxis()->SetTitleFont(42);
   HeavyTracks->Draw("colz");
   CDGMEX_all_5->Modified();
   CDGMEX_all->cd();
  
// ------------>Primitives in pad: CDGMEX_all_6
   CDGMEX_all_6 = new TPad("CDGMEX_all_6", "CDGMEX_all_6",0.6766667,0.01,0.99,0.49);
   CDGMEX_all_6->Draw();
   CDGMEX_all_6->cd();
   CDGMEX_all_6->Range(-3000,-1.095215,17000,4.199351);
   CDGMEX_all_6->SetFillColor(0);
   CDGMEX_all_6->SetBorderMode(0);
   CDGMEX_all_6->SetBorderSize(2);
   CDGMEX_all_6->SetLogy();
   CDGMEX_all_6->SetGridx();
   CDGMEX_all_6->SetGridy();
   CDGMEX_all_6->SetLeftMargin(0.15);
   CDGMEX_all_6->SetBottomMargin(0.15);
   CDGMEX_all_6->SetFrameBorderMode(0);
   CDGMEX_all_6->SetFrameBorderMode(0);
   
   TH1D *SmallBlobs = new TH1D("SmallBlobs","SmallBlobs",100,0,15000);
   SmallBlobs->SetBinContent(1,2468);
   SmallBlobs->SetBinContent(2,349);
   SmallBlobs->SetBinContent(3,29);
   SmallBlobs->SetBinContent(4,3);
   SmallBlobs->SetBinContent(5,2);
   SmallBlobs->SetBinContent(6,3);
   SmallBlobs->SetBinContent(19,1);
   SmallBlobs->SetBinContent(22,1);
   SmallBlobs->SetBinContent(31,1);
   SmallBlobs->SetBinContent(32,1);
   SmallBlobs->SetBinContent(37,1);
   SmallBlobs->SetBinContent(101,1725);
   SmallBlobs->SetEntries(706);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   text = ptstats->AddText("SmallBlobs");
   text->SetTextSize(0.0368);
   text = ptstats->AddText("Entries = 706    ");
   text = ptstats->AddText("Mean  =  108.8");
   text = ptstats->AddText("RMS   =  183.6");
   ptstats->SetOptStat(1111);
   ptstats->SetOptFit(0);
   ptstats->Draw();
   SmallBlobs->GetListOfFunctions()->Add(ptstats);
   ptstats->SetParent(SmallBlobs);
   SmallBlobs->SetLineColor(4);
   SmallBlobs->SetMarkerColor(4);
   SmallBlobs->SetMarkerStyle(27);
   SmallBlobs->GetXaxis()->SetTitle("E [keV]");
   SmallBlobs->GetXaxis()->SetLabelFont(42);
   SmallBlobs->GetXaxis()->SetLabelSize(0.035);
   SmallBlobs->GetXaxis()->SetTitleSize(0.035);
   SmallBlobs->GetXaxis()->SetTitleFont(42);
   SmallBlobs->GetYaxis()->SetTitle("events");
   SmallBlobs->GetYaxis()->SetLabelFont(42);
   SmallBlobs->GetYaxis()->SetLabelSize(0.035);
   SmallBlobs->GetYaxis()->SetTitleSize(0.035);
   SmallBlobs->GetYaxis()->SetTitleFont(42);
   SmallBlobs->GetZaxis()->SetLabelFont(42);
   SmallBlobs->GetZaxis()->SetLabelSize(0.035);
   SmallBlobs->GetZaxis()->SetTitleSize(0.035);
   SmallBlobs->GetZaxis()->SetTitleFont(42);
   SmallBlobs->Draw("colz");
   CDGMEX_all_6->Modified();
   CDGMEX_all->cd();
   CDGMEX_all->Modified();
   CDGMEX_all->cd();
   CDGMEX_all->SetSelected(CDGMEX_all);
}
