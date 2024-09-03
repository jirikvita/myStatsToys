#!/usr/bin/python

import random, sys, os, math

###########################################################

syllabs = [ 'a', 'i', 'e', 'u', 'o',
            
            'ka', 'ki', 'ke', 'ku', 'ko',
            'sa', 'shi', 'se', 'su', 'so',
            'ta', 'chi', 'te', 'tsu', 'to',
            'na', 'ni', 'ne', 'nu', 'no',
            
            'ga', 'gi', 'ge', 'gu', 'go',
            'za', 'ji', 'ze', 'zu', 'zo',
            #'da', 'Ji', 'de', 'Zu', 'do',
            
            ]


#https://en.wikipedia.org/wiki/Hiragana_(Unicode_block)
#    print('\u3041')

hiragana = { 'a' : '\u3042', 'i' : '\u3044', 'e' : '\u3048', 'u' : '\u3046', 'o' : '\u304A',
             
             'ka' : '\u304B', 'ki' : '\u304D', 'ke' : '\u3051', 'ku' : '\u304F', 'ko' : '\u3053',
             'sa' : '\u3055', 'shi' : '\u3057', 'se' : '\u305B', 'su' : '\u3059', 'so' : '\u305D',
             'ta' : '\u305F', 'chi' : '\u3061', 'te' : '\u3066', 'tsu' : '\u3064', 'to' : '\u3068',
             'na' : '\u306A', 'ni' : '\u306B', 'ne' : '\u306D', 'nu' : '\u306C', 'no' : '\u306E',
             
             'ga' : '\u304C', 'gi' : '\u304E', 'ge' : '\u3053', 'gu' : '\u3050', 'go' : '\u3054',
             'za' : '\u3056', 'ji' : '\u3058', 'ze' : '\u305C', 'zu' : '\u305A', 'zo' : '\u305E',
             'da' : '\u3060', 'Ji' : '\u3062', 'de' : '\u3067', 'Zu' : '\u3066', 'do' : '\u3069',

             
             
            }

    
###########################################################

def toFill(used):
    for key,use in used.items():
        if not use:
            return True
    return False

###########################################################
def getTest(syllabs, indent = 5):
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
    test = []
    while toFill(used):
        j = int(random.uniform(0,1)*N)
        j = min(j,N-1)
        syl = syllabs[j]
        if not used[syl]:
            n = n+1
            used[syl] = True
            test.append(syl)
            endl = ' '
            if n % indent == 0:
                endl = '\n'
            print(f'{syl:3}', end = endl)
    print('------------------------------------------------')
    print('Hit a key for solution')
    a = input()
    print('Solution:')
    n = 0
    for syl in test:
        n = n + 1
        endl = ' '
        if n % indent == 0:
            endl = '\n'
        print(f'{hiragana[syl]}', end = endl)
    print('------------------------------------------------')

###########################################################

def main(argv):
    getTest(syllabs)


    
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


