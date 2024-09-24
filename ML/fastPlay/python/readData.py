#!/usr/bin/python

# jk 24.9.2024

#####################################################################

def parseMetaData(tokens):
    mdata = {}
    for token in tokens:
        data = token.split('=')
        if len(data) > 1:
            try:
                key = data[0]
                val = float(data[1])
                mdata[key] = val
            except:
                print(f'Error parsing metadata item {data}')
    return mdata

#####################################################################

def readData(infname, nMaxEvts = -1, debug = 0):
    infile = open(infname, 'r')
    ievt = -1
    metaData = {}
    ipix = 0
    Data = []
    Traces = []
    for xline in infile.readlines():
        line = xline[:-1]
        if 'Evt' in line:
            # store event till now:
            if len(metaData) > 0:
                Data.append(  [ [metaData, Traces] ]  )

            # prepare for next event:
            Traces = []
            ievt = ievt + 1
            if ievt > nMaxEvts:
                break
            tokens = line.split(',')
            metaData = parseMetaData(tokens)
            print(f'Reading event {ievt}')
            continue
        if ':' in line:
            tokens = line.split(':')
            if len(tokens) > 1:
                spix,xtrace = tokens[0], tokens[1]
                strace = xtrace.replace(' ', '').split(',')
                if debug:
                    print(f'Processing pixel id {ipix}')
                    print('strace: ', strace)
                ipix = int(spix)

                trace = []
                for sval in strace:
                    try:
                        val = float(sval)
                        trace.append(val)
                    except:
                        print(f'Could not add trace val "{sval}"')
                Traces.append(trace)
  
    infile.close()
    return Data

#####################################################################
