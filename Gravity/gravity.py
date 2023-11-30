#!/usr/bin/python
# Wed  1 Sep 08:14:55 CEST 2021

# na pocest meho ucitele doc. RNDr. Jiri Boka, CSc.

# todo: odtransformovat teziste?

import ROOT
from math import sqrt, pow, log, exp, sin, cos, pi, log10, log
import os, sys, getopt

cans = []
stuff = []

########################################################################################

kday = 24*3600. # seconds
kyear = 31556952. # seconds; http://www.kylesconverter.com/time/years-to-seconds
kAU = 149597871e3 # m
kEarthMass = 5.972e24 # kg
kSunMass = 1.989e30 # kgso
kSunName = 'Sun'
kms = 1000. # 1 km/s = 1000 m/s
# grav. const
kappa = 6.67408e-11 # m3 kg-1 s-2

# 3D world:)
kdim = 3
kepsilon = 1.e-2*kAU

#########################################

def GetDr(x,y):
    dr = 0.
    for xx,yy in zip(x,y):
        dr = dr + pow(xx-yy, 2)
    if dr > 0:
        dr = sqrt(dr)
    return dr


#########################################
def MakeDigitStr(i, digits = 4):
    tag = str(i)
    n = digits
    try: 
        n = int(log10(i))
    except ValueError:
        pass
    if i == 0:
        n = 0
    for i in range(0, digits - n):
        tag = '0' + tag
    return tag

########################################################################################

# planets holder, to make sure they have unique ID etc;-)
class cSystem:
    def __init__(self, name, x0, y0, z0, SF, i = 0, j = 0, cw = 800, ch = 800, printstep = 1000, bgc = ROOT.kBlack, txtc = ROOT.kWhite):
        self.name = name
        self.X0 = x0
        self.Y0 = y0
        self.Z0 = z0
        self.SF = SF

        self.time = 0.
        
        self.bgc = bgc
        self.txtc = ROOT.kWhite
        
        self.planets = []
        self.can = ROOT.TCanvas(name, name, i, j, cw, ch)
        self.scaleLine = ROOT.TObject()
        self.can.SetFillColor(self.bgc)
        self.leg = ROOT.TLegend(0.88, 0.02, 0.98, 0.20)
        
        self.iteration = 0
        self.printstep = printstep
    def Inc(self, dt):
        self.iteration = self.iteration + 1
        self.time = self.time + dt
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


    def Print(self):
        for planet in self.planets:
            planet.Print()
        return
    
    def DrawPlanetTrack(self, planet):
        # TODO
        self.can.cd()
        
        # TODO:
        # in the future: keep only finite numer of lines
        # so shift them after some time
        # draw last few dashed
        # draw first few thicker
        #lx1, ly1, lx2, ly2 = planet.x[0]/self.SF, planet.x[1]/self.SF, planet.oldx[0]/self.SF, planet.oldx[1]/self.SF
        #print('lines coors: ', lx1, ly1, lx2, ly2)
        #planet.lines.append(ROOT.TLine(lx1, ly1, lx2, ly2))
        #line = planet.lines[-1]        
        #line.SetLineColor(planet.mcol)
        #line.SetLineWidth(2)
        #line.SetLineStyle(1)
        #line.SetNDC()
        #line.Draw()
        if planet.name != kSunName:
            planet.Draw(self.SF)
        return
    
    # set planets and draw the universe:
    def SetPlanets(self, planets):
        self.planets = planets
        return

    def DrawTimer(self):
        stime = ''
        if self.time < kyear:
            stime = '{:.0f} days'.format(self.time / kday)
        else:
            stime = '{:.1f} years'.format(self.time / kyear)
        dx = -0.47
        dy = 0.45
        self.timer = ROOT.TLatex(self.X0/self.SF + dx, self.Y0/self.SF + dy, stime)
        self.timer.SetTextColor(self.txtc)
        self.timer.SetTextSize(0.03)
        self.timer.Draw()
    
    def DrawUniverse(self):
        self.can.Draw()
        for p in self.planets:
            m = p.MakeMarker(self.SF)
            m.SetMarkerSize(1)
            self.leg.AddEntry(m, p.name, 'P')
        self.leg.SetFillColor(self.bgc)
        self.leg.SetTextColor(self.txtc)
        self.leg.Draw()
        dx = 0.45
        dy = -0.45
        lx1,ly1,lx2,ly2 = self.X0/self.SF  + 1.*kAU/self.SF - dx, self.Y0/self.SF + dy, self.X0/self.SF - dx, self.Y0/self.SF + dy
        print('1AU lines coors: ', lx1,ly1,lx2,ly2)
        self.scaleLine = ROOT.TLine(lx1,ly1,lx2,ly2)
        self.scaleLine.SetLineColor(self.txtc)
        self.scaleLine.SetLineWidth(2)
        self.scaleLine.SetLineStyle(1)
        self.scaleLine.SetNDC()
        self.scaleLine.Draw()
        ddy = 0.01
        self.AUtxt = ROOT.TLatex(lx2,ly1 + ddy, '1 AU')
        self.AUtxt.SetNDC()
        self.AUtxt.SetTextSize(0.03)
        self.AUtxt.SetTextColor(self.txtc)
        self.AUtxt.Draw()
        self.DrawTimer()
    
    def DrawTracks(self):
        for planet in self.planets:
            self.DrawPlanetTrack(planet)
        if self.iteration % self.printstep == 0:
            #    self.can.Print(self.name + '{}.png'.format(MakeDigitStr(self.iteration, 4)))
            ROOT.gPad.Update()
        self.DrawTimer()
        return


