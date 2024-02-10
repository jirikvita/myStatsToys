#!/usr/bin/python

import ROOT
import math

def MakeGauss(name, xmin, xmax, mu = 0., sigma = 1.):
    fun = ROOT.TF1(name, "1/(sqrt(2*TMath::Pi()*[1]^2)) * exp(-(x-[0])^2/(2*[1]^2))", xmin, xmax)
    fun.SetParameters(mu, sigma)
    return fun

def MakeChi2(name, xmin = 0., xmax = 15., n = 5):
    fun = ROOT.TF1(name, "1/(2^([0]/2)*TMath::Gamma([0]/2)) * x^([0]/2-1) * exp(-x/2)", xmin, xmax)
    fun.SetParameter(0, n)
    return fun

    
def MakeCauchy(name, xmin, xmax, centre = 0., gamma = 1.):
    fun = ROOT.TF1("Cauchy", "[1]/(2*TMath::Pi()) * 1 / ( (x - [0])^2 + [1]^2/4 )", xmin, xmax)
    fun.SetParameters(centre, gamma)
    return fun


def MakeStudent(name, xmin, xmax, n = 5):
    fun = ROOT.TF1("Student", "TMath::Gamma(([0]+1)/2) / ( sqrt([0]*TMath::Pi()) * TMath::Gamma([0]/2) ) / (1+x^2/[0] )^(([0]+1)/2)", xmin, xmax)
    fun.SetParameter(0, n)
    return fun


def MakePoisson(name, xmin, xmax, mu):
    gr = ROOT.TGraph()
    gr.SetName(name)
    ip = 0
    for i in range(int(xmin), int(xmax)):
        val = 1./(1.*math.factorial(i))*math.exp(-mu)*math.pow(mu, i)
        gr.SetPoint(ip, i, val)
        ip = ip+1
    return gr

def MakeBinomial(name, n, p):
    gr = ROOT.TGraph()
    gr.SetName(name)
    ip = 0
    for i in range(0,n+1):
        val = math.factorial(n)/(1.*math.factorial(i)*math.factorial(n-i))*math.pow(p, i)*math.pow(1-p, n-i)
        gr.SetPoint(ip, i, val)
        ip = ip+1
    return gr
