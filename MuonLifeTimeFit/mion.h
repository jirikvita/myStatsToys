//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Nov 30 13:37:46 2016 by ROOT version 5.34/30
// from TTree Data/Osciloscope data
// found on file: MU.root
//////////////////////////////////////////////////////////

#ifndef mion_h
#define mion_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include <vector>

// Fixed size dimensions of array or collections stored in the TTree if any.

class mion {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           evid;
   Double_t        tp1;
   Double_t        tp2;
   Double_t        tp3;
   Double_t        tp4;
   Bool_t          idv1;
   Bool_t          idv2;
   Bool_t          idv3;
   Bool_t          idv4;
   Double_t        esl1;
   Double_t        esl2;
   Double_t        esl3;
   Double_t        esl4;
   Double_t        pl1;
   Double_t        pl2;
   Double_t        pl3;
   Double_t        pl4;
   Double_t        pt1;
   Double_t        pt2;
   Double_t        pt3;
   Double_t        pt4;
   Double_t        a1;
   Double_t        a2;
   Double_t        a3;
   Double_t        a4;
   vector<double>  *vt1;
   vector<double>  *vt2;
   vector<double>  *vt3;
   vector<double>  *vt4;
   vector<double>  *vy1;
   vector<double>  *vy2;
   vector<double>  *vy3;
   vector<double>  *vy4;

   // List of branches
   TBranch        *b_evid;   //!
   TBranch        *b_tp1;   //!
   TBranch        *b_tp2;   //!
   TBranch        *b_tp3;   //!
   TBranch        *b_tp4;   //!
   TBranch        *b_idv1;   //!
   TBranch        *b_idv2;   //!
   TBranch        *b_idv3;   //!
   TBranch        *b_idv4;   //!
   TBranch        *b_esl1;   //!
   TBranch        *b_esl2;   //!
   TBranch        *b_esl3;   //!
   TBranch        *b_esl4;   //!
   TBranch        *b_pl1;   //!
   TBranch        *b_pl2;   //!
   TBranch        *b_pl3;   //!
   TBranch        *b_pl4;   //!
   TBranch        *b_pt1;   //!
   TBranch        *b_pt2;   //!
   TBranch        *b_pt3;   //!
   TBranch        *b_pt4;   //!
   TBranch        *b_a1;   //!
   TBranch        *b_a2;   //!
   TBranch        *b_a3;   //!
   TBranch        *b_a4;   //!
   TBranch        *b_vt1;   //!
   TBranch        *b_vt2;   //!
   TBranch        *b_vt3;   //!
   TBranch        *b_vt4;   //!
   TBranch        *b_vy1;   //!
   TBranch        *b_vy2;   //!
   TBranch        *b_vy3;   //!
   TBranch        *b_vy4;   //!

   mion(TTree *tree=0);
   virtual ~mion();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef mion_cxx
mion::mion(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("MU.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("MU.root");
      }
      f->GetObject("Data",tree);

   }
   Init(tree);
}

mion::~mion()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t mion::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t mion::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void mion::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   vt1 = 0;
   vt2 = 0;
   vt3 = 0;
   vt4 = 0;
   vy1 = 0;
   vy2 = 0;
   vy3 = 0;
   vy4 = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("evid", &evid, &b_evid);
   fChain->SetBranchAddress("tp1", &tp1, &b_tp1);
   fChain->SetBranchAddress("tp2", &tp2, &b_tp2);
   fChain->SetBranchAddress("tp3", &tp3, &b_tp3);
   fChain->SetBranchAddress("tp4", &tp4, &b_tp4);
   fChain->SetBranchAddress("idv1", &idv1, &b_idv1);
   fChain->SetBranchAddress("idv2", &idv2, &b_idv2);
   fChain->SetBranchAddress("idv3", &idv3, &b_idv3);
   fChain->SetBranchAddress("idv4", &idv4, &b_idv4);
   fChain->SetBranchAddress("esl1", &esl1, &b_esl1);
   fChain->SetBranchAddress("esl2", &esl2, &b_esl2);
   fChain->SetBranchAddress("esl3", &esl3, &b_esl3);
   fChain->SetBranchAddress("esl4", &esl4, &b_esl4);
   fChain->SetBranchAddress("pl1", &pl1, &b_pl1);
   fChain->SetBranchAddress("pl2", &pl2, &b_pl2);
   fChain->SetBranchAddress("pl3", &pl3, &b_pl3);
   fChain->SetBranchAddress("pl4", &pl4, &b_pl4);
   fChain->SetBranchAddress("pt1", &pt1, &b_pt1);
   fChain->SetBranchAddress("pt2", &pt2, &b_pt2);
   fChain->SetBranchAddress("pt3", &pt3, &b_pt3);
   fChain->SetBranchAddress("pt4", &pt4, &b_pt4);
   fChain->SetBranchAddress("a1", &a1, &b_a1);
   fChain->SetBranchAddress("a2", &a2, &b_a2);
   fChain->SetBranchAddress("a3", &a3, &b_a3);
   fChain->SetBranchAddress("a4", &a4, &b_a4);
   fChain->SetBranchAddress("vt1", &vt1, &b_vt1);
   fChain->SetBranchAddress("vt2", &vt2, &b_vt2);
   fChain->SetBranchAddress("vt3", &vt3, &b_vt3);
   fChain->SetBranchAddress("vt4", &vt4, &b_vt4);
   fChain->SetBranchAddress("vy1", &vy1, &b_vy1);
   fChain->SetBranchAddress("vy2", &vy2, &b_vy2);
   fChain->SetBranchAddress("vy3", &vy3, &b_vy3);
   fChain->SetBranchAddress("vy4", &vy4, &b_vy4);
   Notify();
}

Bool_t mion::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void mion::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t mion::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef mion_cxx
