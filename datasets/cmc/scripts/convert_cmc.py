import sys
import numpy as np

from pyijgs.functions import measure_exec_time,write_cfg,binnarize,read_thetas


# THIS DATSET NEEDS NO CONVERTION TO THE ENTRY OF SEPHIROT
# THIS FUNCTION JUST READS
# https://archive.ics.uci.edu/ml/machine-learning-databases/cmc/
def convert(path):
    f = open(path,'r')
    array = []
    for line in f:
        x=[]
        array.append([int(i) for i in line.split(',')])
    f.close()
    return np.array(array)





if __name__ == "__main__":
    # ORIGINAL FILE
    dataset="cmc"
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
    
    
    #data = measure_exec_time(convert,dataPath+orfile,dataPath+orfile)
    data = convert(dataPath+orfile)
    print "\t->Context file written in",dataPath+tbfile.format('tb'),
    import commands
    # THE CMC FILE COMES IN THE EXACT FORMAT SUPPORTED BY SEPHIROT. NO TRANSFORMATION NEEDED BUT JUST A COPY
    print commands.getstatusoutput("cp {0} {1}".format(dataPath+orfile,dataPath+tbfile.format('tb')))
    
    write_cfg(iniPath+inifile.format('tb'),dataset,6,"tb")

    thetas = read_thetas(dataPath+thetasfile)

    measure_exec_time(binnarize,dataPath+tbfile.format('fca.fcacl'),dataPath+tbfile.format('fca{0}'), data, thetas,False,-1)

    write_cfg(iniPath+inifile.format('fca'),dataset,0,"fca")
    write_cfg(iniPath+inifile.format('fcacl'),dataset,0,"fcacl")
