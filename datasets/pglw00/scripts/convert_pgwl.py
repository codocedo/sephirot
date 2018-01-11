import sys
import numpy as np
from pyijgs.functions import measure_exec_time,write_cfg,binnarize,read_thetas,save_ctx


# ALMOST THE SAME FORMAT, BUT SPACE SEPARATED RATHER THAN COMMA SEPARATED
# NO NEED OF MUCH CONVERSION, ALL CATEGORICAL OR INTEGER
# http://lib.stat.cmu.edu/jasadata/pglw00.zip
def convert(path):
    f = open(path,'r')
    array = []
    for line in f:
        x=[int(i) for i in line.split()[1:]]
        array.append(x)
    f.close()
    return np.array(array)

if __name__ == "__main__":
    # ORIGINAL FILE
    dataset="pglw00"
    dataPath = "../data/"
    iniPath = "../ini/"
    orfile = "original/{0}.original.txt".format(dataset)
    tbfile = "{0}.ijgs.{1}.ctx".format(dataset,'{0}')
    inifile = "{0}.ijgs.{1}.ini".format(dataset,'{0}')
    thetasfile = "original/{0}.ijgs.thetas.txt".format(dataset)
    
    
    print "\nPROCESSING DIAGNOSIS DATASET in",dataPath+orfile
    
    if "/" in sys.argv[0]:
        print "ERROR: Please execute the script from within the scripts folder"
        exit()

#data = measure_exec_time(convert,dataPath+orfile)
    data = convert(dataPath+orfile)
    measure_exec_time(save_ctx,dataPath+tbfile.format('tb'),dataPath+tbfile.format('tb'),data)
    print "\t->Context file written in",dataPath+tbfile.format('tb')

    write_cfg(iniPath+inifile.format('tb'),dataset,6,"tb")
    
    thetas = read_thetas(dataPath+thetasfile)
    
    measure_exec_time(binnarize,dataPath+tbfile.format('fca.fcacl'),dataPath+tbfile.format('fca{0}'), data, thetas,True,-1)
    
    write_cfg(iniPath+inifile.format('fca'),dataset,0,"fca")
    write_cfg(iniPath+inifile.format('fcacl'),dataset,0,"fcacl")
