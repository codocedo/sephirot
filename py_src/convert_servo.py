import sys
# import numpy as np

from utils import execute

# 0: numerical 1: categorical 2: float
data_type = [1,1,2,1,1]

# CONVERT FROM THE FORMAT OF SERVO
# contains ABCDE elements in the first two columns. Need to be converted
# https://archive.ics.uci.edu/ml/machine-learning-databases/servo/
def convert(pmgr):
    f = open(pmgr.original_filepath, 'r')
    array = []
    categorical_map = {'A':1,'B':2,'C':3,'D':4,'E':5}
    array = []
    for line in f:
        x=[]
        data= [i.strip() for i in line.replace('\n','').split(',')]
        x.extend([float(i) for i in data[2:]])
        x.extend([categorical_map[i] for i in data[0:2]])
        array.append(x)
    f.close()
    # return np.array(array)
    return array


def execute_servo(dataset_name="servo"):
    # ORIGINAL FILE
    execute(dataset_name, convert)


if __name__ == "__main__":
    execute_servo()



