#include <TStyle.h>
#include <TROOT.h>

void setup()
{

 TStyle *plain  = new TStyle("Plain","Plain Style (no colors/fill areas)");
  
 //some methods doesn't work in plain, but work called for gStyle...happy ROOTing!!!

  plain->SetCanvasBorderMode(0);
  plain->SetPadBorderMode(0);
  plain->SetPadColor(0);
  plain->SetCanvasColor(0);
  //  plain->SetTitleColor(0);
  plain->SetStatColor(0);
  plain->SetOptFit(1111);

 
  //  plain->SetHistLineWidth(2);
  //  plain->SetHistLineStyle(0);
  //  plain->SetStatX(0.1);
  
  //plain->SetTitleXSize(0.06);
  //plain->SetTitleYSize(0.06);
  //plain->SetTitleFontSize(0.06);
  //plain->SetTitleOffset(0.5);

  //  plain->SetStatW(0.4);//0.19
  //plain->SetStatH(0.5);//0.1

   //plain->SetPadGridX(true);
  //plain->SetPadGridY(true);

  gROOT->SetStyle("Plain");


  //gStyle->SetOptStat(111111);//all but bins integral
  //gStyle->SetOptStat(1111);//entries,mean,rms, name
  gStyle->SetOptStat(1110);//entries,mean,rms, NO name!
  
  //gStyle->SetOptFit(1100);

  //gStyle ->SetStatFontSize(0.03);
  gStyle->SetStatW(0.19);//0.19
  gStyle->SetStatH(0.2);//0.25
  gStyle->SetStatX(0.88);
  gStyle->SetStatY(0.9);//0.99
  gStyle->SetStatFontSize(0.08);

  gStyle->SetPadRightMargin(0.12);//0.02 fot TH1F?!
  gStyle->SetPadLeftMargin(0.15);//0.1
  gStyle->SetPadBottomMargin(0.16);//0.1

  // !!! aaa
  //  gStyle->SetPadGridX(true);
  // gStyle->SetPadGridY(true);

  //histogram axis titles
  gStyle->SetTitleXSize(0.06);
  gStyle->SetTitleYSize(0.06);
 
  gStyle->SetTitleFontSize(0.05);
  gStyle->SetTitleOffset(0.8,"X");
  gStyle->SetTitleOffset(0.8,"Y");
  
  //title of the histogram
  gStyle->SetTitleH(0.09);
  gStyle->SetTitleW(0.73);//0.6
  gStyle->SetTitleX(0.15);
  gStyle->SetTitleY(0.99);
  gStyle->SetPalette(1);
  gStyle->SetFillColor(10);
  gStyle->SetFrameBorderMode(0);

  gROOT->ForceStyle();
}
