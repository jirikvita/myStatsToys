#!/usr/bin/python

# jk 24.9.2024

import matplotlib.pyplot as plt


#####################################################################
def passedMinSignal(Traces, minSignal):
    maxs = []
    for trace in Traces:
        maxs.append(max(trace))
    Max = max(maxs)
    return Max >= minSignal

#####################################################################
def plotMetaHistos(MetaData):

    logE = []
    Xmax = []
    coreX = []
    coreY = []
    azimuth = []
    zenith = []
    
    for mtd in MetaData:
        logE.append(mtd['logE'])
        Xmax.append(mtd['Xmax'])
        coreX.append(mtd['Corex'])
        coreY.append(mtd['Corey'])
        azimuth.append(mtd['Azimuth'])
        zenith.append(mtd['Zenith'])

    # Create a figure with 1 row and 2 columns of subplots
    plt.figure(figsize=(9, 9))

    alpha = min(max(0.01, 100./len(logE)), 1)
    #alpha = 1000./len(logE)
    

    print('Lengths to plot')
    print(len(logE))
    
    plt.subplot(2, 2, 1)
    plt.scatter(Xmax, logE, c='red', s=5, alpha = alpha)
    plt.xlabel('Xmax')
    plt.ylabel('logE')
    plt.xlim(300, 1000)
    plt.ylim(16, 21)

    plt.subplot(2, 2, 2)
    plt.scatter(coreX, coreY, c='blue', s=5, alpha = alpha)
    plt.xlabel('core X')
    plt.ylabel('core Y')
    plt.xlim(-30e3, -5e3)
    plt.ylim(-30e3, -5e3)

    plt.subplot(2, 2, 3)
    plt.scatter(zenith, azimuth, c='green', s=5, alpha = alpha)
    plt.xlabel('zenith')
    plt.ylabel('azimuth')
    plt.xlim(0, 90)
    plt.ylim(-180, 180)

    plt.show()
    
    return

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
def readData(infname, i1 = 0, i2 = -1, **kwargs):
    restrictions = {}
    debug = 0
    verb = 1000
    if 'restrictions' in kwargs:
        restrictions = kwargs['restrictions']
    if 'debug' in kwargs:
        debug = kwargs['debug']
    if 'verb' in kwargs:
        verb = kwargs['verb']
    skip=''
    if 'skip' in kwargs:
        skip = kwargs['skip']
    plotmetahistos = False
    if 'plotmetahistos' in kwargs:
        plotmetahistos = kwargs['plotmetahistos']
    minSignal = -1
    if 'minSignal' in kwargs:
        minSignal = kwargs['minSignal']
        
    print('debug, verb: ', debug, verb)

    if len(restrictions) > 0:
        print('Got non-trivial restrictions:')
        print(restrictions)
    
    infile = open(infname, 'r')
    ievt = -1
    metaData = {}
    MetaData = []
    ipix = 0
    Data = []
    Traces = []

    if skip == 'odd' and ievt % 2 == 1:
        print('Will read odd events only!')
    if skip == 'even' and ievt % 2 == 0:
        print('Will read even events only!')

    iline = -1
    for xline in infile.readlines():
        iline = iline+1
        if debug > 1:
            print(f'================= line {iline} =================')
        line = xline[:-1]

        if 'Evt' in line:

            # store event till now:
            if len(metaData) > 0:
                # but first check whether shower parameters are within requirements;)
                GoOnBasedOnAllVars = True
                if len(restrictions) > 0:
                    for varname in restrictions:
                        if debug > 0:
                            print(f'* Judging based on var {varname}')
                        if debug > 0:
                            print(restrictions[varname])
                        reqvals,sigma = restrictions[varname][0], restrictions[varname][1]
                        if not varname in metaData:
                            continue
                        strcurrval = metaData[varname]
                        try:
                            currval = float(strcurrval)
                            shouldContinueSingleVar = False
                            for reqval in reqvals:
                                shouldContinueSingleVar = shouldContinueSingleVar or (abs(currval - reqval) < sigma)
                                if debug > 0:
                                    print(currval, reqval, sigma, (abs(currval - reqval) < sigma), shouldContinueSingleVar)
                        except:
                            print('error converting metadata {varname} value {strcurrval} to float...')
                        GoOnBasedOnAllVars = GoOnBasedOnAllVars and shouldContinueSingleVar
                        if not GoOnBasedOnAllVars:
                            break
                    if not GoOnBasedOnAllVars:
                        if debug > 0:
                            print('SKIPPING event based on required variables')
                        metaData = {}
                        continue # the reading to next event
                    
                    # end of requirements check; NOT TESTED YET
                if debug > 0:
                    print('ACCEPTING event based on required variables')
                if len(metaData) < 1:
                    continue
                # here store event till now:
                passMinSignal = True
                if minSignal > 0:
                    passMinSignal = passedMinSignal(Traces, minSignal) 
                if len(Traces) > 0 and passMinSignal:
                    Data.append(  [ metaData, Traces ]  )
                    MetaData.append(metaData)
                else:
                    #print('Oooops, have got nontrivial metadata, but no corresponding traces! ')
                    metaData = {}
                    Traces = []
                    continue
                if debug == -1:
                    print('dimensions: meta: {}, traces: {} -- '.format(len(metaData), len(Traces)), end = '' )
                    #print(' ... ', metaData)
                    for trace in Traces:
                        print('{} '.format(len(trace)), end='')
                    print()
                metaData = {}
                Traces = []
                continue

            # done if the line was metadata;)
            
            # prepare for saving traces for the next event:
            Traces = []
            ievt = ievt + 1

            # check skipping conditions
            if ievt < i1:
                continue
            if skip == 'odd' and ievt % 2 == 1:
                continue
            if skip == 'even' and ievt % 2 == 0:
                continue
            if i2 > 0 and ievt > i2:
                break
            
            tokens = line.split(',')
            metaData = parseMetaData(tokens)
            evt = metaData['#Evt']
            if ievt % verb == 0:
                print(f'Reading event {ievt} ID {evt}, read so far: {len(Data)}')
            continue

        if len(metaData) == 0:
            # not supposed to read info for this event!
            continue
        
        # read traces data:
        if ':' in line and ievt >= i1:
            tokens = line.split(':')
            if len(tokens) > 1:
                spixevt,xtrace = tokens[0], tokens[1]
                #print(f'spixevt: "{spixevt}"')
                spix = spixevt.split('/')[0]
                sevt = spixevt.split('/')[1]
                thisevt = int(sevt)
                
                if thisevt != evt:
                    print(f'ERROR! Non-matching metadata evt {evt} and as in pixel trace: {thisevt}')
                    metaData = {}
                    Traces = []
                    continue
                
                strace = xtrace.replace(' ', '').split(',')
                if debug > 3:
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

    if plotmetahistos:
        plotMetaHistos(MetaData)
    
    return Data

#####################################################################
