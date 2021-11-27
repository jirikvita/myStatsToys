#!/usr/bin/python


dirs = { '2DGauss' : './Gaus2D.py',
         #'ALFA_compatibility' : '',
         #'AlphaSpectSim' : '',
         'BinCovariance' : './Run.sh',
         'BMI' : 'make ; ./BMI_index',
         'centralLimitTheorem' : './cltCheck.py',
         'Classification' : 'Class.py',
         'Climate' : './ClimateChange.py',
         'ComparisonBias' : './DrawGraph.py',
         'Correlations' : './AlfaBetaGama.py',
         #'Examples' : '',
         'FitError' : 'root -l FitWithErrors.C++',
         'FitResiduals' : 'root -l FitResiduals.C++',
         #'Fitting' : '',
         'GenFunction' : './GenFunction.py',
         #'Gravity' : '',
         'Hypotheses' : './Hypotheses.py',
         #'JetAlgo' : '',
         'kernel' : './toyKernel.py',
         #'LhoodBinnedFit' : '', # just a tool
         'LhoodUnbinnedFit' : 'root -l LhoodNEventsFit.C++',
         'LinCorr' : './LinData.py',
         #'MCsamplesWeights' : '',
         #'MuonLifeTimeFit' : '',
         'PeakSim' : './PeakSim.py',
         #'PeakStatVerication' : './peaksSim.py',
         'PoissonAver' : './PoissonAver.py',
         'PragueMarathon2014' : './PragueMarathon2014.py',
         #'pyDefaults' : '',
         #'pyroot' : '',
         'RandomWalk' : './rndWalk.py',
         #'README.md' : '',
         'RijenNaSilnicich' : './Zahynuvsi.py',
         #'RooFit' : '',
         'SecureKody' : './AnalyzeSecureCodes.py',
         'Smearing' : './SmearingEffectOnRatio.py',
         #'ToF_multi' : '',
         'TopologicalLikelihood' : './Run.sh',
         #'Unsorted' : '',
         'VyberGaus' : './VyberGaus.py',
         'ZemanWords' : './Zeman.py',
         }


for ddir in dirs:
    cmd = dirs[ddir]
    print('Processing {} to run {}'.format(ddir, cmd))
    #os.system('cd {} ; {} ; cd ../'.format(ddir, cmd))
