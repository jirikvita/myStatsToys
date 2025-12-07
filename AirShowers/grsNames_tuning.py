#!/usr/bin/python


import ROOT

dtag = '_tuning'
grdir = 'graphs_bugStillLeadingProtonInNewPhysics/'
#'graphs_Exp_fractions/'

reffilename = 'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0.root'

def getGrsNames(generator):
    gfilenames = {

        # EM:
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.0_mnlHad1.5_primaryE_e.root' : ROOT.kWhite,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.25_mnlHad1.5_primaryE_e.root' : ROOT.kWhite,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad1.5_primaryE_e.root' : ROOT.kWhite,

        # Fe:
        #f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.25_mnlHad1.5_primaryFe56_A56.root' : ROOT.kBlue,
        #f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10_Csigma_2_mnlEM1.0_mnlHad1.5_primaryFe56_A56.root' : ROOT.kBlue,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_FeA56.root' : ROOT.kBlue,

        # protons tuning:
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0.root' : ROOT.kBlue,
        # candle plot...?;)

        # max lenghth X0: 1.0
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.0.root' : ROOT.kCyan, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.0_mnlHad1.5.root' : ROOT.kCyan, 

        # max lenghth X0: 1.5
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.0.root' : ROOT.kMagenta, 
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.5_mnlHad1.5.root' : ROOT.kMagenta,

        
        # max lenghth X0: 1.125
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_10.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_12.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kGreen,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_8.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kGreen,

        # max lenghth X0: 1.125, small Nch
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.45_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.4_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.55_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.5_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_2.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_4.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad1.5.root' : ROOT.kYellow,
        f'graphs_EPOS_Inel_0.6_sigmaInel_0.2_C_6.0_Csigma_2.0_mnlEM1.125_mnlHad999.0.root' : ROOT.kYellow,

        
    }
    
    return gfilenames
