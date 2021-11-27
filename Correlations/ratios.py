#!/usr/bin/python

# Jiri Kvita June 22nd 2016

# gama, alfa, beta averages per 10min:
# open:
BgAver =   [50.24444444444445, 0.4444444444444444, 54.855555555555554]
# 432, closed:[31.020833333333332, 0.0763888888888889, 37.479166666666664]
JeskyneAver = [62.46666666666667, 30.555555555555557, 183.64444444444445]
for b,j in zip(BgAver,JeskyneAver): 
    print(j/b)

# results:
#ratios:
#gama: 2.01370047011
#alfa: 400.0
#beta: 4.89990735594
