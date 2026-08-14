
JK:

===
--- plot oscilloscope waveforms, e.g.
readLecroyMultiWaveforms.py C4--mezzanine.txt

=== July 2026

--- DRs from the WUT fwk json file:
./darkRatesAnalyze.py ./TESTER_0_pmt_test_20260629_151733_63hDR/test_results_20260626_151733.json

--- DRs from WebMonitor's sqlite file, e.g.
./sqliteAnalyze.py Sqlite/20260713/158.194.88.101_monitor.sqlite

--- peak-to-valey, e.g.
./analyzePeakValley.py 1pe_measurement/28cm/test_run_thr30_att825_20260629_141522.root

--- analytical test of fittability of a convolution of Gauss and a rectangular opulse function, to emaulate native TTS comvolution with a fibre time spread:
python plotConv.py

=== August 2026
--- timewalk and TTS:

./timeWalkAnalysis.py TESTER_0_pmt_test_20260812_115919_MCP_3p05kV_dataTaking_Thr15mV/data_run_20260812_121315_data_taking_run.root
./timeWalkAnalysis.py TESTER_0_pmt_test_20260812_125451_3p05kV_dataTaking_Thr10mV/data_run_20260812_130404_data_taking_run.root

13.8.2026:
analysis of channels 1 (PMT) and 6 (MCP):
./timeWalkAnalysis.py TESTER_0_pmt_test_20260813_153745_MCP6_PMT1_Thr15mV/data_run_20260813_154552_data_taking_run.root
./timeWalkAnalysis.py TESTER_0_pmt_test_20260813_155612_MCP6_PMT1_Thr30mV/data_run_20260813_160422_data_taking_run.root

