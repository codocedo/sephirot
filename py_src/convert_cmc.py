import sys
from utils import execute

def convert(pmgr):
    '''
    THIS DATSET NEEDS NO CONVERTION TO THE ENTRY OF SEPHIROT
    THIS FUNCTION JUST READS IT INTO MEMORY
    https://archive.ics.uci.edu/ml/machine-learning-databases/cmc/
    '''
    array = []
    with open(pmgr.original_filepath, 'r') as fin:
        for line in fin:
            array.append([int(i) for i in line.split(',')])
    return array

def execute_cmc(dataset_name = "cmc"):
    # ORIGINAL FILE
    execute(dataset_name, convert)

if __name__ == "__main__":
    execute_cmc()