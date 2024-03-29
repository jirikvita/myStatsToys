void ToF_10mm()
{
//=========Macro generated from canvas: ToF_10mm/ToF_10mm
//=========  (Tue Jan 23 13:30:59 2018) by ROOT version6.08/04
   TCanvas *ToF_10mm = new TCanvas("ToF_10mm", "ToF_10mm",0,50,1212,505);
   gStyle->SetOptTitle(0);
   ToF_10mm->SetHighLightColor(2);
   ToF_10mm->Range(0,0,1,1);
   ToF_10mm->SetFillColor(0);
   ToF_10mm->SetBorderMode(0);
   ToF_10mm->SetBorderSize(2);
   ToF_10mm->SetLeftMargin(0.15);
   ToF_10mm->SetBottomMargin(0.15);
   ToF_10mm->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: ToF_10mm_1
   TPad *ToF_10mm_1 = new TPad("ToF_10mm_1", "ToF_10mm_1",0.01,0.01,0.3233333,0.99);
   ToF_10mm_1->Draw();
   ToF_10mm_1->cd();
   ToF_10mm_1->Range(-600,-1.452695,3400,4.676669);
   ToF_10mm_1->SetFillColor(0);
   ToF_10mm_1->SetBorderMode(0);
   ToF_10mm_1->SetBorderSize(2);
   ToF_10mm_1->SetLogy();
   ToF_10mm_1->SetGridx();
   ToF_10mm_1->SetGridy();
   ToF_10mm_1->SetLeftMargin(0.15);
   ToF_10mm_1->SetBottomMargin(0.15);
   ToF_10mm_1->SetFrameBorderMode(0);
   ToF_10mm_1->SetFrameBorderMode(0);
   
   TH1D *Beta = new TH1D("Beta","Beta",100,0,3000);
   Beta->SetBinContent(1,1228);
   Beta->SetBinContent(2,4192);
   Beta->SetBinContent(3,5014);
   Beta->SetBinContent(4,5166);
   Beta->SetBinContent(5,4882);
   Beta->SetBinContent(6,4359);
   Beta->SetBinContent(7,3942);
   Beta->SetBinContent(8,3489);
   Beta->SetBinContent(9,3058);
   Beta->SetBinContent(10,2519);
   Beta->SetBinContent(11,2064);
   Beta->SetBinContent(12,1588);
   Beta->SetBinContent(13,1299);
   Beta->SetBinContent(14,1189);
   Beta->SetBinContent(15,940);
   Beta->SetBinContent(16,868);
   Beta->SetBinContent(17,779);
   Beta->SetBinContent(18,729);
   Beta->SetBinContent(19,621);
   Beta->SetBinContent(20,563);
   Beta->SetBinContent(21,554);
   Beta->SetBinContent(22,459);
   Beta->SetBinContent(23,388);
   Beta->SetBinContent(24,362);
   Beta->SetBinContent(25,316);
   Beta->SetBinContent(26,301);
   Beta->SetBinContent(27,274);
   Beta->SetBinContent(28,254);
   Beta->SetBinContent(29,241);
   Beta->SetBinContent(30,209);
   Beta->SetBinContent(31,193);
   Beta->SetBinContent(32,198);
   Beta->SetBinContent(33,160);
   Beta->SetBinContent(34,158);
   Beta->SetBinContent(35,119);
   Beta->SetBinContent(36,135);
   Beta->SetBinContent(37,103);
   Beta->SetBinContent(38,117);
   Beta->SetBinContent(39,110);
   Beta->SetBinContent(40,101);
   Beta->SetBinContent(41,84);
   Beta->SetBinContent(42,94);
   Beta->SetBinContent(43,76);
   Beta->SetBinContent(44,73);
   Beta->SetBinContent(45,60);
   Beta->SetBinContent(46,48);
   Beta->SetBinContent(47,41);
   Beta->SetBinContent(48,56);
   Beta->SetBinContent(49,46);
   Beta->SetBinContent(50,46);
   Beta->SetBinContent(51,44);
   Beta->SetBinContent(52,39);
   Beta->SetBinContent(53,27);
   Beta->SetBinContent(54,27);
   Beta->SetBinContent(55,22);
   Beta->SetBinContent(56,31);
   Beta->SetBinContent(57,24);
   Beta->SetBinContent(58,18);
   Beta->SetBinContent(59,23);
   Beta->SetBinContent(60,30);
   Beta->SetBinContent(61,27);
   Beta->SetBinContent(62,33);
   Beta->SetBinContent(63,22);
   Beta->SetBinContent(64,24);
   Beta->SetBinContent(65,22);
   Beta->SetBinContent(66,15);
   Beta->SetBinContent(67,25);
   Beta->SetBinContent(68,18);
   Beta->SetBinContent(69,15);
   Beta->SetBinContent(70,10);
   Beta->SetBinContent(71,12);
   Beta->SetBinContent(72,13);
   Beta->SetBinContent(73,16);
   Beta->SetBinContent(74,18);
   Beta->SetBinContent(75,16);
   Beta->SetBinContent(76,13);
   Beta->SetBinContent(77,10);
   Beta->SetBinContent(78,14);
   Beta->SetBinContent(79,11);
   Beta->SetBinContent(80,7);
   Beta->SetBinContent(81,5);
   Beta->SetBinContent(82,4);
   Beta->SetBinContent(83,6);
   Beta->SetBinContent(84,11);
   Beta->SetBinContent(85,14);
   Beta->SetBinContent(86,5);
   Beta->SetBinContent(87,9);
   Beta->SetBinContent(88,5);
   Beta->SetBinContent(89,14);
   Beta->SetBinContent(90,9);
   Beta->SetBinContent(91,8);
   Beta->SetBinContent(92,2);
   Beta->SetBinContent(93,5);
   Beta->SetBinContent(94,5);
   Beta->SetBinContent(95,4);
   Beta->SetBinContent(96,4);
   Beta->SetBinContent(97,6);
   Beta->SetBinContent(98,9);
   Beta->SetBinContent(99,5);
   Beta->SetBinContent(100,6);
   Beta->SetBinContent(101,309);
   Beta->SetBinError(1,351.8636);
   Beta->SetBinError(2,769.6155);
   Beta->SetBinError(3,919.6793);
   Beta->SetBinError(4,945.9989);
   Beta->SetBinError(5,893.398);
   Beta->SetBinError(6,798.6182);
   Beta->SetBinError(7,722.1205);
   Beta->SetBinError(8,640.8065);
   Beta->SetBinError(9,560.7941);
   Beta->SetBinError(10,462.2889);
   Beta->SetBinError(11,379.5208);
   Beta->SetBinError(12,293.4212);
   Beta->SetBinError(13,239.4723);
   Beta->SetBinError(14,219.6156);
   Beta->SetBinError(15,174.4534);
   Beta->SetBinError(16,161.9691);
   Beta->SetBinError(17,144.8482);
   Beta->SetBinError(18,137.5536);
   Beta->SetBinError(19,115.6244);
   Beta->SetBinError(20,106.325);
   Beta->SetBinError(21,103.131);
   Beta->SetBinError(22,87.68694);
   Beta->SetBinError(23,72.38784);
   Beta->SetBinError(24,68.57113);
   Beta->SetBinError(25,61.56298);
   Beta->SetBinError(26,57.76677);
   Beta->SetBinError(27,52.68776);
   Beta->SetBinError(28,49.13247);
   Beta->SetBinError(29,45.46427);
   Beta->SetBinError(30,40.0874);
   Beta->SetBinError(31,38.61347);
   Beta->SetBinError(32,38.98718);
   Beta->SetBinError(33,32);
   Beta->SetBinError(34,30.3315);
   Beta->SetBinError(35,24.06242);
   Beta->SetBinError(36,26.05763);
   Beta->SetBinError(37,22.2486);
   Beta->SetBinError(38,24.14539);
   Beta->SetBinError(39,21.77154);
   Beta->SetBinError(40,20.27313);
   Beta->SetBinError(41,16.79286);
   Beta->SetBinError(42,19.89975);
   Beta->SetBinError(43,16.79286);
   Beta->SetBinError(44,15.19868);
   Beta->SetBinError(45,13.63818);
   Beta->SetBinError(46,11.13553);
   Beta->SetBinError(47,10.90871);
   Beta->SetBinError(48,11.6619);
   Beta->SetBinError(49,10.48809);
   Beta->SetBinError(50,11.13553);
   Beta->SetBinError(51,10.77033);
   Beta->SetBinError(52,10.44031);
   Beta->SetBinError(53,7.549834);
   Beta->SetBinError(54,7.141428);
   Beta->SetBinError(55,5.830952);
   Beta->SetBinError(56,7.416198);
   Beta->SetBinError(57,6);
   Beta->SetBinError(58,5.477226);
   Beta->SetBinError(59,5.744563);
   Beta->SetBinError(60,8.831761);
   Beta->SetBinError(61,7.416198);
   Beta->SetBinError(62,8.774964);
   Beta->SetBinError(63,5.830952);
   Beta->SetBinError(64,6.928203);
   Beta->SetBinError(65,6.480741);
   Beta->SetBinError(66,5);
   Beta->SetBinError(67,6.403124);
   Beta->SetBinError(68,5.477226);
   Beta->SetBinError(69,4.582576);
   Beta->SetBinError(70,3.162278);
   Beta->SetBinError(71,3.741657);
   Beta->SetBinError(72,4.358899);
   Beta->SetBinError(73,4.472136);
   Beta->SetBinError(74,4.690416);
   Beta->SetBinError(75,4.690416);
   Beta->SetBinError(76,3.872983);
   Beta->SetBinError(77,3.464102);
   Beta->SetBinError(78,4.242641);
   Beta->SetBinError(79,3.605551);
   Beta->SetBinError(80,2.645751);
   Beta->SetBinError(81,2.236068);
   Beta->SetBinError(82,2);
   Beta->SetBinError(83,2.828427);
   Beta->SetBinError(84,3.872983);
   Beta->SetBinError(85,4);
   Beta->SetBinError(86,2.236068);
   Beta->SetBinError(87,3.605551);
   Beta->SetBinError(88,2.236068);
   Beta->SetBinError(89,4.690416);
   Beta->SetBinError(90,3.605551);
   Beta->SetBinError(91,3.162278);
   Beta->SetBinError(92,1.414214);
   Beta->SetBinError(93,2.645751);
   Beta->SetBinError(94,2.645751);
   Beta->SetBinError(95,2.44949);
   Beta->SetBinError(96,2);
   Beta->SetBinError(97,2.44949);
   Beta->SetBinError(98,3);
   Beta->SetBinError(99,2.236068);
   Beta->SetBinError(100,2.828427);
   Beta->SetBinError(101,18.57418);
   Beta->SetEntries(2285);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   TText *AText = ptstats->AddText("Beta");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 2285   ");
   AText = ptstats->AddText("Mean  =  296.2");
   AText = ptstats->AddText("Std Dev   =  323.1");
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
   ToF_10mm_1->Modified();
   ToF_10mm->cd();
  
// ------------>Primitives in pad: ToF_10mm_2
   TPad *ToF_10mm_2 = new TPad("ToF_10mm_2", "ToF_10mm_2",0.3433333,0.01,0.6566667,0.99);
   ToF_10mm_2->Draw();
   ToF_10mm_2->cd();
   ToF_10mm_2->Range(-60,-1.431295,340,4.5554);
   ToF_10mm_2->SetFillColor(0);
   ToF_10mm_2->SetBorderMode(0);
   ToF_10mm_2->SetBorderSize(2);
   ToF_10mm_2->SetLogy();
   ToF_10mm_2->SetGridx();
   ToF_10mm_2->SetGridy();
   ToF_10mm_2->SetLeftMargin(0.15);
   ToF_10mm_2->SetBottomMargin(0.15);
   ToF_10mm_2->SetFrameBorderMode(0);
   ToF_10mm_2->SetFrameBorderMode(0);
   
   TH1D *Gama = new TH1D("Gama","Gama",50,0,300);
   Gama->SetBinContent(1,1820);
   Gama->SetBinContent(2,3332);
   Gama->SetBinContent(3,2537);
   Gama->SetBinContent(4,1812);
   Gama->SetBinContent(5,1146);
   Gama->SetBinContent(6,932);
   Gama->SetBinContent(7,767);
   Gama->SetBinContent(8,616);
   Gama->SetBinContent(9,589);
   Gama->SetBinContent(10,584);
   Gama->SetBinContent(11,499);
   Gama->SetBinContent(12,480);
   Gama->SetBinContent(13,396);
   Gama->SetBinContent(14,346);
   Gama->SetBinContent(15,298);
   Gama->SetBinContent(16,268);
   Gama->SetBinContent(17,235);
   Gama->SetBinContent(18,195);
   Gama->SetBinContent(19,156);
   Gama->SetBinContent(20,110);
   Gama->SetBinContent(21,92);
   Gama->SetBinContent(22,107);
   Gama->SetBinContent(23,84);
   Gama->SetBinContent(24,65);
   Gama->SetBinContent(25,38);
   Gama->SetBinContent(26,39);
   Gama->SetBinContent(27,27);
   Gama->SetBinContent(28,28);
   Gama->SetBinContent(29,24);
   Gama->SetBinContent(30,20);
   Gama->SetBinContent(31,14);
   Gama->SetBinContent(32,7);
   Gama->SetBinContent(33,5);
   Gama->SetBinContent(34,8);
   Gama->SetBinContent(35,5);
   Gama->SetBinContent(36,3);
   Gama->SetBinContent(37,6);
   Gama->SetBinContent(38,2);
   Gama->SetBinContent(39,1);
   Gama->SetBinContent(40,1);
   Gama->SetBinContent(41,1);
   Gama->SetBinContent(43,2);
   Gama->SetBinContent(44,1);
   Gama->SetBinContent(47,2);
   Gama->SetBinContent(51,3);
   Gama->SetBinError(1,1379.348);
   Gama->SetBinError(2,1445.293);
   Gama->SetBinError(3,1040.828);
   Gama->SetBinError(4,744.1505);
   Gama->SetBinError(5,483.0487);
   Gama->SetBinError(6,399.3319);
   Gama->SetBinError(7,318.7272);
   Gama->SetBinError(8,260.4381);
   Gama->SetBinError(9,248.0343);
   Gama->SetBinError(10,242.2437);
   Gama->SetBinError(11,209.5066);
   Gama->SetBinError(12,200.3098);
   Gama->SetBinError(13,164.6572);
   Gama->SetBinError(14,143.3667);
   Gama->SetBinError(15,123.8467);
   Gama->SetBinError(16,109.8727);
   Gama->SetBinError(17,96.19252);
   Gama->SetBinError(18,81.9939);
   Gama->SetBinError(19,65.98485);
   Gama->SetBinError(20,46.32494);
   Gama->SetBinError(21,37.86819);
   Gama->SetBinError(22,45.6618);
   Gama->SetBinError(23,36.24914);
   Gama->SetBinError(24,27.29469);
   Gama->SetBinError(25,16.12452);
   Gama->SetBinError(26,16.70329);
   Gama->SetBinError(27,12.20656);
   Gama->SetBinError(28,15.16575);
   Gama->SetBinError(29,10.58301);
   Gama->SetBinError(30,9.273618);
   Gama->SetBinError(31,6.324555);
   Gama->SetBinError(32,3.316625);
   Gama->SetBinError(33,3);
   Gama->SetBinError(34,4.472136);
   Gama->SetBinError(35,2.645751);
   Gama->SetBinError(36,2.236068);
   Gama->SetBinError(37,2.44949);
   Gama->SetBinError(38,1.414214);
   Gama->SetBinError(39,1);
   Gama->SetBinError(40,1);
   Gama->SetBinError(41,1);
   Gama->SetBinError(43,1.414214);
   Gama->SetBinError(44,1);
   Gama->SetBinError(47,2);
   Gama->SetBinError(51,1.732051);
   Gama->SetEntries(218);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Gama");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 218    ");
   AText = ptstats->AddText("Mean  =  34.94");
   AText = ptstats->AddText("Std Dev   =  34.61");
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
   ToF_10mm_2->Modified();
   ToF_10mm->cd();
  
