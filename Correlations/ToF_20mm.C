void ToF_20mm()
{
//=========Macro generated from canvas: ToF_20mm/ToF_20mm
//=========  (Tue Jan 23 13:30:34 2018) by ROOT version6.08/04
   TCanvas *ToF_20mm = new TCanvas("ToF_20mm", "ToF_20mm",0,50,1212,505);
   gStyle->SetOptTitle(0);
   ToF_20mm->SetHighLightColor(2);
   ToF_20mm->Range(0,0,1,1);
   ToF_20mm->SetFillColor(0);
   ToF_20mm->SetBorderMode(0);
   ToF_20mm->SetBorderSize(2);
   ToF_20mm->SetLeftMargin(0.15);
   ToF_20mm->SetBottomMargin(0.15);
   ToF_20mm->SetFrameBorderMode(0);
  
// ------------>Primitives in pad: ToF_20mm_1
   TPad *ToF_20mm_1 = new TPad("ToF_20mm_1", "ToF_20mm_1",0.01,0.01,0.3233333,0.99);
   ToF_20mm_1->Draw();
   ToF_20mm_1->cd();
   ToF_20mm_1->Range(-600,-1.442986,3400,4.62165);
   ToF_20mm_1->SetFillColor(0);
   ToF_20mm_1->SetBorderMode(0);
   ToF_20mm_1->SetBorderSize(2);
   ToF_20mm_1->SetLogy();
   ToF_20mm_1->SetGridx();
   ToF_20mm_1->SetGridy();
   ToF_20mm_1->SetLeftMargin(0.15);
   ToF_20mm_1->SetBottomMargin(0.15);
   ToF_20mm_1->SetFrameBorderMode(0);
   ToF_20mm_1->SetFrameBorderMode(0);
   
   TH1D *Beta = new TH1D("Beta","Beta",100,0,3000);
   Beta->SetBinContent(1,905);
   Beta->SetBinContent(2,3367);
   Beta->SetBinContent(3,4381);
   Beta->SetBinContent(4,4620);
   Beta->SetBinContent(5,4112);
   Beta->SetBinContent(6,3697);
   Beta->SetBinContent(7,3258);
   Beta->SetBinContent(8,2933);
   Beta->SetBinContent(9,2497);
   Beta->SetBinContent(10,2036);
   Beta->SetBinContent(11,1690);
   Beta->SetBinContent(12,1184);
   Beta->SetBinContent(13,929);
   Beta->SetBinContent(14,868);
   Beta->SetBinContent(15,692);
   Beta->SetBinContent(16,649);
   Beta->SetBinContent(17,520);
   Beta->SetBinContent(18,536);
   Beta->SetBinContent(19,412);
   Beta->SetBinContent(20,397);
   Beta->SetBinContent(21,334);
   Beta->SetBinContent(22,286);
   Beta->SetBinContent(23,258);
   Beta->SetBinContent(24,228);
   Beta->SetBinContent(25,222);
   Beta->SetBinContent(26,162);
   Beta->SetBinContent(27,157);
   Beta->SetBinContent(28,152);
   Beta->SetBinContent(29,126);
   Beta->SetBinContent(30,137);
   Beta->SetBinContent(31,125);
   Beta->SetBinContent(32,124);
   Beta->SetBinContent(33,100);
   Beta->SetBinContent(34,90);
   Beta->SetBinContent(35,80);
   Beta->SetBinContent(36,66);
   Beta->SetBinContent(37,65);
   Beta->SetBinContent(38,68);
   Beta->SetBinContent(39,42);
   Beta->SetBinContent(40,43);
   Beta->SetBinContent(41,50);
   Beta->SetBinContent(42,30);
   Beta->SetBinContent(43,48);
   Beta->SetBinContent(44,31);
   Beta->SetBinContent(45,36);
   Beta->SetBinContent(46,33);
   Beta->SetBinContent(47,15);
   Beta->SetBinContent(48,34);
   Beta->SetBinContent(49,26);
   Beta->SetBinContent(50,32);
   Beta->SetBinContent(51,21);
   Beta->SetBinContent(52,18);
   Beta->SetBinContent(53,14);
   Beta->SetBinContent(54,12);
   Beta->SetBinContent(55,26);
   Beta->SetBinContent(56,12);
   Beta->SetBinContent(57,20);
   Beta->SetBinContent(58,11);
   Beta->SetBinContent(59,15);
   Beta->SetBinContent(60,12);
   Beta->SetBinContent(61,10);
   Beta->SetBinContent(62,13);
   Beta->SetBinContent(63,11);
   Beta->SetBinContent(64,10);
   Beta->SetBinContent(65,8);
   Beta->SetBinContent(66,11);
   Beta->SetBinContent(67,12);
   Beta->SetBinContent(68,14);
   Beta->SetBinContent(69,8);
   Beta->SetBinContent(70,8);
   Beta->SetBinContent(71,8);
   Beta->SetBinContent(72,5);
   Beta->SetBinContent(73,5);
   Beta->SetBinContent(74,8);
   Beta->SetBinContent(75,4);
   Beta->SetBinContent(76,2);
   Beta->SetBinContent(77,7);
   Beta->SetBinContent(78,6);
   Beta->SetBinContent(79,5);
   Beta->SetBinContent(80,6);
   Beta->SetBinContent(81,6);
   Beta->SetBinContent(82,4);
   Beta->SetBinContent(83,1);
   Beta->SetBinContent(84,5);
   Beta->SetBinContent(85,3);
   Beta->SetBinContent(86,4);
   Beta->SetBinContent(87,3);
   Beta->SetBinContent(88,6);
   Beta->SetBinContent(90,1);
   Beta->SetBinContent(91,6);
   Beta->SetBinContent(92,7);
   Beta->SetBinContent(93,2);
   Beta->SetBinContent(94,4);
   Beta->SetBinContent(95,3);
   Beta->SetBinContent(96,2);
   Beta->SetBinContent(97,3);
   Beta->SetBinContent(98,2);
   Beta->SetBinContent(99,2);
   Beta->SetBinContent(100,4);
   Beta->SetBinContent(101,119);
   Beta->SetBinError(1,261.3523);
   Beta->SetBinError(2,616.6498);
   Beta->SetBinError(3,805.1441);
   Beta->SetBinError(4,845.5945);
   Beta->SetBinError(5,753.1109);
   Beta->SetBinError(6,676.9128);
   Beta->SetBinError(7,597.6035);
   Beta->SetBinError(8,538.7922);
   Beta->SetBinError(9,458.721);
   Beta->SetBinError(10,375.2759);
   Beta->SetBinError(11,310.6574);
   Beta->SetBinError(12,218.1788);
   Beta->SetBinError(13,172.3514);
   Beta->SetBinError(14,160.5304);
   Beta->SetBinError(15,128.8177);
   Beta->SetBinError(16,121.0578);
   Beta->SetBinError(17,98.6509);
   Beta->SetBinError(18,100.2098);
   Beta->SetBinError(19,78.31986);
   Beta->SetBinError(20,75.91443);
   Beta->SetBinError(21,63.52952);
   Beta->SetBinError(22,55.40758);
   Beta->SetBinError(23,50.11986);
   Beta->SetBinError(24,44.02272);
   Beta->SetBinError(25,42.44997);
   Beta->SetBinError(26,32.80244);
   Beta->SetBinError(27,31.09662);
   Beta->SetBinError(28,30.62679);
   Beta->SetBinError(29,25.17936);
   Beta->SetBinError(30,27.80288);
   Beta->SetBinError(31,25.39685);
   Beta->SetBinError(32,25.13961);
   Beta->SetBinError(33,19.74842);
   Beta->SetBinError(34,19.39072);
   Beta->SetBinError(35,16.24808);
   Beta->SetBinError(36,14.62874);
   Beta->SetBinError(37,14.52584);
   Beta->SetBinError(38,15.09967);
   Beta->SetBinError(39,9.591663);
   Beta->SetBinError(40,9.848858);
   Beta->SetBinError(41,11.22497);
   Beta->SetBinError(42,7.745967);
   Beta->SetBinError(43,11.31371);
   Beta->SetBinError(44,8.062258);
   Beta->SetBinError(45,9.591663);
   Beta->SetBinError(46,8.544004);
   Beta->SetBinError(47,4.358899);
   Beta->SetBinError(48,8.124038);
   Beta->SetBinError(49,7.211103);
   Beta->SetBinError(50,7.874008);
   Beta->SetBinError(51,7.416198);
   Beta->SetBinError(52,5.09902);
   Beta->SetBinError(53,4.472136);
   Beta->SetBinError(54,3.741657);
   Beta->SetBinError(55,7.211103);
   Beta->SetBinError(56,4.472136);
   Beta->SetBinError(57,6);
   Beta->SetBinError(58,4.123106);
   Beta->SetBinError(59,4.123106);
   Beta->SetBinError(60,4.242641);
   Beta->SetBinError(61,3.741657);
   Beta->SetBinError(62,4.123106);
   Beta->SetBinError(63,4.795832);
   Beta->SetBinError(64,3.464102);
   Beta->SetBinError(65,3.162278);
   Beta->SetBinError(66,4.123106);
   Beta->SetBinError(67,3.741657);
   Beta->SetBinError(68,4.242641);
   Beta->SetBinError(69,3.162278);
   Beta->SetBinError(70,3.162278);
   Beta->SetBinError(71,3.741657);
   Beta->SetBinError(72,2.645751);
   Beta->SetBinError(73,2.236068);
   Beta->SetBinError(74,2.828427);
   Beta->SetBinError(75,2);
   Beta->SetBinError(76,2);
   Beta->SetBinError(77,3.605551);
   Beta->SetBinError(78,2.828427);
   Beta->SetBinError(79,2.236068);
   Beta->SetBinError(80,2.44949);
   Beta->SetBinError(81,2.828427);
   Beta->SetBinError(82,2);
   Beta->SetBinError(83,1);
   Beta->SetBinError(84,2.645751);
   Beta->SetBinError(85,1.732051);
   Beta->SetBinError(86,2);
   Beta->SetBinError(87,1.732051);
   Beta->SetBinError(88,2.44949);
   Beta->SetBinError(90,1);
   Beta->SetBinError(91,2.828427);
   Beta->SetBinError(92,2.645751);
   Beta->SetBinError(93,1.414214);
   Beta->SetBinError(94,2);
   Beta->SetBinError(95,1.732051);
   Beta->SetBinError(96,1.414214);
   Beta->SetBinError(97,2.236068);
   Beta->SetBinError(98,1.414214);
   Beta->SetBinError(99,1.414214);
   Beta->SetBinError(100,2);
   Beta->SetBinError(101,10.90871);
   Beta->SetEntries(1788);
   
   TPaveStats *ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   TText *AText = ptstats->AddText("Beta");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 1788   ");
   AText = ptstats->AddText("Mean  =  263.9");
   AText = ptstats->AddText("Std Dev   =  278.9");
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
   ToF_20mm_1->Modified();
   ToF_20mm->cd();
  
// ------------>Primitives in pad: ToF_20mm_2
   TPad *ToF_20mm_2 = new TPad("ToF_20mm_2", "ToF_20mm_2",0.3433333,0.01,0.6566667,0.99);
   ToF_20mm_2->Draw();
   ToF_20mm_2->cd();
   ToF_20mm_2->Range(-60,-1.413758,340,4.456026);
   ToF_20mm_2->SetFillColor(0);
   ToF_20mm_2->SetBorderMode(0);
   ToF_20mm_2->SetBorderSize(2);
   ToF_20mm_2->SetLogy();
   ToF_20mm_2->SetGridx();
   ToF_20mm_2->SetGridy();
   ToF_20mm_2->SetLeftMargin(0.15);
   ToF_20mm_2->SetBottomMargin(0.15);
   ToF_20mm_2->SetFrameBorderMode(0);
   ToF_20mm_2->SetFrameBorderMode(0);
   
   TH1D *Gama = new TH1D("Gama","Gama",50,0,300);
   Gama->SetBinContent(1,1907);
   Gama->SetBinContent(2,2729);
   Gama->SetBinContent(3,2129);
   Gama->SetBinContent(4,1587);
   Gama->SetBinContent(5,1038);
   Gama->SetBinContent(6,925);
   Gama->SetBinContent(7,659);
   Gama->SetBinContent(8,653);
   Gama->SetBinContent(9,576);
   Gama->SetBinContent(10,521);
   Gama->SetBinContent(11,460);
   Gama->SetBinContent(12,437);
   Gama->SetBinContent(13,398);
   Gama->SetBinContent(14,338);
   Gama->SetBinContent(15,281);
   Gama->SetBinContent(16,262);
   Gama->SetBinContent(17,220);
   Gama->SetBinContent(18,168);
   Gama->SetBinContent(19,177);
   Gama->SetBinContent(20,115);
   Gama->SetBinContent(21,99);
   Gama->SetBinContent(22,102);
   Gama->SetBinContent(23,69);
   Gama->SetBinContent(24,44);
   Gama->SetBinContent(25,50);
   Gama->SetBinContent(26,39);
   Gama->SetBinContent(27,31);
   Gama->SetBinContent(28,28);
   Gama->SetBinContent(29,19);
   Gama->SetBinContent(30,17);
   Gama->SetBinContent(31,12);
   Gama->SetBinContent(32,12);
   Gama->SetBinContent(33,8);
   Gama->SetBinContent(34,2);
   Gama->SetBinContent(36,6);
   Gama->SetBinContent(38,2);
   Gama->SetBinContent(39,1);
   Gama->SetBinContent(40,3);
   Gama->SetBinContent(41,1);
   Gama->SetBinContent(47,1);
   Gama->SetBinContent(48,2);
   Gama->SetBinContent(51,17);
   Gama->SetBinError(1,1349.551);
   Gama->SetBinError(2,1174.901);
   Gama->SetBinError(3,870.1868);
   Gama->SetBinError(4,651.41);
   Gama->SetBinError(5,435.1873);
   Gama->SetBinError(6,388.7711);
   Gama->SetBinError(7,271.943);
   Gama->SetBinError(8,273.1575);
   Gama->SetBinError(9,240.6034);
   Gama->SetBinError(10,217.2901);
   Gama->SetBinError(11,192.7226);
   Gama->SetBinError(12,184.1494);
   Gama->SetBinError(13,164.8878);
   Gama->SetBinError(14,139.9571);
   Gama->SetBinError(15,116.6748);
   Gama->SetBinError(16,107.7219);
   Gama->SetBinError(17,89.97778);
   Gama->SetBinError(18,70.61161);
   Gama->SetBinError(19,72.38094);
   Gama->SetBinError(20,48.17676);
   Gama->SetBinError(21,40.6325);
   Gama->SetBinError(22,42.23742);
   Gama->SetBinError(23,29);
   Gama->SetBinError(24,18.70829);
   Gama->SetBinError(25,21.63331);
   Gama->SetBinError(26,17.4069);
   Gama->SetBinError(27,13.22876);
   Gama->SetBinError(28,13.2665);
   Gama->SetBinError(29,8.544004);
   Gama->SetBinError(30,8.774964);
   Gama->SetBinError(31,6.164414);
   Gama->SetBinError(32,6.324555);
   Gama->SetBinError(33,4.242641);
   Gama->SetBinError(34,1.414214);
   Gama->SetBinError(36,2.828427);
   Gama->SetBinError(38,1.414214);
   Gama->SetBinError(39,1);
   Gama->SetBinError(40,2.236068);
   Gama->SetBinError(41,1);
   Gama->SetBinError(47,1);
   Gama->SetBinError(48,1.414214);
   Gama->SetBinError(51,4.123106);
   Gama->SetEntries(223);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Gama");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 223    ");
   AText = ptstats->AddText("Mean  =  35.92");
   AText = ptstats->AddText("Std Dev   =  35.03");
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
   ToF_20mm_2->Modified();
   ToF_20mm->cd();
  
