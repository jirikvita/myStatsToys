#!/usr/bin/python

import uproot
import pandas as pd
import matplotlib.pyplot as plt

#import seaborn as sns


# Open the ROOT file
file = uproot.open("KM66024.root")

# Access the tree inside the ROOT file (adjust "my_tree" to match your file)
tree = file["singlephotons/pmtaf_tree"]

# Convert the tree to a pandas DataFrame (choose branches you're interested in)
print('getting branches as df')
df = tree.arrays(library="pd")

print('plotting')

# Plot 1D histogram for a single branch
plt.hist(df['energy'], bins=500, histtype='step', color='blue')
plt.xlabel('Energies')
plt.ylabel('Events')
plt.title('Energies histo')
plt.show()

# Plot 2D histogram for two branches
plt.hist2d(df['energy'], df['time_over_threshold_ns'], bins=(500, 500), cmap='viridis')
plt.colorbar(label='Counts')
plt.xlabel('Energy')
plt.ylabel('ToT')
plt.title('2D Histogram of ToT vs Energy')
plt.show()


## 1D Histogram using seaborn
#sns.histplot(df['branch1'], bins=50, kde=True, color='blue')
#plt.title('1D Histogram with Seaborn')
#plt.show()
#
## 2D Histogram (Hexbin) using seaborn
#sns.jointplot(x='branch1', y='branch2', data=df, kind='hex', cmap='viridis')
#plt.show()