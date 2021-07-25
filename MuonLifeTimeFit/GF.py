#!/usr/bin/python

from math import *

tau=2.13
stat=0.21
#tau=2.12954
#stat=0.207899 
# cca dle fit range
syst=0.16

# old Honza:
#tau=2.20
#stat=0.28
#syst=0.11
tot = sqrt( pow(stat,2) + pow(syst,2))

print 'tau = %f +/- %f' % (tau, tot,)
print 'tau = %f +/- %f (stat) +/- %f (syst)' % (tau, stat, syst)

ee = 1.60217662e-19
c=299792456.
ctau = tau * 1e-6 *c /1e-15 # fm
print ctau
m=105.6583745e-3 # GeV
print 'm='
print m
h=6.62607004e-34

hc= h/1.e-15/(2.*pi)*c/ee*1e-9 # GeV fm
print 'hc='
print hc

GF = 1e5*sqrt( hc*192.*pow(pi,3)/(pow(m,5)*(ctau)) )  
gstat = GF / 2. * stat/tau
gsyst = GF / 2. * syst/tau
tot = sqrt( pow(gstat,2) + pow(gsyst,2) )
print 'GF = %f +/- %f (stat) +/- %f (syst) 10-5 GeV-2' % (GF, gstat, gsyst)
print 'GF = %f +/- %f 10-5 GeV-2' % (GF, tot,)

