#define mion_cxx
#include "mion.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TF1.h>

void mion::Loop()
{
//   In a ROOT session, you can do:
//      Root > .L mion.C
//      Root > mion t
//      Root > t.GetEntry(12); // Fill t data members with entry number 12
//      Root > t.Show();       // Show values of entry 12
//      Root > t.Show(16);     // Read and show values of entry 16
//      Root > t.Loop();       // Loop on all entries
//

	TH1D *time20 = new TH1D("time20","Muon lifetime;Time [];Events [-]", 20, 0, 5000);
	TH1D *time10 = new TH1D("time10","Muon lifetime;Time [];Events [-]", 10, 0, 5000);
	TH1D *time15 = new TH1D("time15","Muon lifetime;Time [];Events [-]", 15, 0, 5000);
	TH1D *time25 = new TH1D("time25","Muon lifetime;Time [];Events [-]", 25, 0, 5000);
	TH1D *time30 = new TH1D("time30","Muon lifetime;Time [];Events [-]", 30, 0, 5000);
	TH1D *time50 = new TH1D("time50","Muon lifetime;Time [ns];Events [-]", 50, 0, 500);

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

	if( abs(pt1) < 6000 && abs(pt1) > 20 ){
		time20->Fill(abs(pt1));
		time10->Fill(abs(pt1));
		time15->Fill(abs(pt1));
		time25->Fill(abs(pt1));
		time30->Fill(abs(pt1));
		time50->Fill(abs(pt1)/10.);
		}


   }
double f_from=400;
double f_to=4600;

TF1 *fit = new TF1("fit", "[0]*exp(-[1]*x)+[2]", 0, 5000);
TF1 *fit2 = new TF1("fit2", "[0]*exp(-[1]*x)-exp(-[2]*x)+[3]", 0, 5000);

gStyle->SetOptFit(1);
//gStyle->SetOptStat(0);

/*
fit->SetParameters(time30->GetBinContent(3), -1e-5, 50);
time30->SetMarkerStyle(20);
time30->SetLineColor(1);
time30->Fit("fit", "", "e1", f_from, f_to);
double x30=1./(fit->GetParError(1)+fit->GetParameter(1));
double y30=1./(fit->GetParameter(1)-fit->GetParError(1));
double delta30=abs((x30-y30)/2.);


fit->SetParameters(time25->GetBinContent(3), -1e-5, 50);
time25->SetMarkerStyle(20);
time25->SetLineColor(1);
time25->Fit("fit", "", "e1", f_from, f_to);
double x25=1./(fit->GetParError(1)+fit->GetParameter(1));
double y25=1./(fit->GetParameter(1)-fit->GetParError(1));
double delta25=abs((x25-y25)/2.);

fit->SetParameters(time15->GetBinContent(2), -1e-5, 50);
time15->SetMarkerStyle(20);
time15->SetLineColor(1);
time15->Fit("fit", "", "e1", f_from, f_to);
double x15=1./(fit->GetParError(1)+fit->GetParameter(1));
double y15=1./(fit->GetParameter(1)-fit->GetParError(1));
double delta15=abs((x25-y15)/2.);

fit->SetParameters(time10->GetBinContent(2), -1e-5, 50);
time10->SetMarkerStyle(20);
time10->SetLineColor(1);
time10->Fit("fit", "", "e1", f_from, f_to);
double x10=1./(fit->GetParError(1)+fit->GetParameter(1));
double y10=1./(fit->GetParameter(1)-fit->GetParError(1));
double delta10=abs((x10-y10)/2.);

fit->SetParameters(time20->GetBinContent(3), -1e-5, 50);
time20->SetMarkerStyle(20);
time20->SetLineColor(1);
time20->Fit("fit", "", "e1", f_from, f_to);
double x20=1./(fit->GetParError(1)+fit->GetParameter(1));
double y20=1./(fit->GetParameter(1)-fit->GetParError(1));
double delta20=abs((x20-y20)/2.);
//double time_value=(1./fit->GetParameter(1));

*/

fit->SetParameters(time50->GetBinContent(4), -1e-5, 50);
fit2->SetParameters(time50->GetBinContent(3), -1e-5, 1, 50);


time50->SetMarkerStyle(20);
time50->SetLineColor(1);

time50->Fit("fit", "same+", "+samee1", f_from/10., f_to/10.);

fit2->SetLineColor(4);
time50->Fit("fit2","same+", "+samee1", f_from/10., f_to/10.);

/*
double x50=1./(fit->GetParError(1)+fit->GetParameter(1));
double y50=1./(fit->GetParameter(1)-fit->GetParError(1));
double delta50=abs((x50-y50)/2.);
double time_value=(1./fit->GetParameter(1));
*/

cout << 1./fit2->GetParameter(1) << endl;
cout << 1./fit->GetParameter(1) << endl;


gStyle->SetErrorX(0.1);


gPad->SaveAs("Muon_fited_double.pdf");
gPad->SaveAs("Muon_fited_double.png");
gPad->SaveAs("Muon_fited_double.C");
gPad->SaveAs("Muon_fited_double.root");

/*
//cout << ((delta30+delta25+delta20+delta15+delta10)/5.) << endl;

cout.precision(5);

cout << "\n" << endl;
cout << time_value/100.;

cout.precision(4);

cout << " +- ";
cout << abs((x20-y20)/2000.);
cout << "(stat) +- ";
cout << abs((delta30+delta25+delta20+delta15+delta10)/10000.);
cout << "(syst) us" << endl;

cout.precision(5);

double G=sqrt((192*pow(3.14159,3))/(pow(0.105,5)*time_value/(100000000.*6.58*pow(10,-25))));
cout << "Fermi const." << endl;
cout << G << endl;

cout << "Closure test" << endl;
cout << ((192*pow(3.14159,3))/(pow(0.105,5)*pow(G,2)))*6.58*pow(10,-25)*1000000.;
cout << " us" << endl;


G=0.0000166378;
cout << "time with fermi table value" << endl;
cout << ((192*pow(3.14159,3))/(pow(0.105,5)*pow(G,2)))*6.58*pow(10,-25)*2000000.;
cout << " us" << endl;

cout << 1./fit->GetParameter(1)/1000.;
cout << " +- ";
cout << (x20-y20)/2000.;
cout << "us\n\n" << endl;
*/
}
