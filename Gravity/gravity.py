#!/usr/bin/python
# Wed  1 Sep 08:14:55 CEST 2021

# na pocest meho ucitele doc. RNDr. Jiri Boka, CSc.

from __future__ import print_function

import ROOT
from math import sqrt, pow, log, exp, sin, cos, pi
import os, sys, getopt

cans = []
stuff = []


########################################################################################

kAU = 149597871e3 # m
kEarthMass = 5.972e24
kSunMass = kEarthMass*333000.
kms = 1000. # 1 km/s = 1000 m/s
# grav. const
kappa = 6.67408e10-11 # m3 kg-1 s-2

# 3D world:
kdim = 3

########################################################################################

# planets holder, to make sure they have unique ID etc;-)
class cSystem:
    def __init__(self, name, x0, y0, z0, cw = 800, ch = 100):
        self.name = name
        self.X0 = x0
        self.Y0 = y0
        self.Z0 = z0
        self.planets = []
        self.can = ROOT.TCanvas(name, name, 0, 0, cw, ch)
    def CheckUniquePlanetsNamesOK(self, planets):
        ip1 = -1
        for p1 in self.planets:
            ip1 = ip1 + 1
            ip2 = -1
            for p2 in self.planets:
                ip2 = ip2 + 1
                if ip2 <= ip1:
                    continue
                if p1.name == p2.name:
                    return False
                if p1.pid == p2.pid:
                    return False
        return True

    def DrawPlanet(self, planet):
        # TODO
        return

    def Draw(self):
        for planet in self.planets:
            self.DrawPlanet(planet)
        return


########################################################################################
# we assume circular motion, so the velocity is perp. to diameter vector
class cPlanet:
    def __init__(self, name, pid,  X0, Y0, Z0, mass, v0, R, theta, phi, mcol, mst = 20, msz = 1):
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

        self.x = [X0 + self.R*cos(self.phi)*sin(self.theta),
                  Y0 + self.R*sin(self.phi)*sin(self.theta),
                  Z0 +  self.R*cos(self.theta)]
        self.v = [0., 0., 0.]
        self.oldx = [0., 0., 0.]
        
        self.RecomputePolar()
 
    def GetR2(self):
        R2 = 0.
        for i in range(0,kdim):
            R2 = R2 + pow(self.x[i], 2)
        return R2
            
    def X(self):
        self.x[0] = self.R*cos(self.phi)*sin(self.theta)
        return self.x[0]
    def Y(self):
        self.x[1] = self.R*sin(self.phi)*sin(self.theta)
        return self.x[1]
    def Z(self):
        self.x[2] = self.R*cos(self.theta)
        return self.x[2]

    def Archive(self):
        for i in range(0, kdim):
            self.oldx[i] = 1.*self.x[i]
        return
    
    def RecomputePolar(self):
        self.Archive()
        self.R = self.GetR2()
        return self.R, self.theta, self.phi
        
    def RecomputeCartesian(self):
        self.Archive()
        x,y,z = self.X(), self.Y(), self(Z)
        return x,y,z

    # iunitial speed:
    # to finish!!! inital v pepr. to r!
    def vx(self):
        self.vx = self.vr*cos(self.phi)*sin(self.theta)
        return vx
    def vy(self):
        self.vy = self.vr*sin(self.phi)*sin(self.theta)
        return self.vy
    def vz(self):
        self.vz = self.vr*cos(self.theta)
        return self.vz


########################################################################################
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html

def MakeSolarSystem():

    


    # phi's are random
    # theta is 0

    X0 = 0.5
    Y0 = 0.5
    Z0 = 0.0

    # the Sun
    Sun = cPlanet('Sun', 0, X0, Y0, Z0, kSunMass, 0.*kms, 0*kAU, 0., 0., ROOT.kYellow, 20, 5.)
    
    # inner:
    Mercury = cPlanet('Mercury', 1, X0, Y0, Z0, 0.0553*kEarthMass, 29.4*kms, 0.387*kAU, 0.,  pi/4, ROOT.kRed, 20, 2.)
    Venus   = cPlanet('Venus',   2, X0, Y0, Z0, 0.815*kEarthMass, 21.8*kms,  0.723*kAU, 0., -pi/4, ROOT.kRed, 20, 2.)
    Earth   = cPlanet('Sun',     3, X0, Y0, Z0,       kEarthMass, 18.5*kms,  1.000*kAU, 0.,  pi/2, ROOT.kGreen+2, 20, 2.)
    Mars    = cPlanet('Mars',    4, X0, Y0, Z0, 0.107*kEarthMass, 15.0*kms,  1.520*kAU, 0., -pi/2, ROOT.kRed, 20, 2.)

    # outer:
    Jupiter = cPlanet('Jupiter', 5, X0, Y0, Z0, 317.8*kEarthMass, 8.1*kms,  5.20*kAU, 0.,  pi/3, ROOT.kRed, 20, 2.)
    Saturn  = cPlanet('Saturn',  6, X0, Y0, Z0,  95.2*kEarthMass, 6*kms,    9.58*kAU, 0., -pi/3, ROOT.kRed, 20, 2.)
    Uranus  = cPlanet('Uranus',  7, X0, Y0, Z0,  14.5*kEarthMass, 4.2*kms, 19.20*kAU, 0.,  pi,   ROOT.kRed, 20, 2.)
    Neptune = cPlanet('Neptune', 8, X0, Y0, Z0,  17.1*kEarthMass, 3.4*kms, 30.05*kAU, 0., -pi,   ROOT.kRed, 20, 2.)
    
    planets = [Sun, Mercury, Venus, Earth, Mars, Jupiter]

    system = cSystem("Solar", X0, Y0, Z0)
    system.planets = planets
    allok = system.CheckUniquePlanetsNamesOK(planets)
    print('System planet names are OK: {}'.format(allok))
    
    return system


########################################################################################        

def GetForce(p1, p2):
    f = [0., 0., 0.]
    dR2 = 0.
    vect = [0., 0., 0.]
    for i in range(0,kdim):
        dR2 = dR2 + pow(p1.x[i] - p2.x[i], 2)
        vect[i] = p1.x[i] - p2.x[i]
    if dR2 > 0:
        # todo: make sure the attractive force;-)
        # F ~ 1/dR^2, direct: F ~ R / dR^3, dR^3 = dR2^(3/2)
        for i in range(0,kdim):
            f[i] = vect[i] / pow(dR2, 3./2.) * kappa * p1.mass * p2.mass
    return f

########################################################################################
def ComputeForceVect(planet, planets):

    f = [0., 0., 0]
    for p in planets:
        if p.pid == planet.pid:
            continue
        force = GetForce(planet, p)
        for i in range(0, kdim):
            f[i] = f[i] + force[i]
    
    return f

########################################################################################
def MakeStep(planet, planets, dt):

    F = ComputeForceVect(planet, planets)

    dp = [0., 0., 0.]
    for i in range(0, kdim):
        # Mr. Newton
        dp[i] = F[i]*dt
        # dx = v*dt
        planet.x[i] = planet.x[i] + dp[i] / planet.mass * dt
        planet.v[i] = planet.v[i] + dp[i] / planet.mass
        
    return

########################################################################################

def MovePlanets(planets, dt = 1.e-4):
    for planet in planets:
        MakeStep(planet, planets, dt)

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

    system = MakeSolarSystem()

    Nsteps = 100
    dt = 1e-4
    for istep in range(0, Nsteps):
        MovePlanets(system.planets, dt)
        system.Draw()
        
    
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

