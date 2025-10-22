#!/usr/bin/python3


from airsim import *

##########################################

def main(argv):

    dirs = ['png', 'pdf']
    for dir in dirs:
        os.system(f'mkdir -p {dir}')
    
    E,iteration,gBatch,doDraw = processArgs(argv)
    if E < 0:
        return 1

    # Primary particle energy!
    E0 = E*gGeV #1e14*geV
    primaryPID = 'p'
    #primaryPID = 'e'
    #primaryPID = 'A56'
    randomizeY = True
    
    # regulates whether split energies to two daughter particles evenly after X0*ln(2) or by exp decay law:
    halfSteps = False

    useDarkStyle = True
    
    ROOT.gStyle.SetOptTitle(0)
    if useDarkStyle:
        SetMyStyle()
    ROOT.gStyle.SetOptStat(1110)

    debug = 0
    world = cworld(debug)
    world.decayMuons = False
    world.useDarkStyle = useDarkStyle
    
    x, y = 0.*gkm, 0.*gm
    yend = 0*gm # dummy
    primary = cpart(E0, primaryPID, x, y, yend)
    tag, rtag, gtag, ropt = makeTags(primary, E0, iteration)

    tuneTag = world.Tunables.makeTag()
    world.makeOutHistos(iteration, rtag, ropt, f'root{tuneTag}/')
    world.PrintPars()
    
    # Simulate!
    particles = Simulate(doDraw, primary, world, E0, randomizeY, halfSteps)

    # get/make some stuff needed
    #print('Getting some stats...')
    #jmax,maxx    = getMaxX(particles)
    
    if doDraw:
        print('Counting drawn particles...')
        partCounts = {}
        for pid in glabel:
            partCounts[pid] = 0
        for part in particles:
            pid = part.pid
            try:
                partCounts[pid] = partCounts[pid] + 1
            except:
                print(f"Don't know how to count {pid}")
        for pid in partCounts:
            print(f'{pid:6}: {partCounts[pid]:10,}')
            
    spitSomeInfo(primary, E0, particles, world)
    if doDraw:
        can, h2, lines, partialDraw, statcan, txt = doAllDrawing(world, primary, E0, particles, halfSteps, tag, gtag, world.h1Nx, partCounts)
        stuff.append([can, h2, lines, partialDraw, statcan, txt])
    
    world.outfile.Write()
    
    if doDraw and not gBatch:
        ROOT.gApplication.Run()
    
    world.outfile.Close()
    
    print(f'...Thanks for running {sys.argv[0]}')
    print('...Returning and kiling oneself!')
    print('...So long, and thanks for all the fish!')
    #os.system('killall -9 run_airsim.py')
    return 0

###################################
###################################
###################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)
    
###################################
###################################
###################################

