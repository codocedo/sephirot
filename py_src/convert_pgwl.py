import sys
# import numpy as np
from utils import execute

def convert(pmgr):
    '''
    ALMOST THE SAME FORMAT, BUT SPACE SEPARATED RATHER THAN COMMA SEPARATED
    NO NEED OF MUCH CONVERSION, ALL CATEGORICAL OR INTEGER
    http://lib.stat.cmu.edu/jasadata/pglw00.zip
    '''
    array = []
    with open(pmgr.original_filepath, 'r') as fin:
        for line in fin:
            row = [int(i) for i in line.split()[1:]]
            array.append(row)
    return array

def execute_pgwl(dataset_name="pglw00"):
    # ORIGINAL FILE
    execute(dataset_name, convert)

if __name__ == "__main__":
    execute_pgwl()
