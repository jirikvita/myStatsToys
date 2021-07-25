#include "weights.h"

#include <string>
#include <vector>
#include <iostream>

#include "TH1D.h"
#include "TCanvas.h"
#include "TFile.h"

using std::cout;
using std::cerr;
using std::endl;

// usage: root -b -q -l 'draw.c+("LeadJetPt")'
// usage: root -l 'draw.c+("LeadJetPt")'


//void draw(TString hname = "xi"){
  // void draw(TString hname = "DijetMass"){
void draw(TString hname = "LeadJetPt", int SampleTag = 0){

	std::vector<std::vector<std::string> > loadedFile = loadDataFile("jet_samples_cross_sections.v1.txt", 4);

	std::vector<TH1D*> hists;

	
	const int NfilesDPE = 4;
	TString TagDPE = "DPE";
	TString FileNamesDPE[NfilesDPE] = {"998001.Herwigpp_DPE_H12007_jetjet_JZ0",
					   "998002.Herwigpp_DPE_H12007_jetjet_JZ1",
					   "998003.Herwigpp_DPE_H12007_jetjet_JZ2",
					   "998004.Herwigpp_DPE_H12007_jetjet_JZ3"};
	const int NfilesEE = 6;
	TString TagEE = "EE";
	TString FileNamesEE[NfilesEE] = {"999001.Herwigpp_EE3CTEQ6L1_jetjet_JZ0", 
					 "999002.Herwigpp_EE3CTEQ6L1_jetjet_JZ1", 
					 "999003.Herwigpp_EE3CTEQ6L1_jetjet_JZ2", 
					 "999004.Herwigpp_EE3CTEQ6L1_jetjet_JZ3", 
					 "999005.Herwigpp_EE3CTEQ6L1_jetjet_JZ4", 
					 "999006.Herwigpp_EE3CTEQ6L1_jetjet_JZ5" };
	
	const int NfilesSDN = 4;
	TString TagSDN = "SDN";
	TString FileNamesSDN[NfilesSDN] = {"996001.Herwigpp_SDN_H12007_jetjet_JZ0", 
					"996002.Herwigpp_SDN_H12007_jetjet_JZ1",  
					"996003.Herwigpp_SDN_H12007_jetjet_JZ2",
					"996004.Herwigpp_SDN_H12007_jetjet_JZ3"};

	const int NfilesSDP = 4;
	TString TagSDP = "SDP";
	TString FileNamesSDP[NfilesSDP] = {"997001.Herwigpp_SDP_H12007_jetjet_JZ0",
					   "997002.Herwigpp_SDP_H12007_jetjet_JZ1",
					   "997003.Herwigpp_SDP_H12007_jetjet_JZ2",
					   "997004.Herwigpp_SDP_H12007_jetjet_JZ3"};


	TString Tag;
	TString *pFileNames = 0;
	int Nfiles = 0;
	switch(SampleTag) {
	case 0:
	  Tag = TagDPE;
	  pFileNames = (TString*)&FileNamesDPE[0];
	  Nfiles = NfilesDPE;
	  break;
	case 1:
	  Tag = TagEE;
	  pFileNames = (TString*)&FileNamesEE[0];
	  Nfiles = NfilesEE;
	  break;
	case 2:
	  Tag = TagSDN;
	  pFileNames = (TString*)&FileNamesSDN[0];
	  Nfiles = NfilesSDN;
	  break;
	case 3:
	  Tag = TagSDP;
	  pFileNames = (TString*)&FileNamesSDP[0];
	  Nfiles = NfilesSDP;
	  break;  
	}

	for (int ifile = 0; ifile < Nfiles; ++ifile) {
	  TFile *file = new TFile(pFileNames[ifile] + ".root", "read");
	  cout << "Opening file " << pFileNames[ifile].Data() << endl;
	  TH1D *hist = 0;
	  TH1D *normhist = 0;
	  if (file) {
	    hist = (TH1D*) file -> Get(hname); 
	    normhist = (TH1D*) file -> Get("njets"); 
	    if (hist) {
	      double entries  = 0.;
	      if (normhist)
		entries = hist->GetEntries();
	      cout << "Entries: " << entries << endl;
	      double weight = getWeight(pFileNames[ifile].Data(), loadedFile);
	      if (entries > 0.)
		hist->Scale(weight/entries); // APPROXIMATION!!!
	      hists.push_back(hist);
	    } else {
	      cerr << "    ERROR getting histo pointer!" << endl;
	    }
	  } else {
	    cerr << "  ERROR getting file pointer!" << endl;
	  }
	} // files

	TH1D *h_sum = 0;

	if (hists.size() > 0) {

	  h_sum = (TH1D*) hists[0]->Clone(Form("Summed_%s", hists[0]->GetName()));
	  h_sum->Reset();
	  h_sum->Sumw2();
	  for (int ih = 0; ih < hists.size(); ++ih) {
	    h_sum->Add(hists[ih]);
	  }
	  
	} else {
	  cerr << "Zero hists list!" << endl;
	}
       
	TCanvas *can = new TCanvas(Tag, Tag);
	can -> cd();
	can -> SetLogy(1);

	if (h_sum) {
	  h_sum->SetMarkerColor(1);
	  h_sum->SetMarkerSize(1);
	  h_sum->SetMarkerStyle(20);

	  h_sum->SetTitle(TString(h_sum -> GetTitle()) + ", " + Tag);
	  
	  // h_sum -> SetMinimum(hists[hists.size()-1]->GetMinimum());
	  if (TString(h_sum -> GetName()).Contains("Eta"))
	    h_sum -> SetMinimum(1.e-6);
	  cout << "Drawing sum..." << endl;
	  h_sum->Draw("hist");
	  for (int ih = 0; ih < hists.size(); ++ih) {
	    cout << "Drawing ihisto=" << ih << endl;
	    hists[ih]->SetLineColor(1+ih);
	    hists[ih]->Draw("hist same");
	  }
	  cout << "Redrawing sum..." << endl;
	  h_sum->Draw("e1same");
	}

	can -> Print(hname + Tag + ".eps");
	can -> Print(hname + Tag + ".png");

}
