#!/usr/bin/python

import matplotlib.pyplot as plt

# jk 27.11.2024

"""
https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2020-07/fig_06.pdf
https://atlas.web.cern.ch/Atlas/GROUPS/PHYSICS/PAPERS/HIGG-2020-07/

"""

y = [3, 8, 3, 7, 5,
     11, 14, 10, 9, 9, 9,
     16, 14, 32, 38, 57,
     46, 40, 28, 15,
     11, 9, 12, 15, 9,
     17, 15,
     10, 13, 10, 12, 8, 8, 10, 10, 10,
     3, 8, 6, 6, 7, 5, 7, 9]

print(y)
print(len(y))

dx = (160 - 105) / len(y)
x = [ 105 + i*dx for i in range(1,len(y)+1) ]

print(x)
print(len(x))


plt.plot(x, y, marker='o')

plt.show()
