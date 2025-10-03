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

            ]
add = [
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
katakana = {

             'a' : '\u30A2', 'i' : '\u30A4',  'u' : '\u30A6', 'e' : '\u30A8', 'o' : '\u30AA',
             
             'ka' : '\u30AB', 'ki' : '\u30AD', 'ku' : '\u30AF', 'ke' : '\u30B1', 'ko' : '\u30B3',
             'sa' : '\u30B5', 'shi' : '\u30B7', 'su' : '\u30B9', 'se' : '\u30BB', 'so' : '\u30BD',
             'ta' : '\u30BF', 'chi' : '\u30C1', 'tsu' : '\u30C4', 'te' : '\u30C6', 'to' : '\u30C8',
             'na' : '\u30CA', 'ni' : '\u30CB', 'nu' : '\u30CC', 'ne' : '\u30CD', 'no' : '\u30CE',
             'ha' : '\u30CF', 'hi' : '\u30D2', 'fu' : '\u30D5', 'he' : '\u30D8', 'ho' : '\u30DB',

             'ma' : '\u30DE', 'mi' : '\u30DF', 'mu' : '\u30E0', 'me' : '\u30E1', 'mo' : '\u30E2',
             'ya' : '\u30E4', 'yu' : '\u30E6', 'yo' : '\u30E8',
             
             'ra' : '\u30E9', 'ri' : '\u30EA', 'ru' : '\u30EB', 're' : '\u30EC', 'ro' : '\u30ED',
             'wa' : '\u30EF', 'O' : '\u30F2', 'n' : '\u30F3',

             'ga' : '\u30AC', 'gi' : '\u30AE', 'gu' : '\u30B0', 'ge' : '\u30B2', 'go' : '\u30B4',
             'za' : '\u30B6', 'ji' : '\u30B8', 'zu' : '\u30BA', 'ze' : '\u30BC', 'zo' : '\u30BE',
             'da' : '\u30C0', 'Ji' : '\u30C2', 'Zu' : '\u30C5', 'de' : '\u30C7', 'do' : '\u30C9',

             'ba' : '\u30D0', 'bi' : '\u30D3', 'bu' : '\u30D6', 'be' : '\u30D9', 'bo' : '\u30DC',
             'pa' : '\u30D1', 'pi' : '\u30D4', 'pu' : '\u30D7', 'pe' : '\u30DA', 'po' : '\u30DD',
}
add = {
             'kya' : '\u30AD\u30E3', 'kyu' : '\u30AD\u30E5', 'kyo' : '\u30AD\u30E7',
             'sya' : '\u30B7\u30E3', 'syu' : '\u30B7\u30E5', 'syo' : '\u30B7\u30E7',
             'cya' : '\u30C1\u30E3', 'cyu' : '\u30C1\u30E5', 'cyo' : '\u30C1\u30E7',
             'nya' : '\u30CB\u30E3', 'nyu' : '\u30CB\u30E5', 'nyo' : '\u30CB\u30E7',
             'hya' : '\u30D2\u30E3', 'hyu' : '\u30D2\u30E5', 'hyo' : '\u30D2\u30E7',
             'gya' : '\u30AE\u30E3', 'gyu' : '\u30AE\u30E5', 'gyo' : '\u30AE\u30E7',
             'ja'  : '\u30B8\u30E3', 'ju'  : '\u30B8\u30E5', 'jo'  : '\u30B8\u30E7',
             'bya' : '\u30D3\u30E3', 'byu' : '\u30D3\u30E5', 'byo' : '\u30D3\u30E7',
             'pya' : '\u30D4\u30E3', 'pyu' : '\u30D4\u30E5', 'pyo' : '\u30D4\u30E7',
}

###########################################################


def find_key(syllabet, val):
    for key in syllabet:
        if syllabet[key] == val:
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
def checkUniqUnicode(syllabet):
    vals = {}
    for key,val in syllabet.items():
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
           
def printSolutions(Solutions, syllabet):
    for solution in Solutions:
        for syll in solution:
            key = find_key(syllabet, syll)
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
def printSolution(solution, syllabet):
    for syll in solution:
        key = find_key(syllabet, syll)
        if syllabs.index(key) > 70:
            print(f'{syll:4}', end='')
        else:
            print(f'{syll:5}', end='')
    return

###########################################################
def getTest(syllabs, syllabet, doPrintBatch = 0, doReverse = 0, indent = 8):
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
        solution.append(f'{syllabet[syl]}')
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
            printSolutions(Solutions, syllabet)
        print('------------------------------------------------')
        print('Hit a key for solution -- when ready! ;-)')
        wait_for_key()
        #print('Solution:')
        print('------------------------------------------------')
        if not doReverse:
            printSolutions(Solutions, syllabet)
        else:
            printTestLines(TestLines)
        print('------------------------------------------------')

    else:
        # line by line
        for testline, solution in zip(TestLines, Solutions):
            if not doReverse:
                printTestLine(testline)
            else:
                printSolution(solution, syllabet)
                print()
            wait_for_key()
            if not doReverse:
                printSolution(solution, syllabet)
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
        print(f'argv[0] [syllabete=h/k=hiragana/katakana] [PrintAllAtOnce=0/1] [reverse=0/1]')
        return

    
    askedFor = 'hiragana'
    if len(argv) > 1:
        askedFor = ''
        try:
            askedFor = argv[1]
            print(f'OK, using custom syllabet {askedFor}')
        except:
            # this should bever happen;)
            print('error getting user-defined syllabet to be examind from!')

    doPrintBatch = 0    
    if len(argv) > 2:
        try:
            doPrintBatch = int(argv[2])
            print(f'OK, using custom doPrintBatch={doPrintBatch}')
        except:
            print('error getting doPrintBatch as first command line argument')

    doReverse = 0
    if len(argv) > 3:
        try:
            doReverse = int(argv[3])
            print(f'OK, using custom doReverse={doReverse}')
        except:
            print('error getting doReverse as first command line argument')

    syllabet = {}
    if askedFor == 'h' or askedFor == 'H' or askedFor == 'hiragana' or askedFor == 'Hiragana':
        syllabet = hiragana
    elif askedFor == 'k' or askedFor == 'K' or askedFor == 'katakana' or askedFor == 'Katakana':
        syllabet = katakana
    else:
        print(f'Error determining the syllabete to be examined from! Should be h/k = hiragana/katakana; got "{askedFor}" instead.')
        return 1

    checkUniqUnicode(syllabet)

    getTest(syllabs, syllabet, doPrintBatch, doReverse)

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


