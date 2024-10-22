#!/usr/bin/env python3
import uproot as ur
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# example by Nick Prouse
# modified by Jiri Kvita

# read channels from file
file = ur.open("KM66024.root")
tree = [file[c].arrays() for c in ["singlephotons/pmtaf_tree"]]
all_channels = tree # + ...

#single_pulses = np.where(np.all([c["nPeaks"] >= 1 for c in all_channels], axis=0))[0]
##is_over_threshold = np.all([c["PeakVoltage"][single_pulses, 0] > 0.2 for c in all_channels], axis=0)
#is_over_threshold = np.all([c["PeakVoltage"][single_pulses, 0] > 0.02 for c in leadGlass], axis=0)
#good_events = single_pulses[is_over_threshold]

cut1 = np.where(np.all([c["energy"] >= 1.e-4 for c in all_channels], axis=0))[0]
is_over_threshold = np.all([c["energy"][cut1] > 0.001 for c in all_channels], axis=0)

good_events = cut1[is_over_threshold]

# calculate the means
energies = np.mean([c["energy"][good_events] for c in tree], axis=0)
tot = np.mean([c["time_over_threshold_ns"][good_events] for c in tree], axis=0)

# limits
tot_lim = (0, 100.)
energy_lim = (250, 350.)

# plotting

# plot 2d and 1d histograms
fig, axs = plt.subplots(2,2, constrained_layout=True, figsize=(12, 10))
h = axs[0, 1].hist2d(energies, tot, bins=200, range=(energy_lim, tot_lim), norm=mcolors.LogNorm())


# 1d histogram of tot
axs[0, 0].hist(tot, bins=200, range=tot_lim, histtype="step")
axs[0, 0].set_xlim(*tot_lim)
axs[0, 0].set_yscale('log')

# 1d histogram of ACT2+ACT3 amplitude
axs[1, 1].hist(energies, bins=200, range=energy_lim, histtype="step", orientation='horizontal')
axs[1, 1].set_ylim(*energy_lim)

# 2d histogram
h = axs[1, 0].hist2d(energies, tot, bins=200, range=(energy_lim, tot_lim), norm=mcolors.LogNorm())
axs[1, 0].set_xlabel("Energy")
axs[1, 0].set_ylabel("ToT")
#fig.colorbar(h[3], ax=axs[1, 0], pad=0)
plt.show()
