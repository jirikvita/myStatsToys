#!/usr/bin/python3
# Po 19. února 2024, 09:33:36 CET

from math import sqrt, pow, log, exp, pi
import os, sys, getopt
from random import uniform

from matplotlib import pyplot as plt
import matplotlib.patches as patches


stuff = []
##########################################
def getPiGuesstimate(Nevts, storePoints = False):
    Nin = 0
    Nall = 0
    xsin = []
    ysin = []
    xsout = []
    ysout = []
    for i in range(0, Nevts):
        x = uniform(0,1)
        y = uniform(0,1)
        if x*x + y*y < 1:
            Nin = Nin + 1
            if storePoints:
                xsin.append(x)
                ysin.append(y)
        else:
            if storePoints:
                xsout.append(x)
                ysout.append(y)

        Nall = Nall + 1
    return 4*Nin / (1.*Nall), xsin, ysin, xsout, ysout

##########################################
def PlotPoint(xs, ys, pis):
     cols = ['blue', 'black']
     i = -1
     for x,y in zip(xs,ys):
         i = i + 1
         plt.scatter(x, y, s = 3, color=cols[i])
     plt.title('Arrows for pi')
         
     # Define the circle parameters
     circle_center = (0, 0)  # Center of the circle
     circle_radius = 1       # Radius of the circle

     # Plot the circle_radius
     quarter_circle = patches.Arc(circle_center, 2*circle_radius, 2*circle_radius, angle=0, theta1=0, theta2=90, color='red', label='')
     plt.gca().add_patch(quarter_circle)  # Add the quarter circle to the current axes

     # full circle:
     #circle = plt.Circle(circle_center, circle_radius, color='r', fill=False, label='Circle')
     #plt.gca().add_patch(circle)  # Add the circle to the current axes


     plt.gca().set_aspect('equal', adjustable='box')
     plt.grid(True)

     plt.xlabel('X')
     plt.ylabel('Y')
     plt.legend()
     plt.savefig('plot.pdf')
     
     plt.show()

     plt.scatter(range(0,len(pis)), pis)
     plt.show()
     
     return
##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
   
    Xs = []
    Ys = []
    Pis = []
    #Nevts = [ int(pow(10,i)) for i in range(1,10)]
    Nevts = [ int(pow(10,i)) for i in range(1,10)]
    for Nevt in Nevts:
        storePoints = Nevt == 1000
        pihat, xsin, ysin, xsout, ysout = getPiGuesstimate(Nevt, storePoints)
        Pis.append(pihat)
        print(f'Using N={Nevt}, the pi guess is {pihat:1.6f}')
        if len(xsin) > 0:
            Xs.append(xsin)
            Ys.append(ysin)
            Xs.append(xsout)
            Ys.append(ysout)
    #print(Xs[1],Ys[1])
    if len(Xs) > 0:
        PlotPoint(Xs, Ys, Pis)

    # ROOT.gApplication.Run()
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

