#!/usr/bin/python

import random, sys, os, math
import termios
import tty


###########################################################

syllabs = [ 'a', 'i', 'u', 'e', 'o',
            
            'ka', 'ki', 'ku', 'ke', 'ko',
            'sa', 'shi', 'su', 'se', 'so',
            'ta', 'chi', 'tsu', 'te', 'to',
            'na', 'ni', 'nu', 'ne', 'no',
            'ha', 'hi', 'fu', 'he', 'ho',
            'ma', 'mi', 'mu', 'me', 'mo',
            
            'ya', 'yu', 'yo',
            'ra', 'ri', 'ru', 're', 'ro',
            'wa', 'O',
            'n',
            
            'ga', 'gi', 'gu', 'ge', 'go',
            'za', 'ji', 'zu', 'ze', 'zo',
            'da', 'Ji', 'Zu', 'de', 'do',

            'ba', 'bi', 'bu', 'be', 'bo',
            'pa', 'pi', 'pu', 'pe', 'po',

            'kya', 'kyu', 'kyo',
            'sya', 'syu', 'syo',
            'cya', 'cyu', 'cyo',
            'nya', 'nyu', 'nyo',
            'hya', 'hyu', 'hyo',
            'gya', 'gyu', 'gyo',
            'ja' , 'ju' , 'jo',
            'bya', 'byu', 'byo',
            'pya', 'pyu', 'pyo',
            
            ]


# https://en.wikipedia.org/wiki/Hiragana_(Unicode_block)
#    print('\u3041')
# TO FINISH ;-)

hiragana = { 'a' : '\u3042', 'i' : '\u3044',  'u' : '\u3046', 'e' : '\u3048', 'o' : '\u304A',
             
             'ka' : '\u304B', 'ki' : '\u304D', 'ku' : '\u304F', 'ke' : '\u3051', 'ko' : '\u3053',
             'sa' : '\u3055', 'shi' : '\u3057', 'su' : '\u3059', 'se' : '\u305B', 'so' : '\u305D',
             'ta' : '\u305F', 'chi' : '\u3061', 'tsu' : '\u3064', 'te' : '\u3066', 'to' : '\u3068',
             'na' : '\u306A', 'ni' : '\u306B', 'nu' : '\u306C', 'ne' : '\u306D', 'no' : '\u306E',
             'ha' : '\u306F', 'hi' : '\u3072', 'fu' : '\u3075', 'he' : '\u3078', 'ho' : '\u307B',

             'ma' : '\u307E', 'mi' : '\u307F', 'mu' : '\u3080', 'me' : '\u3081', 'mo' : '\u3082',
             'ya' : '\u3084', 'yu' : '\u3086', 'yo' : '\u3088',
             
             'ra' : '\u3089', 'ri' : '\u308A', 'ru' : '\u308B', 're' : '\u308C', 'ro' : '\u308D',
             'wa' : '\u308F', 'O' : '\u3092', 'n' : '\u3093',
             
             'ga' : '\u304C', 'gi' : '\u304E', 'gu' : '\u3050', 'ge' : '\u3052', 'go' : '\u3054',
             'za' : '\u3056', 'ji' : '\u3058', 'zu' : '\u305A', 'ze' : '\u305C', 'zo' : '\u305E',
             'da' : '\u3060', 'Ji' : '\u3062', 'Zu' : '\u3065', 'de' : '\u3067', 'do' : '\u3069',

             'ba' : '\u3070', 'bi' : '\u3073', 'bu' : '\u3076', 'be' : '\u3079', 'bo' : '\u307C',
             'pa' : '\u3071', 'pi' : '\u3074', 'pu' : '\u3077', 'pe' : '\u307A', 'po' : '\u307D',

             'kya' : '\u304D\u3083', 'kyu' : '\u304D\u3085', 'kyo' : '\u304D\u3087',
             'sya' : '\u3057\u3083', 'syu' : '\u3057\u3085', 'syo' : '\u3057\u3087',
             'cya' : '\u3061\u3083', 'cyu' : '\u3061\u3085', 'cyo' : '\u3061\u3087',
             'nya' : '\u306B\u3083', 'nyu' : '\u306B\u3085', 'nyo' : '\u306B\u3087',
             'hya' : '\u3072\u3083', 'hyu' : '\u3072\u3085', 'hyo' : '\u3072\u3087',
             'gya' : '\u304E\u3083', 'gyu' : '\u304E\u3085', 'gyo' : '\u304E\u3087',
             'ja'  : '\u3058\u3083', 'ju'  : '\u3058\u3085', 'jo'  : '\u3058\u3087',
             'bya' : '\u3073\u3083', 'byu' : '\u3073\u3085', 'byo' : '\u3073\u3087',
             'pya' : '\u3074\u3083', 'pyu' : '\u3074\u3085', 'pyo' : '\u3074\u3087',
             
            }



