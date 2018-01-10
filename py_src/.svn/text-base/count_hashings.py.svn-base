'''
    DESIGNED TO COUNT THE IDS.
    IF THE AMOUNT OF IDS IS LOWER THAN THE AMOUNT OF CONCEPTS,
    THEN THERE IS A PROBLEM WITH THE HASHINGS
'''

import sys

if __name__ == '__main__':
    f = open(sys.argv[1],'r')
    hs = set([])
    d = {}
    i = 0
    for line in f:
        i+=1
        x =line.replace('\n','').strip()
        hs.add(x)
        if d.get(x,-1) != -1:
            print x
        d[x]=x

    
    if len(hs) != i:
        print 'PROBLEM WITH HASHINGS!!!',len(hs),'!=',i
    else:
        print 'No prob, bro!',len(hs),'==',i