// ------------>Primitives in pad: ToF_10mm_3
   TPad *ToF_10mm_3 = new TPad("ToF_10mm_3", "ToF_10mm_3",0.6766667,0.01,0.99,0.99);
   ToF_10mm_3->Draw();
   ToF_10mm_3->cd();
   ToF_10mm_3->Range(-3000,-1.158663,17000,3.010484);
   ToF_10mm_3->SetFillColor(0);
   ToF_10mm_3->SetBorderMode(0);
   ToF_10mm_3->SetBorderSize(2);
   ToF_10mm_3->SetLogy();
   ToF_10mm_3->SetGridx();
   ToF_10mm_3->SetGridy();
   ToF_10mm_3->SetLeftMargin(0.15);
   ToF_10mm_3->SetBottomMargin(0.15);
   ToF_10mm_3->SetFrameBorderMode(0);
   ToF_10mm_3->SetFrameBorderMode(0);
   
   TH1D *Alpha = new TH1D("Alpha","Alpha",100,0,15000);
   Alpha->SetBinContent(2,14);
   Alpha->SetBinContent(3,23);
   Alpha->SetBinContent(4,52);
   Alpha->SetBinContent(5,90);
   Alpha->SetBinContent(6,141);
   Alpha->SetBinContent(7,186);
   Alpha->SetBinContent(8,181);
   Alpha->SetBinContent(9,167);
   Alpha->SetBinContent(10,182);
   Alpha->SetBinContent(11,143);
   Alpha->SetBinContent(12,119);
   Alpha->SetBinContent(13,96);
   Alpha->SetBinContent(14,99);
   Alpha->SetBinContent(15,83);
   Alpha->SetBinContent(16,73);
   Alpha->SetBinContent(17,46);
   Alpha->SetBinContent(18,56);
   Alpha->SetBinContent(19,53);
   Alpha->SetBinContent(20,47);
   Alpha->SetBinContent(21,41);
   Alpha->SetBinContent(22,37);
   Alpha->SetBinContent(23,30);
   Alpha->SetBinContent(24,37);
   Alpha->SetBinContent(25,33);
   Alpha->SetBinContent(26,26);
   Alpha->SetBinContent(27,19);
   Alpha->SetBinContent(28,35);
   Alpha->SetBinContent(29,23);
   Alpha->SetBinContent(30,22);
   Alpha->SetBinContent(31,14);
   Alpha->SetBinContent(32,19);
   Alpha->SetBinContent(33,14);
   Alpha->SetBinContent(34,13);
   Alpha->SetBinContent(35,12);
   Alpha->SetBinContent(36,14);
   Alpha->SetBinContent(37,9);
   Alpha->SetBinContent(38,12);
   Alpha->SetBinContent(39,10);
   Alpha->SetBinContent(40,10);
   Alpha->SetBinContent(41,13);
   Alpha->SetBinContent(42,12);
   Alpha->SetBinContent(43,15);
   Alpha->SetBinContent(44,10);
   Alpha->SetBinContent(45,9);
   Alpha->SetBinContent(46,7);
   Alpha->SetBinContent(47,10);
   Alpha->SetBinContent(48,2);
   Alpha->SetBinContent(49,7);
   Alpha->SetBinContent(50,7);
   Alpha->SetBinContent(51,3);
   Alpha->SetBinContent(52,6);
   Alpha->SetBinContent(53,5);
   Alpha->SetBinContent(54,6);
   Alpha->SetBinContent(55,13);
   Alpha->SetBinContent(56,9);
   Alpha->SetBinContent(57,12);
   Alpha->SetBinContent(58,8);
   Alpha->SetBinContent(59,6);
   Alpha->SetBinContent(60,3);
   Alpha->SetBinContent(61,8);
   Alpha->SetBinContent(62,8);
   Alpha->SetBinContent(63,9);
   Alpha->SetBinContent(64,3);
   Alpha->SetBinContent(65,9);
   Alpha->SetBinContent(66,2);
   Alpha->SetBinContent(67,3);
   Alpha->SetBinContent(68,7);
   Alpha->SetBinContent(69,3);
   Alpha->SetBinContent(70,5);
   Alpha->SetBinContent(71,1);
   Alpha->SetBinContent(72,1);
   Alpha->SetBinContent(74,1);
   Alpha->SetBinContent(75,4);
   Alpha->SetBinContent(76,5);
   Alpha->SetBinContent(77,5);
   Alpha->SetBinContent(78,1);
   Alpha->SetBinContent(79,1);
   Alpha->SetBinContent(80,6);
   Alpha->SetBinContent(81,1);
   Alpha->SetBinContent(82,2);
   Alpha->SetBinContent(83,1);
   Alpha->SetBinContent(84,2);
   Alpha->SetBinContent(85,1);
   Alpha->SetBinContent(86,2);
   Alpha->SetBinContent(87,2);
   Alpha->SetBinContent(88,1);
   Alpha->SetBinContent(89,2);
   Alpha->SetBinContent(90,1);
   Alpha->SetBinContent(91,4);
   Alpha->SetBinContent(92,4);
   Alpha->SetBinContent(93,1);
   Alpha->SetBinContent(94,5);
   Alpha->SetBinContent(96,4);
   Alpha->SetBinContent(97,1);
   Alpha->SetBinContent(99,2);
   Alpha->SetBinContent(100,33);
   Alpha->SetBinError(2,3.741657);
   Alpha->SetBinError(3,4.795832);
   Alpha->SetBinError(4,8.485281);
   Alpha->SetBinError(5,11.57584);
   Alpha->SetBinError(6,16.46208);
   Alpha->SetBinError(7,21.0238);
   Alpha->SetBinError(8,20.66398);
   Alpha->SetBinError(9,17.86057);
   Alpha->SetBinError(10,19.69772);
   Alpha->SetBinError(11,17.11724);
   Alpha->SetBinError(12,14.52584);
   Alpha->SetBinError(13,12.49);
   Alpha->SetBinError(14,12.52996);
   Alpha->SetBinError(15,11.35782);
   Alpha->SetBinError(16,10.34408);
   Alpha->SetBinError(17,7.874008);
   Alpha->SetBinError(18,8.831761);
   Alpha->SetBinError(19,8.42615);
   Alpha->SetBinError(20,7.937254);
   Alpha->SetBinError(21,7.141428);
   Alpha->SetBinError(22,6.557439);
   Alpha->SetBinError(23,6.324555);
   Alpha->SetBinError(24,6.708204);
   Alpha->SetBinError(25,5.91608);
   Alpha->SetBinError(26,5.09902);
   Alpha->SetBinError(27,4.795832);
   Alpha->SetBinError(28,6.708204);
   Alpha->SetBinError(29,5.196152);
   Alpha->SetBinError(30,4.898979);
   Alpha->SetBinError(31,4);
   Alpha->SetBinError(32,4.795832);
   Alpha->SetBinError(33,4.242641);
   Alpha->SetBinError(34,3.872983);
   Alpha->SetBinError(35,3.741657);
   Alpha->SetBinError(36,4.472136);
   Alpha->SetBinError(37,3);
   Alpha->SetBinError(38,3.464102);
   Alpha->SetBinError(39,3.464102);
   Alpha->SetBinError(40,3.464102);
   Alpha->SetBinError(41,4.123106);
   Alpha->SetBinError(42,4.242641);
   Alpha->SetBinError(43,4.123106);
   Alpha->SetBinError(44,3.162278);
   Alpha->SetBinError(45,3);
   Alpha->SetBinError(46,2.645751);
   Alpha->SetBinError(47,3.162278);
   Alpha->SetBinError(48,1.414214);
   Alpha->SetBinError(49,2.645751);
   Alpha->SetBinError(50,2.645751);
   Alpha->SetBinError(51,1.732051);
   Alpha->SetBinError(52,2.44949);
   Alpha->SetBinError(53,2.236068);
   Alpha->SetBinError(54,2.44949);
   Alpha->SetBinError(55,3.605551);
   Alpha->SetBinError(56,3);
   Alpha->SetBinError(57,3.741657);
   Alpha->SetBinError(58,2.828427);
   Alpha->SetBinError(59,2.44949);
   Alpha->SetBinError(60,1.732051);
   Alpha->SetBinError(61,2.828427);
   Alpha->SetBinError(62,2.828427);
   Alpha->SetBinError(63,3);
   Alpha->SetBinError(64,2.236068);
   Alpha->SetBinError(65,3);
   Alpha->SetBinError(66,1.414214);
   Alpha->SetBinError(67,1.732051);
   Alpha->SetBinError(68,2.645751);
   Alpha->SetBinError(69,1.732051);
   Alpha->SetBinError(70,2.236068);
   Alpha->SetBinError(71,1);
   Alpha->SetBinError(72,1);
   Alpha->SetBinError(74,1);
   Alpha->SetBinError(75,2);
   Alpha->SetBinError(76,2.236068);
   Alpha->SetBinError(77,2.236068);
   Alpha->SetBinError(78,1);
   Alpha->SetBinError(79,1);
   Alpha->SetBinError(80,2.44949);
   Alpha->SetBinError(81,1);
   Alpha->SetBinError(82,1.414214);
   Alpha->SetBinError(83,1);
   Alpha->SetBinError(84,1.414214);
   Alpha->SetBinError(85,1);
   Alpha->SetBinError(86,1.414214);
   Alpha->SetBinError(87,1.414214);
   Alpha->SetBinError(88,1);
   Alpha->SetBinError(89,1.414214);
   Alpha->SetBinError(90,1);
   Alpha->SetBinError(91,2);
   Alpha->SetBinError(92,2);
   Alpha->SetBinError(93,1);
   Alpha->SetBinError(94,2.236068);
   Alpha->SetBinError(96,2);
   Alpha->SetBinError(97,1);
   Alpha->SetBinError(99,1.414214);
   Alpha->SetBinError(100,32.01562);
   Alpha->SetEntries(1936);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Alpha");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 1936   ");
   AText = ptstats->AddText("Mean  =   2915");
   AText = ptstats->AddText("Std Dev   =   2908");
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
   ToF_10mm_3->Modified();
   ToF_10mm->cd();
   ToF_10mm->Modified();
   ToF_10mm->cd();
   ToF_10mm->SetSelected(ToF_10mm);
}