// ------------>Primitives in pad: ToF_20mm_3
   TPad *ToF_20mm_3 = new TPad("ToF_20mm_3", "ToF_20mm_3",0.6766667,0.01,0.99,0.99);
   ToF_20mm_3->Draw();
   ToF_20mm_3->cd();
   ToF_20mm_3->Range(-3000,-1.097557,17000,2.66422);
   ToF_20mm_3->SetFillColor(0);
   ToF_20mm_3->SetBorderMode(0);
   ToF_20mm_3->SetBorderSize(2);
   ToF_20mm_3->SetLogy();
   ToF_20mm_3->SetGridx();
   ToF_20mm_3->SetGridy();
   ToF_20mm_3->SetLeftMargin(0.15);
   ToF_20mm_3->SetBottomMargin(0.15);
   ToF_20mm_3->SetFrameBorderMode(0);
   ToF_20mm_3->SetFrameBorderMode(0);
   
   TH1D *Alpha = new TH1D("Alpha","Alpha",100,0,15000);
   Alpha->SetBinContent(1,1);
   Alpha->SetBinContent(2,15);
   Alpha->SetBinContent(3,22);
   Alpha->SetBinContent(4,34);
   Alpha->SetBinContent(5,58);
   Alpha->SetBinContent(6,57);
   Alpha->SetBinContent(7,79);
   Alpha->SetBinContent(8,91);
   Alpha->SetBinContent(9,86);
   Alpha->SetBinContent(10,58);
   Alpha->SetBinContent(11,54);
   Alpha->SetBinContent(12,40);
   Alpha->SetBinContent(13,35);
   Alpha->SetBinContent(14,39);
   Alpha->SetBinContent(15,22);
   Alpha->SetBinContent(16,19);
   Alpha->SetBinContent(17,25);
   Alpha->SetBinContent(18,18);
   Alpha->SetBinContent(19,14);
   Alpha->SetBinContent(20,13);
   Alpha->SetBinContent(21,8);
   Alpha->SetBinContent(22,5);
   Alpha->SetBinContent(23,10);
   Alpha->SetBinContent(24,13);
   Alpha->SetBinContent(25,14);
   Alpha->SetBinContent(26,8);
   Alpha->SetBinContent(27,6);
   Alpha->SetBinContent(28,5);
   Alpha->SetBinContent(29,3);
   Alpha->SetBinContent(30,1);
   Alpha->SetBinContent(31,5);
   Alpha->SetBinContent(32,6);
   Alpha->SetBinContent(33,7);
   Alpha->SetBinContent(34,7);
   Alpha->SetBinContent(35,2);
   Alpha->SetBinContent(36,1);
   Alpha->SetBinContent(37,5);
   Alpha->SetBinContent(38,4);
   Alpha->SetBinContent(39,3);
   Alpha->SetBinContent(40,1);
   Alpha->SetBinContent(41,3);
   Alpha->SetBinContent(42,1);
   Alpha->SetBinContent(43,3);
   Alpha->SetBinContent(44,2);
   Alpha->SetBinContent(45,1);
   Alpha->SetBinContent(47,2);
   Alpha->SetBinContent(48,1);
   Alpha->SetBinContent(49,3);
   Alpha->SetBinContent(51,1);
   Alpha->SetBinContent(52,3);
   Alpha->SetBinContent(54,1);
   Alpha->SetBinContent(59,2);
   Alpha->SetBinContent(60,1);
   Alpha->SetBinContent(61,2);
   Alpha->SetBinContent(62,1);
   Alpha->SetBinContent(63,1);
   Alpha->SetBinContent(71,1);
   Alpha->SetBinContent(72,1);
   Alpha->SetBinContent(75,1);
   Alpha->SetBinContent(76,1);
   Alpha->SetBinContent(79,1);
   Alpha->SetBinContent(90,1);
   Alpha->SetBinContent(100,1);
   Alpha->SetBinError(1,1);
   Alpha->SetBinError(2,4.123106);
   Alpha->SetBinError(3,4.898979);
   Alpha->SetBinError(4,6.480741);
   Alpha->SetBinError(5,8.944272);
   Alpha->SetBinError(6,9.433981);
   Alpha->SetBinError(7,13);
   Alpha->SetBinError(8,11.44552);
   Alpha->SetBinError(9,11.40175);
   Alpha->SetBinError(10,9.797959);
   Alpha->SetBinError(11,8.831761);
   Alpha->SetBinError(12,7.071068);
   Alpha->SetBinError(13,6.244998);
   Alpha->SetBinError(14,7.141428);
   Alpha->SetBinError(15,4.690416);
   Alpha->SetBinError(16,5);
   Alpha->SetBinError(17,6.557439);
   Alpha->SetBinError(18,4.472136);
   Alpha->SetBinError(19,4.242641);
   Alpha->SetBinError(20,3.605551);
   Alpha->SetBinError(21,2.828427);
   Alpha->SetBinError(22,2.236068);
   Alpha->SetBinError(23,3.162278);
   Alpha->SetBinError(24,3.605551);
   Alpha->SetBinError(25,4);
   Alpha->SetBinError(26,2.828427);
   Alpha->SetBinError(27,2.44949);
   Alpha->SetBinError(28,2.236068);
   Alpha->SetBinError(29,1.732051);
   Alpha->SetBinError(30,1);
   Alpha->SetBinError(31,2.236068);
   Alpha->SetBinError(32,2.44949);
   Alpha->SetBinError(33,2.645751);
   Alpha->SetBinError(34,3);
   Alpha->SetBinError(35,1.414214);
   Alpha->SetBinError(36,1);
   Alpha->SetBinError(37,2.236068);
   Alpha->SetBinError(38,2);
   Alpha->SetBinError(39,1.732051);
   Alpha->SetBinError(40,1);
   Alpha->SetBinError(41,1.732051);
   Alpha->SetBinError(42,1);
   Alpha->SetBinError(43,1.732051);
   Alpha->SetBinError(44,1.414214);
   Alpha->SetBinError(45,1);
   Alpha->SetBinError(47,1.414214);
   Alpha->SetBinError(48,1);
   Alpha->SetBinError(49,1.732051);
   Alpha->SetBinError(51,1);
   Alpha->SetBinError(52,1.732051);
   Alpha->SetBinError(54,1);
   Alpha->SetBinError(59,1.414214);
   Alpha->SetBinError(60,1);
   Alpha->SetBinError(61,1.414214);
   Alpha->SetBinError(62,1);
   Alpha->SetBinError(63,1);
   Alpha->SetBinError(71,1);
   Alpha->SetBinError(72,1);
   Alpha->SetBinError(75,1);
   Alpha->SetBinError(76,1);
   Alpha->SetBinError(79,1);
   Alpha->SetBinError(90,1);
   Alpha->SetBinError(100,1);
   Alpha->SetEntries(787);
   
   ptstats = new TPaveStats(0.78,0.775,0.98,0.935,"brNDC");
   ptstats->SetName("stats");
   ptstats->SetBorderSize(1);
   ptstats->SetFillColor(0);
   ptstats->SetTextAlign(12);
   ptstats->SetTextFont(42);
   AText = ptstats->AddText("Alpha");
   AText->SetTextSize(0.0368);
   AText = ptstats->AddText("Entries = 787    ");
   AText = ptstats->AddText("Mean  =   1968");
   AText = ptstats->AddText("Std Dev   =   1734");
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
   ToF_20mm_3->Modified();
   ToF_20mm->cd();
   ToF_20mm->Modified();
   ToF_20mm->cd();
   ToF_20mm->SetSelected(ToF_20mm);
}
