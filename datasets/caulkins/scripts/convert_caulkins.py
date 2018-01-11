import sys
import numpy as np

from pyijgs.functions import measure_exec_time,write_cfg,binnarize

#from functions import make_it_clear

# 0: numerical 1: categorical 2: float
data_type = [0,1,1,1,2,1,2,1,2,2,2,2,2,2,2]
donotuse = [4,5,7]





'''
    The "Drug" field gives the drug type cited in the original data; "Drg Cde"
    indicates its coding into one of the ten types of drugs analyzed.
    
    The "Raw Qty" and "Units" field give the quantity as reported in the original
    data.  "Qin Grams" gives converts this quantity (or transaction size) into
    grams.
    
    "Low $" and "High $" give the bottom and top of the range of prices listed in
    the original data.  "Avg. $" is the midpoint of this range.  Similarly for "Lo
    Pur", "Hi Pur", and "Av Pur", all ranging between 0 and 100.  "Pure Qty" is
    the "Qin Grams" times the "Av Pur" divided by 100.
'''
# I DO NOT USE BOTH, WEIGHT AND GRAMS REPRESENTATION.

def convert(path):
    f = open(path,'r')
    map = {}
    #g=open('diagnosis.csv','w')
    array = []
    for line in f:
        x=[i for i in line.strip().split('\t')]
        if (len(x) > 1):
            array.append(x)
    f.close()
    matrix = []
    for i in array:
        row = []
        for j in [k for k in range(len(i)) if k not in donotuse]:
            if (data_type[j] != 1):
                row.append (float(i[j]))
            else:
                x = map.get(i[j],len(map))
                map[i[j]] = x
                row.append(x)
        matrix.append(row)
    matrix = np.array(matrix)

    return matrix,map


def save_context(path,table):
    f = open(path,'w')
    for i in table:
        s = str(int(i[0]))
        for j in range(1,len(i)):
            if data_type[j] < 2:
                s+=","+str(int(i[j]))
            else:
                s+=","+str(float(i[j]))
        f.write(s+'\n')
    f.close()

def save_map(path,map):
    with open(path,'w') as f:
        m = [(j,i) for i,j in map.items()]
        m.sort()
        for j,i in m:
            f.write(str(j)+"\t"+str(i)+"\n")

def read_thetas(path):
    with open(path,'r') as f:
        lines = f.readlines()
        return [float(theta) for theta in lines[0].strip().split(',')]


if __name__ == "__main__":
    # ORIGINAL FILE
    dataset="caulkins"
    dataPath = "../data/"
    iniPath = "../ini/"
    orfile = "original/{0}.original.txt".format(dataset)
    tbfile = "{0}.ijgs.{1}.ctx".format(dataset,'{0}')
    inifile = "{0}.ijgs.{1}.ini".format(dataset,'{0}')
    thetasfile = "original/{0}.ijgs.thetas.txt".format(dataset)
    
    print "\nPROCESSING {0} DATASET IN {1}".format(dataset,dataPath+orfile).upper()

    if "/" in sys.argv[0]:
        print "ERROR: Please execute the script from within the scripts folder"
        exit()
    #data,map = measure_exec_time(convert,"../data/caulkins.data.txt")
    data,map = convert(dataPath + orfile)

    measure_exec_time(save_context,dataPath+tbfile.format('tb'),dataPath+tbfile.format('tb'),data)
    print "\t->Context file written in "+dataPath+tbfile.format('tb')

    write_cfg(iniPath+inifile.format('tb'),dataset,6,"tb")

    save_map("../data/caulkins.ijgs.map.txt",map)
    print "\t->Map of categorical attributes written in ../data/caulkins.ijgs.map.txt"

    thetas = read_thetas(dataPath+thetasfile)
    measure_exec_time(binnarize,dataPath+tbfile.format('fca.fcacl'), dataPath+tbfile.format('fca{0}'), data, thetas, False, -1)

    write_cfg(iniPath+inifile.format('fca'),dataset,0,"fca")
    write_cfg(iniPath+inifile.format('fcacl'),dataset,0,"fcacl")






