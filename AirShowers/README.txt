Jiri Kvita
December 2025


*** General description

 -- Core simulation routines: airsim.py
 -- Constants and steering (new physics, aka Z'): consts.py
 -- Running script: run_airsim.py # also steering what primary particle!
Usage:
./run_airsim.py -h
Usage: ./run_airsim.py [logE(eV)=13.5] [iteration=0] [batch=0] [draw=1]
E.g.
./run_airsim.py 12.9
or, in GeV:
./run_airsim.py 50000 # 50 TeV


*** Personal work flow:

./GetAll.sh


in cmpXmean in main(), need to choose whether to use plotSsigma or not;-)
similar in drawCmpGraphs.py (there it's governed by xtag)
in drawCmpGraphs, also select which set of graphs to compare (grsNames*)

default model: (adds automatically also one more directory, root_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0)
./cmpXmean.py root_Inel_0.45_sigmaInel_0.2_C_10_Csigma_3_mnlEM1.125_mnlHad999.0_testNoNewPhysWithNewPhysArea

./runCmpAll.sh

./drawCmpGraphs.py

./quickPlotStdVsXmaxCmp.py


