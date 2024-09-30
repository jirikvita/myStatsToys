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
    print('debug, verb: ', debug, verb)
    
    infile = open(infname, 'r')
    ievt = -1
    metaData = {}
    ipix = 0
    Data = []
    Traces = []

    if skip == 'odd' and ievt % 2 == 1:
        print('Will read odd events only!')
    if skip == 'even' and ievt % 2 == 0:
        print('Will read even events only!')
            
    for xline in infile.readlines():
        line = xline[:-1]

        if 'Evt' in line:

            # store event till now:
            if len(metaData) > 0:
                # but first check whether shower parameters are within requirements;)
                GoOnBasedOnAllVars = True
                if len(restrictions) > 0:
                    if not GoOnBasedOnAllVars:
                        continue
                    for varname in restrictions:
                        if debug:
                            print(f'* Judging based on var {varname}')
                        if debug:
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
                                if debug:
                                    print(currval, reqval, sigma, shouldContinueSingleVar)
                        except:
                            print('error converting metadata {varname} value {strcurrval} to float...')
                        GoOnBasedOnAllVars = GoOnBasedOnAllVars and shouldContinueSingleVar
                    if not GoOnBasedOnAllVars:
                        if debug:
                            print('skipping event based on required variables')
                        continue # the reading to next event
                    
                    # end of requirements check; NOT TESTED YET
                    
                # here store event till now:  
                Data.append(  [ metaData, Traces ]  )
                metaData = {}

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
            if ievt % verb == 0:
                print(f'Reading event {ievt}')
            continue

        if len(metaData) == 0:
            # not supposed to read info for this event
            continue
        
        # read traces data:
        if ':' in line and ievt >= i1:
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