########################################################################################
# we assume circular motion, so the velocity is perp. to diameter vector
class cPlanet:
    def __init__(self, name, pid,  X0, Y0, Z0, mass, v0, R, theta, phi, mcol, mst = 20, msz = 0.3):
        self.name = name
        self.pid = pid
        self.mass = mass
        self.v0 = v0
        self.R = R
        self.theta = theta 
        self.phi = phi
        self.mcol = mcol
        self.mst = mst
        self.msz = msz

        self.time = 0.
        self.timePrinted = False
        
        self.lines = []
        self.markers = []

        self.x = [X0 + self.R*cos(self.phi)*sin(self.theta),
                  Y0 + self.R*sin(self.phi)*sin(self.theta),
                  Z0 + self.R*cos(self.theta)]

        # initial position for period extraction
        self.x0 = [1.*self.x[0], 1.*self.x[1], 1.*self.x[2], ]
        
        # perp vector to initial R:
        self.v = [-self.v0*sin(self.phi)*sin(self.theta),
                  +self.v0*cos(self.phi)*sin(self.theta),
                  0.]
        self.oldx = [0., 0., 0.]
        self.Archive()
        self.Print()
        
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

    def Print(self):
        print('{} id={} m={} x={} y={} z={} AU; vx={} vy={} vz={} km/s'.format(self.name, self.pid, self.mass,
                                                                               self.x[0]/kAU, self.x[1]/kAU, self.x[2]/kAU,
                                                                               self.v[0]/kms, self.v[1]/kms, self.v[2]/kms) )
        return

    def MakeMarker(self, SF):
        mark = ROOT.TMarker(self.x[0]/SF, self.x[1]/SF, self.mst)
        mark.SetMarkerSize(self.msz)
        mark.SetMarkerColor(self.mcol)
        mark.SetNDC()
        self.markers.append(mark)
        return mark
    
    def Draw(self, SF):
        self.MakeMarker(SF)
        mark = self.markers[-1]
        mark.Draw()
        
    def Archive(self):
        for i in range(0, kdim):
            self.oldx[i] = 1.*self.x[i]
        return
    
    def RecomputePolar(self):
        self.Archive()
        self.R = self.GetR2()
        if self.R > 0:
            self.R = sqrt(self.R)
        
        # not needed so far?
        # TODO!!!
        # tantheta = 
              
        return self.R, self.theta, self.phi
        
    def RecomputeCartesian(self):
        self.Archive()
        x,y,z = self.X(), self.Y(), self(Z)
        return x,y,z

   # use velocity in radial coors?


