import sys
import numpy as np

from pyijgs.functions import measure_exec_time,write_cfg,binnarize,read_thetas,save_ctx

# 0: numerical 1: categorical 2: float
data_type = [1,1,2,1,1]

# CONVERT FROM THE FORMAT OF SERVO
# contains ABCDE elements in the first two columns. Need to be converted
# https://archive.ics.uci.edu/ml/machine-learning-databases/servo/
def convert(path):
    f = open(path,'r')
    array = []
    di = {'A':1,'B':2,'C':3,'D':4,'E':5}
    array = []
    for line in f:
        x=[]
        data= [i.strip() for i in line.replace('\n','').split(',')]
        x.extend([float(i) for i in data[2:]])
        x.extend([di[i] for i in data[0:2]])
        array.append(x)
    f.close()
    return np.array(array)

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


if __name__ == "__main__":
    # ORIGINAL FILE
    dataset="servo"
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
    
    
    #data = measure_exec_time(convert,dataPath+orfile)
    data = convert(dataPath+orfile)
    measure_exec_time(save_context,dataPath+tbfile.format('tb'),dataPath+tbfile.format('tb'),data)
    print "\t->Context file written in",dataPath+tbfile.format('tb')

    write_cfg(iniPath+inifile.format('tb'),dataset,6,"tb")

    thetas = read_thetas(dataPath+thetasfile)

    measure_exec_time(binnarize,dataPath+tbfile.format('fca.fcacl'),dataPath+tbfile.format('fca{0}'), data, thetas,False,-1)

    write_cfg(iniPath+inifile.format('fca'),dataset,0,"fca")
    write_cfg(iniPath+inifile.format('fcacl'),dataset,0,"fcacl")






