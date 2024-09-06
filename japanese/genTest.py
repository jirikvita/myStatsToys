#!/usr/bin/python

import random, sys, os, math

###########################################################

syllabs = [ 'a', 'i', 'u', 'e', 'o',
            
            'ka', 'ki', 'ku', 'ke', 'ko',
            'sa', 'shi', 'su', 'se', 'so',
            'ta', 'chi', 'tsu', 'te', 'to',
            'na', 'ni', 'nu', 'ne', 'no',
            'ha', 'hi', 'fu', 'he', 'ho',
            
            #'ma', 'mi', 'mu', 'me', 'mo',
            #'ya', 'yu', 'yo',
            #'ra', 'ri', 'ru', 're', 'ro',
            #'wa', 'wa',
            #'n',
            
            #'ga', 'gi', 'gu', 'ge', 'go',
            #'za', 'ji', 'zu', 'ze', 'zo',
            
            #'da', 'Ji', 'Ze', 'de', 'do',
            #'ba', 'bi', 'bu', 'be', 'bo',
            #'pa', 'pi', 'pu', 'pe', 'po',
            
            
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
             'wa' : '\u308F', 'wo' : '\u3092', 'n' : '\u3093',


             
             'ga' : '\u304C', 'gi' : '\u304E', 'gu' : '\u3050', 'ge' : '\u3052', 'go' : '\u3054',
             'za' : '\u3056', 'ji' : '\u3058', 'zu' : '\u305A', 'ze' : '\u305C', 'zo' : '\u305E',
             'da' : '\u3060', 'Ji' : '\u3062', 'Zu' : '\u3065', 'de' : '\u3067', 'do' : '\u3069',

             
             
            }

# https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
# katakana {
# }

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
    print('Hit a key for solution -- when ready! ;-)')
    a = input()
    print('Solution:')
    print('------------------------------------------------')
    n = 0
    for syl in test:
        n = n + 1
        endl = ' '
        if n % indent == 0:
            endl = '\n'
        print(f'{hiragana[syl]:2}', end = endl)
    print('------------------------------------------------')

###########################################################

def main(argv):
    checkUniqUnicode(hiragana)
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


