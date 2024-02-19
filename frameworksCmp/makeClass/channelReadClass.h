//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Fri Feb  2 09:54:53 2024 by ROOT version 6.24/06
// from TTree PbGlass/
// found on file: output/ntuple_000409.root
//////////////////////////////////////////////////////////

#ifndef channelReadClass_h
#define channelReadClass_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class channelReadClass {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

  const int MaxNpeaks = 100;
  
   // Declaration of leaf types
   Double_t        Pedestal;
   Double_t        PedestalSigma;
   Int_t           nPeaks;
   Double_t        PeakVoltage[MaxNpeaks];   //[nPeaks]
   Double_t        PeakTime[MaxNpeaks];   //[nPeaks]
   Double_t        SignalTime[MaxNpeaks];   //[nPeaks]
   Double_t        IntCharge[MaxNpeaks];   //[nPeaks]
   UInt_t          timeStamp;
   UInt_t          triggerTime;

   // List of branches
   TBranch        *b_Pedestal;   //!
   TBranch        *b_PedestalSigma;   //!
   TBranch        *b_nPeaks;   //!
   TBranch        *b_PeakVoltage;   //!
   TBranch        *b_PeakTime;   //!
   TBranch        *b_SignalTime;   //!
   TBranch        *b_IntCharge;   //!
   TBranch        *b_timeStamp;   //!
   TBranch        *b_triggerTime;   //!

   channelReadClass(TTree *tree=0);
   virtual ~channelReadClass();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef channelReadClass_cxx
channelReadClass::channelReadClass(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("output/ntuple_000409.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("output/ntuple_000409.root");
      }
      f->GetObject("PbGlass",tree);

   }
   Init(tree);
}

channelReadClass::~channelReadClass()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t channelReadClass::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t channelReadClass::LoadTree(Long64_t entry)
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

void channelReadClass::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("Pedestal", &Pedestal, &b_Pedestal);
   fChain->SetBranchAddress("PedestalSigma", &PedestalSigma, &b_PedestalSigma);
   fChain->SetBranchAddress("nPeaks", &nPeaks, &b_nPeaks);
   fChain->SetBranchAddress("PeakVoltage", PeakVoltage, &b_PeakVoltage);
   fChain->SetBranchAddress("PeakTime", PeakTime, &b_PeakTime);
   fChain->SetBranchAddress("SignalTime", SignalTime, &b_SignalTime);
   fChain->SetBranchAddress("IntCharge", IntCharge, &b_IntCharge);
   fChain->SetBranchAddress("timeStamp", &timeStamp, &b_timeStamp);
   fChain->SetBranchAddress("triggerTime", &triggerTime, &b_triggerTime);
   Notify();
   fChain -> AddFriend("ACT2L");
}

Bool_t channelReadClass::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void channelReadClass::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t channelReadClass::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef channelReadClass_cxx