########################################################################################
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/planet_table_ratio.html

def MakeSolarSystem(cw, ch, printstep):

    # phi's are random
    # theta is 0

    relSF = 25 #120 # 40 ,120, 7...
    SF = relSF * kAU
    
    X0 = relSF/2.*kAU
    Y0 = relSF/2.*kAU
    Z0 = 0.0*kAU
    
    system = cSystem("Solar", X0, Y0, Z0, SF, 0, 0, cw, ch, printstep)
    
    theta = pi/2.
    
    # the Sun
    Sun = cPlanet(kSunName, 0, X0, Y0, Z0, kSunMass, 0.*kms, 0*kAU, theta, 0., ROOT.kYellow, 20, 4.)
    Sun.Draw(SF)


    """
    Mercury = cPlanet('Mercury', 1, X0, Y0, Z0, 0.0553*kEarthMass, 29.4*kms, 0.387*kAU, theta,  pi/4, ROOT.kWhite, 20)
    Venus   = cPlanet('Venus',   2, X0, Y0, Z0, 0.815*kEarthMass,  21.8*kms,  0.723*kAU, theta, -pi/4, ROOT.kOrange, 20)
    Earth   = cPlanet('Earth',   3, X0, Y0, Z0,       kEarthMass,  18.5*kms,  1.000*kAU, theta,  pi/4, ROOT.kGreen+2, 20)
    Mars    = cPlanet('Mars',    4, X0, Y0, Z0, 0.107*kEarthMass,  15.*kms,  1.520*kAU, theta, -pi/2, ROOT.kRed+1, 20)

    # outer:
    Jupiter = cPlanet('Jupiter', 5, X0, Y0, Z0, 317.8*kEarthMass, 8.1*kms,  5.20*kAU, theta,  pi/3, ROOT.kPink, 20)
    Saturn  = cPlanet('Saturn',  6, X0, Y0, Z0,  95.2*kEarthMass,  6.*kms,    9.58*kAU, theta, -pi/3, ROOT.kMagenta, 20)
    Uranus  = cPlanet('Uranus',  7, X0, Y0, Z0,  14.5*kEarthMass,  4.2*kms, 19.20*kAU, theta,  pi,   ROOT.kBlue, 20)
    Neptune = cPlanet('Neptune', 8, X0, Y0, Z0,  17.1*kEarthMass,  3.4*kms, 30.05*kAU, theta, -pi,   ROOT.kCyan, 20)
    Pluto = cPlanet('Pluto',     9, X0, Y0, Z0,  0.0025*kEarthMass,2.9*kms, 39.48*kAU, theta, -pi,   ROOT.kCyan+2, 20)
    """

        
    # inner:
    Mercury = cPlanet('Mercury', 1, X0, Y0, Z0, 0.0553*kEarthMass, 47.4*kms, 0.387*kAU, theta,  pi/4, ROOT.kWhite, 20)
    Venus   = cPlanet('Venus',   2, X0, Y0, Z0, 0.815*kEarthMass,  35.0*kms,  0.723*kAU, theta, -pi/4, ROOT.kOrange, 20)
    Earth   = cPlanet('Earth',   3, X0, Y0, Z0,       kEarthMass,  29.8*kms,  1.000*kAU, theta,  pi/4, ROOT.kGreen+2, 20)
    Mars    = cPlanet('Mars',    4, X0, Y0, Z0, 0.107*kEarthMass,  24.1*kms,  1.520*kAU, theta, -pi/2, ROOT.kRed+1, 20)

    DoomsDay  = cPlanet('Dooms Day',    -1, X0, Y0, Z0, 0.5*kEarthMass,  42.*kms,  0.8*kAU, theta, 3*pi/2, ROOT.kGray+1, 20)

    # outer:
    Jupiter = cPlanet('Jupiter', 5, X0, Y0, Z0, 317.8*kEarthMass, 13.1*kms,  5.20*kAU, theta,  pi/3, ROOT.kPink, 20)
    Saturn  = cPlanet('Saturn',  6, X0, Y0, Z0,  95.2*kEarthMass,  9.7*kms,    9.58*kAU, theta, -pi/3, ROOT.kMagenta, 20)
    Uranus  = cPlanet('Uranus',  7, X0, Y0, Z0,  14.5*kEarthMass,  6.8*kms, 19.20*kAU, theta,  pi,   ROOT.kBlue, 20)
    Neptune = cPlanet('Neptune', 8, X0, Y0, Z0,  17.1*kEarthMass,  5.4*kms, 30.05*kAU, theta, -pi,   ROOT.kCyan, 20)
    Pluto = cPlanet('Pluto',     9, X0, Y0, Z0,  0.0025*kEarthMass,4.7*kms, 39.48*kAU, theta, -pi,   ROOT.kCyan+2, 20)

    

    #planets = [Sun, Earth]
    #planets = [Sun, Earth, DoomsDay, Jupiter]
    #planets = [Sun, Mercury, Venus, Earth, Mars, DoomsDay]
    #planets = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]

    planets = [Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, DoomsDay, Pluto]

    system.SetPlanets(planets)
    allok = system.CheckUniquePlanetsNamesOK(planets)
    print('System planet names are OK: {}'.format(allok))
    
    return system


