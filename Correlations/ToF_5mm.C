void ToF_5mm()
{
//=========Macro generated from canvas: ToF_5mm/ToF_5mm
//=========  (Tue Jan 23 13:31:03 2018) by ROOT version6.08/04
   TCanvas *ToF_5mm = new TCanvas("ToF_5mm", "ToF_5mm",0,50,1212,505);
   gStyle->SetOptTitle(0);
   ToF_5mm->SetHighLightColor(2);
   ToF_5mm->Range(0,0,1,1);
   ToF_5mm->SetFillColor(0);
   ToF_5mm->SetBorderMode(0);
   ToF_5mm->SetBorderSize(2);
   ToF_5mm->SetLeftMargin(0.15);
   ToF_5mm->SetBottomMargin(0.15);
   ToF_5mm->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: ToF_5mm_1
   TPad *ToF_5mm_1 = new TPad("ToF_5mm_1", "ToF_5mm_1",0.01,0.01,0.3233333,0.99);
   ToF_5mm_1->Draw();
   ToF_5mm_1->cd();
   ToF_5mm_1->Range(-600,-1.4406,3400,4.608131);
   ToF_5mm_1->SetFillColor(0);
   ToF_5mm_1->SetBorderMode(0);
   ToF_5mm_1->SetBorderSize(2);
   ToF_5mm_1->SetLogy();
   ToF_5mm_1->SetGridx();
   ToF_5mm_1->SetGridy();
   ToF_5mm_1->SetLeftMargin(0.15);
   ToF_5mm_1->SetBottomMargin(0.15);
   ToF_5mm_1->SetFrameBorderMode(0);
   ToF_5mm_1->SetFrameBorderMode(0);
   
   TH1D *Beta = new TH1D("Beta","Beta",100,0,3000);
   Beta->SetBinContent(1,1008);
   Beta->SetBinContent(2,3506);
   Beta->SetBinContent(3,4135);
   Beta->SetBinContent(4,4494);
   Beta->SetBinContent(5,4123);
   Beta->SetBinContent(6,3803);
   Beta->SetBinContent(7,3236);
   Beta->SetBinContent(8,3039);
   Beta->SetBinContent(9,2566);
   Beta->SetBinContent(10,2227);
   Beta->SetBinContent(11,1650);
   Beta->SetBinContent(12,1402);
   Beta->SetBinContent(13,1000);
   Beta->SetBinContent(14,846);
   Beta->SetBinContent(15,746);
   Beta->SetBinContent(16,611);
   Beta->SetBinContent(17,553);
   Beta->SetBinContent(18,480);
   Beta->SetBinContent(19,425);
   Beta->SetBinContent(20,407);
   Beta->SetBinContent(21,369);
   Beta->SetBinContent(22,332);
   Beta->SetBinContent(23,276);
   Beta->SetBinContent(24,240);
   Beta->SetBinContent(25,246);
   Beta->SetBinContent(26,205);
   Beta->SetBinContent(27,182);
   Beta->SetBinContent(28,147);
   Beta->SetBinContent(29,144);
   Beta->SetBinContent(30,150);
   Beta->SetBinContent(31,131);
   Beta->SetBinContent(32,118);
   Beta->SetBinContent(33,81);
   Beta->SetBinContent(34,90);
   Beta->SetBinContent(35,89);
   Beta->SetBinContent(36,79);
   Beta->SetBinContent(37,86);
   Beta->SetBinContent(38,77);
   Beta->SetBinContent(39,53);
   Beta->SetBinContent(40,55);
   Beta->SetBinContent(41,49);
   Beta->SetBinContent(42,47);
   Beta->SetBinContent(43,46);
   Beta->SetBinContent(44,49);
   Beta->SetBinContent(45,35);
   Beta->SetBinContent(46,39);
   Beta->SetBinContent(47,31);
   Beta->SetBinContent(48,26);
   Beta->SetBinContent(49,35);
   Beta->SetBinContent(50,21);
   Beta->SetBinContent(51,24);
   Beta->SetBinContent(52,20);
   Beta->SetBinContent(53,19);
   Beta->SetBinContent(54,15);
   Beta->SetBinContent(55,11);
   Beta->SetBinContent(56,22);
   Beta->SetBinContent(57,19);
   Beta->SetBinContent(58,19);
   Beta->SetBinContent(59,9);
   Beta->SetBinContent(60,15);
   Beta->SetBinContent(61,16);
   Beta->SetBinContent(62,16);
   Beta->SetBinContent(63,9);
   Beta->SetBinContent(64,16);
   Beta->SetBinContent(65,12);
   Beta->SetBinContent(66,13);
   Beta->SetBinContent(67,14);
   Beta->SetBinContent(68,16);
   Beta->SetBinContent(69,16);
   Beta->SetBinContent(70,10);
   Beta->SetBinContent(71,7);
   Beta->SetBinContent(72,8);
   Beta->SetBinContent(73,4);
   Beta->SetBinContent(74,11);
   Beta->SetBinContent(75,10);
   Beta->SetBinContent(76,6);
   Beta->SetBinContent(77,7);
   Beta->SetBinContent(78,9);
   Beta->SetBinContent(79,8);
   Beta->SetBinContent(80,4);
   Beta->SetBinContent(81,9);
   Beta->SetBinContent(82,6);
   Beta->SetBinContent(83,2);
   Beta->SetBinContent(84,8);
   Beta->SetBinContent(85,6);
   Beta->SetBinContent(86,5);
   Beta->SetBinContent(87,6);
   Beta->SetBinContent(88,6);
   Beta->SetBinContent(89,4);
   Beta->SetBinContent(90,1);
   Beta->SetBinContent(91,6);
   Beta->SetBinContent(92,3);
   Beta->SetBinContent(93,4);
   Beta->SetBinContent(94,3);
   Beta->SetBinContent(95,6);
   Beta->SetBinContent(96,7);
   Beta->SetBinContent(97,2);
   Beta->SetBinContent(98,3);
   Beta->SetBinContent(99,2);
   Beta->SetBinContent(100,2);
   Beta->SetBinContent(101,171);
   Beta->SetBinError(1,288.555);
   Beta->SetBinError(2,643.0614);
   Beta->SetBinError(3,758.3831);
   Beta->SetBinError(4,823.5156);
   Beta->SetBinError(5,756.0337);
   Beta->SetBinError(6,697.4518);
   Beta->SetBinError(7,593.7171);
   Beta->SetBinError(8,559.5596);
   Beta->SetBinError(9,473.0814);
   Beta->SetBinError(10,411.2481);
   Beta->SetBinError(11,304.263);
   Beta->SetBinError(12,261.0555);
   Beta->SetBinError(13,185.4131);
   Beta->SetBinError(14,157.4039);
   Beta->SetBinError(15,138.181);
   Beta->SetBinError(16,114.9391);
   Beta->SetBinError(17,103.5133);
   Beta->SetBinError(18,89.16277);
   Beta->SetBinError(19,80.19352);
   Beta->SetBinError(20,76.88303);
   Beta->SetBinError(21,70.91544);
   Beta->SetBinError(22,63.08724);
   Beta->SetBinError(23,53.04715);
   Beta->SetBinError(24,46);
   Beta->SetBinError(25,46.98936);
   Beta->SetBinError(26,40.6325);
   Beta->SetBinError(27,35.69314);
   Beta->SetBinError(28,29.10326);
   Beta->SetBinError(29,28.94823);
   Beta->SetBinError(30,29.79933);
   Beta->SetBinError(31,26.96294);
   Beta->SetBinError(32,23.91652);
   Beta->SetBinError(33,17.4069);
   Beta->SetBinError(34,19.79899);
   Beta->SetBinError(35,18.57418);
   Beta->SetBinError(36,16.64332);
   Beta->SetBinError(37,17.66352);
   Beta->SetBinError(38,16.58312);
   Beta->SetBinError(39,12.60952);
   Beta->SetBinError(40,11.35782);
   Beta->SetBinError(41,10.34408);
   Beta->SetBinError(42,11.35782);
   Beta->SetBinError(43,10.3923);
   Beta->SetBinError(44,11.26943);
   Beta->SetBinError(45,8.544004);
   Beta->SetBinError(46,9.643651);
   Beta->SetBinError(47,7.28011);
   Beta->SetBinError(48,6.78233);
   Beta->SetBinError(49,8.42615);
   Beta->SetBinError(50,5.385165);
   Beta->SetBinError(51,6.164414);
   Beta->SetBinError(52,5.830952);
   Beta->SetBinError(53,5.567764);
   Beta->SetBinError(54,4.123106);
   Beta->SetBinError(55,4.123106);
   Beta->SetBinError(56,6.480741);
   Beta->SetBinError(57,5.744563);
   Beta->SetBinError(58,5.385165);
   Beta->SetBinError(59,3.316625);
   Beta->SetBinError(60,5.196152);
   Beta->SetBinError(61,4.472136);
   Beta->SetBinError(62,4.472136);
   Beta->SetBinError(63,3);
   Beta->SetBinError(64,4.898979);
   Beta->SetBinError(65,4.472136);
   Beta->SetBinError(66,4.358899);
   Beta->SetBinError(67,4.242641);
   Beta->SetBinError(68,4.472136);
   Beta->SetBinError(69,5.09902);
   Beta->SetBinError(70,3.741657);
   Beta->SetBinError(71,3);
   Beta->SetBinError(72,2.828427);
   Beta->SetBinError(73,2.44949);
   Beta->SetBinError(74,3.872983);
   Beta->SetBinError(75,3.464102);
   Beta->SetBinError(76,2.828427);
   Beta->SetBinError(77,3);
   Beta->SetBinError(78,3.316625);
   Beta->SetBinError(79,2.828427);
   Beta->SetBinError(80,2);
   Beta->SetBinError(81,3.605551);
   Beta->SetBinError(82,2.44949);
   Beta->SetBinError(83,1.414214);
   Beta->SetBinError(84,3.162278);
   Beta->SetBinError(85,2.44949);
   Beta->SetBinError(86,2.236068);
   Beta->SetBinError(87,2.44949);
   Beta->SetBinError(88,2.828427);
   Beta->SetBinError(89,2);
   Beta->SetBinError(90,1);
   Beta->SetBinError(91,2.44949);
   Beta->SetBinError(92,1.732051);
   Beta->SetBinError(93,2);
   Beta->SetBinError(94,1.732051);
   Beta->SetBinError(95,2.828427);
   Beta->SetBinError(96,2.645751);
   Beta->SetBinError(97,1.414214);
   Beta->SetBinError(98,2.236068);
   Beta->SetBinError(99,1.414214);
   Beta->SetBinError(100,1.414214);
   Beta->SetBinError(101,13.30413);
   Beta->SetEntries(1946);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   TText *AText = ptstats->AddText("Beta");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 1946   ");
   AText = ptstats->AddText("Mean  =  272.3");
   AText = ptstats->AddText("Std Dev   =  293.7");
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
   ToF_5mm_1->Modified();
   ToF_5mm->cd();
  
// ------------>Primitives in pad: ToF_5mm_2
   TPad *ToF_5mm_2 = new TPad("ToF_5mm_2", "ToF_5mm_2",0.3433333,0.01,0.6566667,0.99);
   ToF_5mm_2->Draw();
   ToF_5mm_2->cd();
   ToF_5mm_2->Range(-60,-1.412578,340,4.449336);
   ToF_5mm_2->SetFillColor(0);
   ToF_5mm_2->SetBorderMode(0);
   ToF_5mm_2->SetBorderSize(2);
   ToF_5mm_2->SetLogy();
   ToF_5mm_2->SetGridx();
   ToF_5mm_2->SetGridy();
   ToF_5mm_2->SetLeftMargin(0.15);
   ToF_5mm_2->SetBottomMargin(0.15);
   ToF_5mm_2->SetFrameBorderMode(0);
   ToF_5mm_2->SetFrameBorderMode(0);
   
   TH1D *Gama = new TH1D("Gama","Gama",50,0,300);
   Gama->SetBinContent(1,1405);
   Gama->SetBinContent(2,2690);
   Gama->SetBinContent(3,2144);
   Gama->SetBinContent(4,1600);
   Gama->SetBinContent(5,1035);
   Gama->SetBinContent(6,777);
   Gama->SetBinContent(7,649);
   Gama->SetBinContent(8,542);
   Gama->SetBinContent(9,537);
   Gama->SetBinContent(10,540);
   Gama->SetBinContent(11,467);
   Gama->SetBinContent(12,412);
   Gama->SetBinContent(13,346);
   Gama->SetBinContent(14,340);
   Gama->SetBinContent(15,305);
   Gama->SetBinContent(16,228);
   Gama->SetBinContent(17,187);
   Gama->SetBinContent(18,175);
   Gama->SetBinContent(19,156);
   Gama->SetBinContent(20,122);
   Gama->SetBinContent(21,114);
   Gama->SetBinContent(22,69);
   Gama->SetBinContent(23,74);
   Gama->SetBinContent(24,57);
   Gama->SetBinContent(25,34);
   Gama->SetBinContent(26,24);
   Gama->SetBinContent(27,29);
   Gama->SetBinContent(28,19);
   Gama->SetBinContent(29,13);
   Gama->SetBinContent(30,13);
   Gama->SetBinContent(31,14);
   Gama->SetBinContent(32,10);
   Gama->SetBinContent(33,7);
   Gama->SetBinContent(34,3);
   Gama->SetBinContent(35,2);
   Gama->SetBinContent(36,4);
   Gama->SetBinContent(37,5);
   Gama->SetBinContent(39,2);
   Gama->SetBinContent(40,1);
   Gama->SetBinContent(41,1);
   Gama->SetBinContent(45,1);
   Gama->SetBinError(1,1068.708);
   Gama->SetBinError(2,1161.198);
   Gama->SetBinError(3,877.2491);
   Gama->SetBinError(4,656.25);
   Gama->SetBinError(5,432.554);
   Gama->SetBinError(6,330.2832);
   Gama->SetBinError(7,270.3461);
   Gama->SetBinError(8,229.7694);
   Gama->SetBinError(9,221.9031);
   Gama->SetBinError(10,223.9196);
   Gama->SetBinError(11,194.8615);
   Gama->SetBinError(12,175.9034);
   Gama->SetBinError(13,144.7757);
   Gama->SetBinError(14,141.294);
   Gama->SetBinError(15,127.1023);
   Gama->SetBinError(16,95.18403);
   Gama->SetBinError(17,76.89603);
   Gama->SetBinError(18,72.8217);
   Gama->SetBinError(19,65.68105);
   Gama->SetBinError(20,50.59644);
   Gama->SetBinError(21,50.25933);
   Gama->SetBinError(22,29.3087);
   Gama->SetBinError(23,31.20897);
   Gama->SetBinError(24,24.55606);
   Gama->SetBinError(25,15.42725);
   Gama->SetBinError(26,10.19804);
   Gama->SetBinError(27,13.52775);
   Gama->SetBinError(28,8.660254);
   Gama->SetBinError(29,5.91608);
   Gama->SetBinError(30,5.91608);
   Gama->SetBinError(31,7.211103);
   Gama->SetBinError(32,4.472136);
   Gama->SetBinError(33,3.316625);
   Gama->SetBinError(34,1.732051);
   Gama->SetBinError(35,1.414214);
   Gama->SetBinError(36,2.828427);
   Gama->SetBinError(37,2.236068);
   Gama->SetBinError(39,1.414214);
   Gama->SetBinError(40,1);
   Gama->SetBinError(41,1);
   Gama->SetBinError(45,1);
   Gama->SetEntries(209);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Gama");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 209    ");
   AText = ptstats->AddText("Mean  =  36.15");
   AText = ptstats->AddText("Std Dev   =  34.58");
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
   ToF_5mm_2->Modified();
   ToF_5mm->cd();
  
