#!/usr/bin/python

import uproot
import numpy as np
import matplotlib.pyplot as plt

# Open the ROOT file
file = uproot.open("KM66024.root")

# Access the tree inside the ROOT file (adjust "my_tree" to match your file)
tree = file["singlephotons/pmtaf_tree"]

# Extract branches as NumPy arrays
print('getting branches as np')
branches = tree.arrays(library="np")

# Now 'branches' is a dictionary where keys are branch names and values are NumPy arrays
print('getting individual branches')
branch1 = branches["energy"]
branch2 = branches["time_over_threshold_ns"]

# Print first 5 entries of branch1
print(branch1[:5])

print('plotting')

# 1D Histogram for branch1
plt.hist(branch1, bins=500, histtype='step', color='blue')
plt.xlabel('Branch 1 values')
plt.ylabel('Frequency')
plt.title('1D Histogram of Branch 1')
plt.show()

# 2D Histogram for branch1 vs branch2
plt.hist2d(branch1, branch2, bins=(500, 500), cmap='viridis')
plt.colorbar(label='Counts')
plt.xlabel('Energy')
plt.ylabel('ToT')
plt.title('2D Histogram of Branch 1 vs Branch 2')
plt.show()