########################################################################################
def MakeBinary(cw, ch, printstep):

    # phi's are random
    # theta is 0

    relSF = 2.
    SF = relSF * kAU
    
    X0 = relSF/2.*kAU
    Y0 = relSF/2.*kAU
    Z0 = 0.0*kAU
    
    system = cSystem("Binary", X0, Y0, Z0, SF, 400, 0, cw, ch, printstep)
    
    theta = pi/2.
    
    # the Suns of the binary system
    Sun1 = cPlanet('Sun1', 0, X0, Y0, Z0, 1.*kSunMass,  20.*kms, 0.5*kAU, theta, -pi/2, ROOT.kRed, 20, 0.3)
    Sun2 = cPlanet('Sun2', 1, X0, Y0, Z0, 1.*kSunMass,  20.*kms, 0.5*kAU, theta, +pi/2, ROOT.kBlue, 20, 0.3)

    planets = [Sun1, Sun2]

    system.SetPlanets(planets)
    allok = system.CheckUniquePlanetsNamesOK(planets)
    print('System planet names are OK: {}'.format(allok))
    
    return system



########################################################################################
def MakeTertiary(cw, ch, printstep):

    # phi's are random
    # theta is 0

    relSF = 50.
    SF = relSF * kAU
    
    X0 = relSF/2.*kAU
    Y0 = relSF/2.*kAU
    Z0 = 0.0*kAU
    
    system = cSystem("Tertiary", X0, Y0, Z0, SF, 800, 0, cw, ch, printstep)
    
    theta = pi/2.
    
    # the Suns of the binary system
    Sun1 = cPlanet('Sun1', 0, X0, Y0, Z0, 1.*kSunMass, 12.*kms, 5*kAU, theta, -pi/2, ROOT.kRed, 20, 0.3)
    Sun2 = cPlanet('Sun2', 1, X0, Y0, Z0, 1.*kSunMass, 10.*kms, 5*kAU, theta, +pi/2, ROOT.kBlue, 20, 0.3)
    Sun3 = cPlanet('Sun3', 1, X0, Y0, Z0, 1.*kSunMass, 2.*kms, 1.*kAU, theta, pi, ROOT.kWhite, 20, 0.3)

    planets = [Sun1, Sun2, Sun3]

    system.SetPlanets(planets)
    allok = system.CheckUniquePlanetsNamesOK(planets)
    print('System planet names are OK: {}'.format(allok))
    
    return system


########################################################################################        
# beware, some physics here;-)

