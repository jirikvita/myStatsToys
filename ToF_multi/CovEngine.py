#!/usr/bin/python

from ROOT import *

# jk 27.4.2018



def PrettyPrintMatrix(m):
    for row in m:
        srow = ''
        for el in row:
            srow = srow + '{:2.2f} '.format(el)
        print srow
    return


class CovEngine():
    def __init__(self, nVars, nbins, t0, t1, scaling = 2.):
        self._nVars = nVars
        self._means = []
        self._squares = []
        self._Cov = [];
        for i in range(0, self._nVars):
            row = []
            for j in range(0, self._nVars):
                row.append(0.)
            self._Cov.append(row)
        for i in range(0, self._nVars):
            name = 'mean_{:}'.format(i)
            self._means.append(TH1D(name, name, nbins, t0, t1))
            for j in range(i+1, self._nVars):
                name = 'square_{:}{:}'.format(i,j)
                self._squares.append(TH1D(name, name, nbins, t0*t0/scaling, t1*t1/scaling))
                
    def Add(self, vect):
        if len(vect) != self._nVars:
            print 'CovEngine::Add: ERROR, did not get values of expected dimension {:}!'.format(self._nVars)
        index = -1
        for i in range(0,len(vect)):
            self._means[i].Fill(vect[i])
            for j in range(i+1,len(vect)):
                index = index+1
                self._squares[index].Fill(vect[i]*vect[j])
        return
                                        
    def MakeCov(self):
        index = -1
        #PrettyPrintMatrix(self._Cov)  
        for i in range(0, self._nVars):
            for j in range(i+1, self._nVars):
                index = index+1
                print self._squares[index].GetMean(), self._means[i].GetMean(),self._means[j].GetMean() 
                self._Cov[i][j] = self._squares[index].GetMean() - self._means[i].GetMean()*self._means[j].GetMean() 
        #PrettyPrintMatrix(self._Cov)        
        # symmetrize:
        for i in range(0, self._nVars):
            for j in range(0, i):
                self._Cov[i][j] = self._Cov[j][i] 
        #PrettyPrintMatrix(self._Cov)  
                
    def GetCovariance(self):
        self.MakeCov()
        return self._Cov
    def DrawAll(self):
        canname = 'Means'
        can1 = TCanvas(canname, canname)
        can1.Divide(self._nVars/2, self._nVars/2+1)
        canname = 'Squares'
        can2 = TCanvas(canname, canname)
        can2.Divide(self._nVars, self._nVars)
        index = -1
        for i in range(0, self._nVars):
            can1.cd(i+1)
            self._means[i].Draw('hist')
            for j in range(i+1, self._nVars):
                index = index+1
                can2.cd(i*self._nVars + j+1)
                self._squares[index].Draw('colz')
        
        return can1,can2