# https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
# katakana {
# }

###########################################################

def find_key(alphabet, val):
    for key in alphabet:
        if alphabet[key] == val:
            return key
    return None

###########################################################

"""
ChatGPT4:
"how can i use read() in python as a 'hit any key' and not have an amptuy printed line on terminal?"
How this works:
It switches the terminal to raw mode (disabling line buffering) so it reads a single character instead of waiting for Enter.
It restores the terminal settings after reading.
This method ensures there are no extra newlines printed and only one key is captured.
"""

def wait_for_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

###########################################################
def checkUniqUnicode(hiragana):
    vals = {}
    for key,val in hiragana.items():
        if not val in vals:
            vals[val] = 1
        else:
            vals[val] = vals[val] + 1
    for val,count in vals.items():
        if count > 1:
            print(f'ERROR: multiple unicode used for {val}!')

###########################################################

def toFill(used):
    for key,use in used.items():
        if not use:
            return True
    return False

###########################################################
def printTestLines(TestLines):
    for testline in TestLines:
        for syll in testline:
            print(f'{syll:6}', end='')
        print()
    return
###########################################################
           
def printSolutions(Solutions, alphabet):
    for solution in Solutions:
        for syll in solution:
            key = find_key(alphabet, syll)
            if syllabs.index(key) > 70:
                print(f'{syll:4}', end='')
            else:
                print(f'{syll:5}', end='')
        print()
    return

###########################################################
def printTestLine(testline):
    for syll in testline:
        print(f'{syll:6}', end='')
    print()
    return

###########################################################
def printSolution(solution, alphabet):
    for syll in solution:
        key = find_key(alphabet, syll)
        if syllabs.index(key) > 70:
            print(f'{syll:4}', end='')
        else:
            print(f'{syll:5}', end='')
    return

###########################################################
def getTest(syllabs, alphabet, doPrintBatch = 0, doReverse = 0, indent = 8):
    used = {}
    for syl in syllabs:
        used[syl] = False

    N = len(used)
    print(f'Will test you on {N} syllabs!')
    #print(syllabs)
    #print(used)
    print('------------------------------------------------')
 
    n = 0
    endl = ''
    toTest = []
    TestLines = []
    testline = []
    while toFill(used):
        j = int(random.uniform(0,1)*N)
        j = min(j,N-1)
        syl = syllabs[j]
        if not used[syl]:
            n = n+1
            used[syl] = True
            toTest.append(syl)
            endl = ' '
            testline.append(syl)
            if n % indent == 0:
                endl = '\n'
                TestLines.append(testline)
                testline = []
    if len(testline) > 0:
        TestLines.append(testline)

        
    n = 0
    Solutions = []
    solution = []
    for syl in toTest:
        n = n + 1
        endl = ' '
        solution.append(f'{alphabet[syl]}')
        if n % indent == 0:
            endl = '\n'
            Solutions.append(solution)
            solution = []
    if len(solution) > 0:
        Solutions.append(solution)


    #######################################
    # print

    if doPrintBatch:
        # print the assignement
        print('------------------------------------------------')
        if not doReverse:
            printTestLines(TestLines)
        else:
            printSolutions(Solutions, alphabet)
        print('------------------------------------------------')
        print('Hit a key for solution -- when ready! ;-)')
        wait_for_key()
        #print('Solution:')
        print('------------------------------------------------')
        if not doReverse:
            printSolutions(Solutions, alphabet)
        else:
            printTestLines(TestLines)
        print('------------------------------------------------')

    else:
        # line by line
        for testline, solution in zip(TestLines, Solutions):
            if not doReverse:
                printTestLine(testline)
            else:
                printSolution(solution, alphabet)
                print()
            wait_for_key()
            if not doReverse:
                printSolution(solution, alphabet)
                print('\n-----------------------------------------------------')
            else:
                printTestLine(testline)
                print('-----------------------------------------------------')


###########################################################
###########################################################
###########################################################

def main(argv):

    if '-h' in argv:
        print('Usage: ')
        print(f'argv[0] [PrintAllAtOnce=0/1] [reverse=0/1]')
        return
        
    checkUniqUnicode(hiragana)

    doPrintBatch = 0
    if len(argv) > 1:
        try:
            doPrintBatch = int(argv[1])
            print(f'OK, using custom doPrintBatch={doPrintBatch}')
        except:
            print('error getting doPrintBatch as first command line argument')

    doReverse = 0
    if len(argv) > 2:
        try:
            doReverse = int(argv[2])
            print(f'OK, using custom doReverse={doReverse}')
        except:
            print('error getting doReverse as first command line argument')
            
    getTest(syllabs, hiragana, doPrintBatch, doReverse)

    return

###########################################################
###########################################################
###########################################################

if __name__ == "__main__":
    # execute only if run as a script"
    main(sys.argv)

###########################################################
###########################################################
###########################################################