// ------------>Primitives in pad: ToF_5mm_3
   TPad *ToF_5mm_3 = new TPad("ToF_5mm_3", "ToF_5mm_3",0.6766667,0.01,0.99,0.99);
   ToF_5mm_3->Draw();
   ToF_5mm_3->cd();
   ToF_5mm_3->Range(-3000,-1.105302,17000,2.708108);
   ToF_5mm_3->SetFillColor(0);
   ToF_5mm_3->SetBorderMode(0);
   ToF_5mm_3->SetBorderSize(2);
   ToF_5mm_3->SetLogy();
   ToF_5mm_3->SetGridx();
   ToF_5mm_3->SetGridy();
   ToF_5mm_3->SetLeftMargin(0.15);
   ToF_5mm_3->SetBottomMargin(0.15);
   ToF_5mm_3->SetFrameBorderMode(0);
   ToF_5mm_3->SetFrameBorderMode(0);
   
   TH1D *Alpha = new TH1D("Alpha","Alpha",100,0,15000);
   Alpha->SetBinContent(2,15);
   Alpha->SetBinContent(3,13);
   Alpha->SetBinContent(4,37);
   Alpha->SetBinContent(5,52);
   Alpha->SetBinContent(6,61);
   Alpha->SetBinContent(7,72);
   Alpha->SetBinContent(8,100);
   Alpha->SetBinContent(9,78);
   Alpha->SetBinContent(10,83);
   Alpha->SetBinContent(11,54);
   Alpha->SetBinContent(12,54);
   Alpha->SetBinContent(13,63);
   Alpha->SetBinContent(14,39);
   Alpha->SetBinContent(15,37);
   Alpha->SetBinContent(16,27);
   Alpha->SetBinContent(17,33);
   Alpha->SetBinContent(18,22);
   Alpha->SetBinContent(19,14);
   Alpha->SetBinContent(20,19);
   Alpha->SetBinContent(21,17);
   Alpha->SetBinContent(22,17);
   Alpha->SetBinContent(23,9);
   Alpha->SetBinContent(24,15);
   Alpha->SetBinContent(25,11);
   Alpha->SetBinContent(26,2);
   Alpha->SetBinContent(27,9);
   Alpha->SetBinContent(28,9);
   Alpha->SetBinContent(29,6);
   Alpha->SetBinContent(30,7);
   Alpha->SetBinContent(31,12);
   Alpha->SetBinContent(32,5);
   Alpha->SetBinContent(33,6);
   Alpha->SetBinContent(34,6);
   Alpha->SetBinContent(35,9);
   Alpha->SetBinContent(36,4);
   Alpha->SetBinContent(37,5);
   Alpha->SetBinContent(38,4);
   Alpha->SetBinContent(39,2);
   Alpha->SetBinContent(40,4);
   Alpha->SetBinContent(41,7);
   Alpha->SetBinContent(42,5);
   Alpha->SetBinContent(43,3);
   Alpha->SetBinContent(44,8);
   Alpha->SetBinContent(45,5);
   Alpha->SetBinContent(46,4);
   Alpha->SetBinContent(47,5);
   Alpha->SetBinContent(48,4);
   Alpha->SetBinContent(49,4);
   Alpha->SetBinContent(50,6);
   Alpha->SetBinContent(51,5);
   Alpha->SetBinContent(52,16);
   Alpha->SetBinContent(53,9);
   Alpha->SetBinContent(54,16);
   Alpha->SetBinContent(55,3);
   Alpha->SetBinContent(56,4);
   Alpha->SetBinContent(57,8);
   Alpha->SetBinContent(58,6);
   Alpha->SetBinContent(59,3);
   Alpha->SetBinContent(60,5);
   Alpha->SetBinContent(61,3);
   Alpha->SetBinContent(62,4);
   Alpha->SetBinContent(63,4);
   Alpha->SetBinContent(64,2);
   Alpha->SetBinContent(65,1);
   Alpha->SetBinContent(67,3);
   Alpha->SetBinContent(68,2);
   Alpha->SetBinContent(69,1);
   Alpha->SetBinContent(70,2);
   Alpha->SetBinContent(71,1);
   Alpha->SetBinContent(72,1);
   Alpha->SetBinContent(73,1);
   Alpha->SetBinContent(74,1);
   Alpha->SetBinContent(75,1);
   Alpha->SetBinContent(76,1);
   Alpha->SetBinContent(79,1);
   Alpha->SetBinContent(80,1);
   Alpha->SetBinContent(83,1);
   Alpha->SetBinContent(84,2);
   Alpha->SetBinContent(85,1);
   Alpha->SetBinContent(86,1);
   Alpha->SetBinContent(89,1);
   Alpha->SetBinContent(93,1);
   Alpha->SetBinContent(94,2);
   Alpha->SetBinContent(97,1);
   Alpha->SetBinContent(98,1);
   Alpha->SetBinContent(100,3);
   Alpha->SetBinError(2,3.872983);
   Alpha->SetBinError(3,3.872983);
   Alpha->SetBinError(4,7.681146);
   Alpha->SetBinError(5,8.246211);
   Alpha->SetBinError(6,9.219544);
   Alpha->SetBinError(7,10.3923);
   Alpha->SetBinError(8,12);
   Alpha->SetBinError(9,10.95445);
   Alpha->SetBinError(10,10.81665);
   Alpha->SetBinError(11,8.246211);
   Alpha->SetBinError(12,8.3666);
   Alpha->SetBinError(13,9.219544);
   Alpha->SetBinError(14,7);
   Alpha->SetBinError(15,6.403124);
   Alpha->SetBinError(16,5.91608);
   Alpha->SetBinError(17,6.244998);
   Alpha->SetBinError(18,4.898979);
   Alpha->SetBinError(19,3.741657);
   Alpha->SetBinError(20,4.358899);
   Alpha->SetBinError(21,4.123106);
   Alpha->SetBinError(22,4.582576);
   Alpha->SetBinError(23,3);
   Alpha->SetBinError(24,3.872983);
   Alpha->SetBinError(25,3.316625);
   Alpha->SetBinError(26,1.414214);
   Alpha->SetBinError(27,3);
   Alpha->SetBinError(28,3);
   Alpha->SetBinError(29,2.44949);
   Alpha->SetBinError(30,3);
   Alpha->SetBinError(31,3.464102);
   Alpha->SetBinError(32,2.236068);
   Alpha->SetBinError(33,2.44949);
   Alpha->SetBinError(34,2.44949);
   Alpha->SetBinError(35,3);
   Alpha->SetBinError(36,2);
   Alpha->SetBinError(37,2.236068);
   Alpha->SetBinError(38,2);
   Alpha->SetBinError(39,1.414214);
   Alpha->SetBinError(40,2);
   Alpha->SetBinError(41,2.645751);
   Alpha->SetBinError(42,2.236068);
   Alpha->SetBinError(43,1.732051);
   Alpha->SetBinError(44,2.828427);
   Alpha->SetBinError(45,2.236068);
   Alpha->SetBinError(46,2);
   Alpha->SetBinError(47,2.236068);
   Alpha->SetBinError(48,2);
   Alpha->SetBinError(49,2);
   Alpha->SetBinError(50,2.828427);
   Alpha->SetBinError(51,2.236068);
   Alpha->SetBinError(52,4.898979);
   Alpha->SetBinError(53,3);
   Alpha->SetBinError(54,4.242641);
   Alpha->SetBinError(55,1.732051);
   Alpha->SetBinError(56,2);
   Alpha->SetBinError(57,2.828427);
   Alpha->SetBinError(58,2.44949);
   Alpha->SetBinError(59,1.732051);
   Alpha->SetBinError(60,2.236068);
   Alpha->SetBinError(61,1.732051);
   Alpha->SetBinError(62,2);
   Alpha->SetBinError(63,2);
   Alpha->SetBinError(64,1.414214);
   Alpha->SetBinError(65,1);
   Alpha->SetBinError(67,1.732051);
   Alpha->SetBinError(68,1.414214);
   Alpha->SetBinError(69,1);
   Alpha->SetBinError(70,1.414214);
   Alpha->SetBinError(71,1);
   Alpha->SetBinError(72,1);
   Alpha->SetBinError(73,1);
   Alpha->SetBinError(74,1);
   Alpha->SetBinError(75,1);
   Alpha->SetBinError(76,1);
   Alpha->SetBinError(79,1);
   Alpha->SetBinError(80,1);
   Alpha->SetBinError(83,1);
   Alpha->SetBinError(84,1.414214);
   Alpha->SetBinError(85,1);
   Alpha->SetBinError(86,1);
   Alpha->SetBinError(89,1);
   Alpha->SetBinError(93,1);
   Alpha->SetBinError(94,1.414214);
   Alpha->SetBinError(97,1);
   Alpha->SetBinError(98,1);
   Alpha->SetBinError(100,2.236068);
   Alpha->SetEntries(1055);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Alpha");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 1055   ");
   AText = ptstats->AddText("Mean  =   2805");
   AText = ptstats->AddText("Std Dev   =   2668");
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
   ToF_5mm_3->Modified();
   ToF_5mm->cd();
   ToF_5mm->Modified();
   ToF_5mm->cd();
   ToF_5mm->SetSelected(ToF_5mm);
}
