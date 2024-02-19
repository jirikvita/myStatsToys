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
    xs = []
    ys = []
    for i in range(0, Nevts):
        x = uniform(0,1)
        y = uniform(0,1)
        if x*x + y*y < 1:
            Nin = Nin + 1
        Nall = Nall + 1
        if storePoints:
            xs.append(x)
            ys.append(y)
    return 4*Nin / (1.*Nall), xs, ys
##########################################
def PlotPoint(x, y):
     plt.scatter(x, y, s = 3)
     plt.title('Arrows for pi')
     # Define the circle parameters
     circle_center = (0, 0)  # Center of the circle
     circle_radius = 1       # Radius of the circle

     # Plot the circle_radius
     quarter_circle = patches.Arc(circle_center, 2*circle_radius, 2*circle_radius, angle=0, theta1=0, theta2=90, color='r', label='')
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
     return
##########################################
# https://www.tutorialspoint.com/python/python_command_line_arguments.htm
def main(argv):
   
    Xs = []
    Ys = []
    Nevts = [ int(pow(10,i)) for i in range(1,6)]
    for Nevt in Nevts:
        storePoints = Nevt == 1000
        pihat, xs, ys = getPiGuesstimate(Nevt, storePoints)
        print(f'Using N={Nevt}, the pi guess is {pihat:1.4f}')
        if len(xs) > 0:
            Xs.append(xs)
            Ys.append(ys)

    if len(Xs) > 0:
        PlotPoint(Xs[0], Ys[0])


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