def GetForce(p1, p2, debug = 0):
    # force
    f = [0., 0., 0.]
    # R^2
    dR2 = 0.
    # vector R
    vect = [0., 0., 0.]
    for i in range(0,kdim):
        dR2 = dR2 + pow(p1.x[i] - p2.x[i], 2)
        vect[i] = -p1.x[i] + p2.x[i]
    if dR2 > 0:
        # todo: make sure the attractive force;-)
        # F ~ 1/dR^2, direction: F ~ R / dR^3, dR^3 = dR2^(3/2)
        if debug:
            print('dR: AU', sqrt(dR2) / kAU)
            print('vect: {}, {}, {} AU'.format(vect[0]/kAU, vect[1]/kAU, vect[2]/kAU))
        for i in range(0,kdim):
            if debug:
                print('m1={}, m2={} kappa*m1*m2={} kappa*m1*m2/dR2={}'.format(p1.mass, p2.mass, kappa * p1.mass * p2.mass, 1. / dR2 * kappa * p1.mass * p2.mass ))
            ### CORE PHYSICS
            f[i] = vect[i] / pow(dR2, 3./2.) * kappa * p1.mass * p2.mass
        if debug:
            print('force: {}, {}, {} MZ', f[0]/kEarthMass, f[1]/kEarthMass, f[2]/kEarthMass, )
    else:
        print('ERROR getting the force!')
    return f

########################################################################################
def ComputeForceVect(planet, planets):
    f = [0., 0., 0]
    for p in planets:
        if p.pid == planet.pid:
            continue
        force = GetForce(planet, p)
        for i in range(0, kdim):
            ### CORE superposition of forces
            f[i] = f[i] + force[i]
    
    return f

########################################################################################
def MakeStep(planet, system, dt, debug = 0):
    if debug:
        print('-------------- MakeStep {} --------------'.format(planet.name))
    F = ComputeForceVect(planet, system.planets)
    if debug:
        print('original v: {}, {}, {} km/s'.format(planet.v[0]/kms, planet.v[1]/kms, planet.v[2]/kms) )
    dp = [0., 0., 0.]
    for i in range(0, kdim):
        # Mr. Newton
        ### CORE PHYSICS
        dp[i] = F[i]*dt
        if debug:
            print('   dp{} = {}'.format(i, dp[i]))
        # dx = v*dt
        ### CORE PHYSICS
        ### TODO!!!
        #planet.x[i] = planet.x[i] + planet.v[i]*dt + dp[i]*dt/planet.mass
        #planet.v[i] = planet.v[i] + dp[i]/planet.mass
        # better"
        planet.v[i] = planet.v[i] + dp[i] / planet.mass
        planet.x[i] = planet.x[i] +  planet.v[i]*dt

    ###!!! planet.RecomputePolar()
    # and if use above, remove next line!
    planet.Archive()
    planet.time = planet.time + dt
    
    if planet.name != kSunName and not planet.timePrinted and GetDr(planet.x, planet.x0) < kepsilon and planet.time > 10*kday:
        # Wow, we have a revolution!
        T = planet.time / (24*3600.)
        print('planet {} T={} days'.format(planet.name, T))
        planet.timePrinted = True
    
    if debug:
        print('updated v: {}, {}, {} km/s'.format(planet.v[0]/kms, planet.v[1]/kms, planet.v[2]/kms) )
    return

########################################################################################

def MovePlanets(system, dt, debug = 0):
    for planet in system.planets:
        MakeStep(planet, system, dt)
        if debug:
            planet.Print()
    system.Inc(dt)
    #print('iteration: {}'.format(system.iteration))

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

    # STEERING !
    cw = 798
    ch = 799
    printstep = 100
    dt = 0.1*kday #0.1*kday
    Nsteps = 30000 # 12000
    
    systems = [ MakeSolarSystem(cw, ch, printstep),
                #MakeBinary(cw, ch, printstep),
                #MakeTertiary(cw, ch, printstep)
    ]

    for system in systems:
        system.Print()
        system.DrawUniverse()

    for istep in range(0, Nsteps):
        for system in systems:
            MovePlanets(system, dt)
            system.DrawTracks()

    # more steps for the tertiry system:
    for istep in range(Nsteps, 1*Nsteps):
        for system in systems[-1:]:
            MovePlanets(system, dt)
            system.DrawTracks()

            
    stuff.append(systems)

    for system in systems:
        system.can.Print('final_' + system.name + '.png')
    
    
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

