#!/usr/bin/python


import ROOT

def getGrsNames(generator):
    gfilenames = {

        # EM:
        #f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.0_mnlHad1.5_primaryE_e.root' : ROOT.kWhite,
        #f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.25_mnlHad1.5_primaryE_e.root' : ROOT.kWhite,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad1.5_primaryE_e.root' : ROOT.kWhite,

        
        # New physics: Zprime 1000GeV
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_1000.0_Gamma_100.0_mode_ee_xsectFrac_0.25.root' : ROOT.k,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_1000.0_Gamma_100.0_mode_ee_xsectFrac_1.00.root' : ROOT.kTeal,
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_1000.0_Gamma_100.0_mode_mumu_xsectFrac_0.25.root' : ROOT.k,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_1000.0_Gamma_100.0_mode_mumu_xsectFrac_1.00.root' : ROOT.kMagenta,
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_1000.0_Gamma_100.0_mode_pipi_xsectFrac_0.25.root' : ROOT.k,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_1000.0_Gamma_100.0_mode_pipi_xsectFrac_1.00.root' : ROOT.kYellow,

        # p:
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0.root' : ROOT.kBlue,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_testNoNewPhysWithNewPhysArea.root' : ROOT.kBlue,
        # Fe:
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_FeA56.root' : ROOT.kBlue,


        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_testNoNewPhysWithNewPhysArea.root' : ROOT.kGreen,

        
        # New physics: Zprime 100GeV
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_0.25.root' : ROOT.k,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_1.00.root' : ROOT.kTeal,
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_mumu_xsectFrac_0.25.root' : ROOT.k,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_mumu_xsectFrac_1.00.root' : ROOT.kMagenta,
        #f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_pipi_xsectFrac_0.25.root' : ROOT.k,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_Zprime_100.0_Gamma_10.0_mode_pipi_xsectFrac_1.00.root' : ROOT.kYellow,
    
        
    }
    
    return gfilenames
