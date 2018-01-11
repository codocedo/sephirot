import sys
import numpy as np

from pyijgs.functions import measure_exec_time,write_cfg,binnarize,read_thetas,save_ctx


# CONVERT FROM THE FORMAT OF DIAGNOSIS
# contains yes or not which are converted to binary elements.
# THE FIRST ELEMENT IS A NUMBER, NEEDS convertions
# https://archive.ics.uci.edu/ml/machine-learning-databases/acute/
def convert(path):
    f = open(path,'r')
    di = {'yes':2,'no':1}
    array = []
    for line in f:
        x=[]
        data= line.replace('\n','').split('\t')
        x.append(float(data[0].replace(',','.')))
        x.extend([di[i] for i in data[1:]])
        array.append(x)
    f.close()
    return np.array(array)


def save_context(path, table):
    with open(path,'w') as f:
        for i in table:
            s = str(float(i[0]))
            for j in range(1,len(i)):
                s+=","+str(float(i[j]))
            f.write(s+'\n')
                                        
                                        
if __name__ == "__main__":
    # ORIGINAL FILE
    dataset="diagnosis"
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
    measure_exec_time(save_context,dataPath+tbfile.format('tb'),dataPath+tbfile.format('tb'),data)
    print "\t->Context file written in",dataPath+tbfile.format('tb')

    write_cfg(iniPath+inifile.format('tb'),dataset,6,"tb")

    thetas = read_thetas(dataPath+thetasfile)

    measure_exec_time(binnarize,dataPath+tbfile.format('fca.fcacl'),dataPath+tbfile.format('fca{0}'), data, thetas,False,-1)

    write_cfg(iniPath+inifile.format('fca'),dataset,0,"fca")
    write_cfg(iniPath+inifile.format('fcacl'),dataset,0,"fcacl")






