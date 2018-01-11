import sys
import numpy as np
from pyijgs.functions import measure_exec_time,write_cfg,binnarize,read_thetas,save_ctx

# http://lib.stat.cmu.edu/jasadata/hughes-r
def convert(path):
    f = open(path,'r')
    #g=open('diagnosis.csv','w')
    array = []
    for line in f:
        x=[float(i) for i in line.split()]
        array.append(x)
        # hl - left endpoint HIV-1 infection time interval
        # First column: -1: In utero infection. 0-24: means infection occurred no earlier than that time .
        # 25: means uninfected as of 24 months of age
        if x[0] == -1:
            x.append(1)
            x.append(0)
        elif x[0] == 25:
            x[0] = -1
            x.append(0)
            x.append(1)
        else:
            x.append(0)
            x.append(0)
        # hr - right endpoint of HIV-1 infection time interval
        # Second column 0-24 means infection ocurred no later than that time
        if x[1] == 25:
            x.append(1)
            x[1] = -1
        else:
            x.append(0)
        # dtime death time
        # Third column 0-24 means infection ocurred no later than that time
        if x[2] == 25:
            x.append(1)
            x[2] = -1
        else:
            x.append(0)
    f.close()
    return np.array(array)



if __name__ == "__main__":
    # ORIGINAL FILE
    dataset="hughes"
    dataPath = "../data/"
    iniPath = "../ini/"
    orfile = "original/{0}.original.txt".format(dataset)
    tbfile = "{0}.ijgs.{1}.ctx".format(dataset,'{0}')
    inifile = "{0}.ijgs.{1}.ini".format(dataset,'{0}')
    thetasfile = "original/{0}.ijgs.thetas.txt".format(dataset)
    empty_value = -1
    
    print "\nPROCESSING {0} DATASET IN {1}".format(dataset,dataPath+orfile).upper()
    
    if "/" in sys.argv[0]:x
        print "ERROR: Please execute the script from within the scripts folder"
        exit()


    #data = measure_exec_time(convert,dataPath+orfile)
    data = convert(dataPath+orfile)
    measure_exec_time(save_ctx,dataPath+tbfile.format('tb'),dataPath+tbfile.format('tb'),data)
    print "\t->Context file written in",dataPath+tbfile.format('tb')

    write_cfg(iniPath+inifile.format('tb'),dataset,6,"tb",more="empty_value = {0}\n".format(empty_value))
    
    thetas = read_thetas(dataPath+thetasfile)
    
    measure_exec_time(binnarize,dataPath+tbfile.format('fca.fcacl'),dataPath+tbfile.format('fca{0}'), data, thetas,False,empty_value)
    
    write_cfg(iniPath+inifile.format('fca'),dataset,0,"fca")
    write_cfg(iniPath+inifile.format('fcacl'),dataset,0,"fcacl")
