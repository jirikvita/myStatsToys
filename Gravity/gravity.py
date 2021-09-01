#!/usr/bin/python
# Wed  1 Sep 08:14:55 CEST 2021

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp, sin, cos
import os, sys, getopt

cans = []
stuff = []


########################################################################################
def ChedkUniquePlanetsNamesOK(planets):
    ip1 = -1
    for p1 in planets:
        ip1 = ip1 + 1
        ip2 = -1
        for p2 in planets:
            ip2 = ip2 + 1
            if ip2 <= ip1:
                continue
            if p1.name == p2.name:
                return false
    return true

########################################################################################

kEarthMass = 1.
kSunMass = kEarthMass*333000.
kms = 1. # km/s
# grav. const
kappa = 1.

########################################################################################


# planets holder, makes sure they have unique ID etc;-)
class cSystem:
    def __init__(self, name):
        self.name = name
        planets = []
    


########################################################################################
# we assume circular motion, so the velocity is perp. to diameter vector
class cPlanet:
    def __init__(self, name, pid, mass, v0, R, theta, phi, mcol, mst = 20, msz = 1):
        self.name = name
        self.pid = pid
        self.mass = mass
        self.v0 = v0
        self.R = R
        self.theta = theta 
        self.phi = phi

        self.vr = 0.
        self.vphi = v0
        self.vtheta = 0.

        self.x = [X(), Y(), Z()]
        
    def X() = R*cos(phi)*sin(theta)
    def Y() = R*sin(phi)*sin(theta)
    def X() = R*cos(theta)

    
    
    # to finish!!! inital v pepr. to r!
    def vx() = vr*cos(phi)*sin(theta)
    def vy() = vr*sin(phi)*sin(theta)
    def vz() = vr*cos(theta)


########################################################################################
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html

def MakeSolarSystem():
    Sun = cPlanet('Sun', kSunMass, 0, 0.*kms, 0*AU, 0., 0., ROOT.kYellow, 20, 5.)

    # phi's are random
    # theta is 0
    
    # inner:
    Mercury = cPlanet('Mercury', 1, , 0.0553*kEarthMass, 29.4*kms, 0.387*AU, 0.,  pi.4, ROOT.kRed, 20, 2.)
    Venus   = cPlanet('Venus',   2, 0.815*kEarthMass, 21.8*kms,  0.723*AU, 0., -pi/4, ROOT.kRed, 20, 2.)
    Earth   = cPlanet('Sun',     3,       kEarthMass, 18.5*kms,  1.000*AU, 0.,  pi.2, ROOT.kGreen+2, 20, 2.)
    Mars    = cPlanet('Mars',    4, 0.107*kEarthMass, 15.0*kms,  1.520*AU, 0., -pi/2, ROOT.kRed, 20, 2.)

    # outer:
    Jupiter = cPlanet('Jupiter', 5, 317.8*kEarthMass, 8.1*kms,  5.20*AU, 0.,  pi/3, ROOT.kRed, 20, 2.)
    Saturn  = cPlanet('Saturn',  6,  95.2*kEarthMass, 6*kms,    9.58*AU, 0., -pi/3, ROOT.kRed, 20, 2.)
    Uranus  = cPlanet('Uranus',  7,  14.5*kEarthMass, 4.2*kms, 19.20*AU, 0.,  pi,   ROOT.kRed, 20, 2.)
    Neptune = cPlanet('Neptune', 8,  17.1*kEarthMass, 3.4*kms, 30.05*AU, 0., -pi,   ROOT.kRed, 20, 2.)
    
    planets = [Sun, Mercury, Venus, Earth, Mars, Jupiter]
    return planets


########################################################################################    
def Draw(planet):

    # TODO
    
    return

########################################################################################    
def DrawAll(system):
    for planet in system.planets:
        Draw(planet)
    return

########################################################################################        
def MakeStep(planets, dt = 0.001):
    return

########################################################################################        

def GetForce(p1, p2):
    f = [0., 0., 0.]
    dR2 = 0.
    vect = [0., 0., 0.]
    for i in range(0,dim):w
        dR2 = dr + pow(p1.x[i] - p2.x[i], 2)
        vect[i] = p1.x[i] - p2.x[i]
    if dR2 > 0:
        # todo: make sure the attractive force;-)
        # F ~ 1/dR^2, direct: F ~ R / dR^3, dR^3 = dR2^(3/2)
        for i in range(0,dim):
            f[i] = vect[i] / pow(dR2, 3./2.) * kappa * p1.mass * p2.mass
    return f

########################################################################################
def ComputeForceVect(planet, planets):

    f = [0., 0., 0]
    for p in planets:
        if p.pid == planet.pid:
            continue
        force = GetForce(planet, p)
        for i in range(0, dim):
            f[i] = f[i] + force[i]
    
    return f

########################################################################################
def MakeStep(planet, planets):

    F = ComputeForceVect(planet, planets)

    dp = [0., 0., 0.]
    for i in range(0, dim):
        # Mr. Newton
        dp[i] = F[i]*dt
        # dx = v*dt
        planet.x[i] = planet.x[i] + dp[i] / planet.mass * dt

        
        
    return

    


########################################################################################
########################################################################################
########################################################################################

# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
    #if len(sys.argv) > 1:
    #  foo = sys.argv[1]

    ### https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    ### https://pymotw.com/2/getopt/
    ### https://docs.python.org/3.1/library/getopt.html
    gBatch = False
    gTag=''
    print(argv[1:])
    try:
        # options that require an argument should be followed by a colon (:).
        opts, args = getopt.getopt(argv[2:], 'hbt:', ['help','batch','tag='])

        print('Got options:')
        print(opts)
        print(args)
    except getopt.GetoptError:
        print('Parsing...')
        print ('Command line argument error!')
        print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]]'.format(argv[0]))
        sys.exit(2)
    for opt,arg in opts:
        print('Processing command line option {} {}'.format(opt,arg))
        if opt == '-h':
            print('{:} [ -h -b --batch -tTag --tag="MyCoolTag"]'.format(argv[0]))
            sys.exit()
        elif opt in ("-b", "--batch"):
            gBatch = True
        elif opt in ("-t", "--tag"):
            gTag = arg
            print('OK, using user-defined histograms tag for output pngs {:}'.format(gTag,) )

    if gBatch:
        ROOT.gROOT.SetBatch(1)

    print('*** Settings:')
    print('tag={:}, batch={:}'.format(gTag, gBatch))

    canname = 'can'
    can = ROOT.TCanvas(canname, canname)
    cans.append(can)

    planets = MakeSolarSystem()
    

    
    ROOT.gApplication.Run()
    return

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

