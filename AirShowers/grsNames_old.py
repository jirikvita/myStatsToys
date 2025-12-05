#!/usr/bin/python


def getGrsNames(generator):
    gfilenames = {

        # protons:
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0.root' : ROOT.kBlue,
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0.root' : ROOT.kBlue + 1,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EMonly1p5lengthsCut_p.root'  : ROOT.kAzure+1,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM_and_had_1p5lengthsCut_p.root' : ROOT.kMagenta+3,
        
        # Fe:
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_A56.root' : ROOT.kBlue + 1,

        # New physics, Z' of 100 GeV:
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_0.10.root' : ROOT.kCyan,
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_ee_xsectFrac_1.00.root' : ROOT.kCyan,
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_mumu_xsectFrac_0.10.root' : ROOT.kMagenta,
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_mumu_xsectFrac_1.00.root' : ROOT.kMagenta,
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_pipi_xsectFrac_0.10.root' : ROOT.kYellow,
        #f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_Zprime_100.0_Gamma_10.0_mode_pipi_xsectFrac_1.00.root' : ROOT.kYellow,
        #f'graphs_{generator}_primaryEl_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0.root' : ROOT.kWhite,

        # various EM showers with exp penetration truncated and 1--5 sigma:
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM1lengthsCut_e.root' : ROOT.kGray,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM1p25lengthsCut_e.root' : ROOT.kGray+1,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM1p5lengthsCut_e.root' : ROOT.kGray+2,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM2lengthsCut_e.root' : ROOT.kMagenta,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM3lengthsCut_e.root' : ROOT.kTeal,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM4lengthsCut_e.root' : ROOT.kGreen,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM5lengthsCut_e.root' : ROOT.kYellow,
        f'graphs_{generator}_Inel_0.55_sigmaInel_0.2_C_120.0_Csigma_30.0_EM999lengthsCut_e.root' : ROOT.kPink,
        
    }
    return gfilenames
