#!/snap/bin/pyroot

import ROOT

def io_test():

  # some example
  fit = ROOT.TF1('fun', 'gaus', -1, 1)
  fit.SetParameters(1, 0, 1)
  h1 = ROOT.TH1D('h1', 'h1', 100, -1, 1)
  h1.FillRandom('fun', 1000)
  h1.Fit(fit)
  print('fitmean: {}'.format(fit.GetParameter(1)))
  
  # ascii write to a file
  outfilename = 'out.txt'
  infile = open(outfilename, 'w')
  infile.write('fitmean: {:1.5f}'.format(fit.GetParameter(1)))
  infile.close()

  # ascii read from a file
  inputfilename = outfilename
  infile = open(inputfilename)
  xlines = infile.readlines()
  for xline in xlines:
      line = xline[:-1] # remove end of line character
      print('Read: {}'.format(line))
  infile.close()
  

if __name__ == "__main__":
    # execute only if run as a script"
    io_test()


    

