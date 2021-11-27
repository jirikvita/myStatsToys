import ROOT
import math

# Jiri Kvita June 22nd 2016

objs = []
# col = [ROOT.kBlack, ROOT.kTeal+2, ROOT.kOrange+2, ROOT.kMagenta, ROOT.kGreen+2, ROOT.kRed, ROOT.kPink, 2, 4, 3, 1, 2, 3, 4, 6, 7, 1, 2, 3, 4, 6, 7, 1, 2, 3, 4, 6]
col = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, 2, 4, 3, 1, 2, 3, 4, 6, 7, 1, 2, 3, 4, 6, 7, 1, 2, 3, 4, 6]
mark = [ 20, 20, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 20]


#########################################
def MakeSpectrum(matrix, iy, ranges):
    tag = matrix[iy][0]
    hist = ROOT.TH1D(tag, tag + ';E [keV];Events', ranges[0], ranges[1], ranges[2])
    for i in range(0, len(matrix[iy][1])):
        val = matrix[iy][1][i]
        if val > 0:
            hist.Fill(i, val)
    hist.SetMarkerStyle(mark[iy])
    hist.SetMarkerColor(col[iy])
    hist.SetLineColor(col[iy])
    #hist.GetXaxis().SetTitle(tag)
    objs.append(hist)
    return hist

#########################################
def Make2D(matrix, ny, name, tag = ''):
    nx = len(matrix[0][1])
    h2 = ROOT.TH2D(name, name + ';' + tag + '', nx, 0, nx, ny, 0, ny)
    for i in range(0,ny):
        for j in range(0, len(matrix[i][1])):
            val = matrix[i][1][j]
            h2.SetBinContent(j+1, ny-i, val)

    i = 0
    for item in matrix:
        h2.GetYaxis().SetBinLabel(ny-i, matrix[i][0])
        i = i+1
    h2.SetStats(0)
    objs.append(h2)
    return h2

#########################################
def MakeGraph(matrix, iy, tag = 'frame'):
    gr = ROOT.TGraph()
    tag = matrix[iy][0]
    gr.SetName(tag + "_gr")
    for i in range(0, len(matrix[iy][1])):
        gr.SetPoint(i, i, matrix[iy][1][i])
#        i = i+1
    gr.SetMarkerStyle(mark[iy])
    # gr.SetMarkerSize(0.7)
    gr.SetMarkerColor(col[iy])
    gr.SetLineColor(col[iy])
    gr.GetXaxis().SetTitle(tag)
    objs.append(gr)
    return gr

#########################################
def MakeScatterGraph(matrix, ii, jj):
    gr = ROOT.TGraph()
    tag = matrix[jj][0] + '_vs_' + matrix[ii][0]
    gr.SetName(tag + "_gr")
    np = 0
    for i in range(0, len(matrix[ii][1])):
        gr.SetPoint(np, matrix[ii][1][i], matrix[jj][1][i])
        np = np+1
    gr.SetMarkerStyle(mark[ii+jj])
    gr.SetMarkerColor(col[ii+jj])
    gr.SetLineColor(col[ii+jj])
    objs.append(gr)
    gr.GetXaxis().SetTitle(matrix[ii][0])
    gr.GetYaxis().SetTitle(matrix[jj][0])
    return gr


#########################################
def MakeCov(h2):
    tag = h2.GetName() + 'Cov'
    ny = h2.GetYaxis().GetNbins()
    nx = h2.GetXaxis().GetNbins()
    Cov = ROOT.TH2D(tag, tag, ny, 0, ny, ny, 0, ny)
    for j in range(1,h2.GetYaxis().GetNbins()+1):
        Cov.GetXaxis().SetBinLabel(j, h2.GetYaxis().GetBinLabel(j))
    for j in range(1,h2.GetYaxis().GetNbins()+1):
        Cov.GetYaxis().SetBinLabel(j, h2.GetYaxis().GetBinLabel(j))

    aver = []
    for j in range(1,h2.GetYaxis().GetNbins()+1):
        maver = 0.
        n = 0
        for i in range(1,h2.GetXaxis().GetNbins()+1):
            maver = maver + h2.GetBinContent(i,j)
            n = n+1
        maver = maver / n
        aver.append(maver)

    print('Aver: ', aver)
    cvals = []
    # compute 1/nx sum(val-aver)
    for j in range(1,h2.GetYaxis().GetNbins()+1):
        vals = []
        for i in range(1,h2.GetYaxis().GetNbins()+1):
            vali = 0.
            # go through data
            for k in range(1,h2.GetXaxis().GetNbins()+1):
                vali = vali + 1./(nx-1)*(h2.GetBinContent(k,j) - aver[j-1])*(h2.GetBinContent(k,i) - aver[i-1])
            vals.append(vali)
        cvals.append(vals)

    for j in range(1,Cov.GetYaxis().GetNbins()+1):
        for i in range(1,Cov.GetXaxis().GetNbins()+1):
            Cov.SetBinContent(i,j, cvals[i-1][j-1])

    Cov.Scale(1.)
    Cov.SetStats(0)
    return Cov

#########################################
def MakeCorr(Cov):
    Corr = Cov.Clone(Cov.GetName() + 'Corr')
    Corr.Reset()
    for i in range(1,Cov.GetXaxis().GetNbins()+1):
        for j in range(1,Cov.GetYaxis().GetNbins()+1):
            Corr.SetBinContent(i, j, Cov.GetBinContent(i,j) / math.sqrt(Cov.GetBinContent(i,i)*Cov.GetBinContent(j,j)))
    Corr.Scale(1.)
    Corr.SetStats(0)
    return Corr

