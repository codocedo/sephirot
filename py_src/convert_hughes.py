import sys
from utils import execute

# http://lib.stat.cmu.edu/jasadata/hughes-r
def convert(pmgr):
    f = open(pmgr.original_filepath, 'r')
    #g=open('diagnosis.csv','w')
    array = []
    for line in f:
        x = [float(i) for i in line.split()]
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
    return array


def execute_hughes(dataset_name = "hughes"):
    execute(dataset_name, convert)

if __name__ == "__main__":
    execute_hughes()
