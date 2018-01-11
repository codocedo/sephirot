import sys
from utils import execute

def convert(pmgr):
    '''
    CONVERT FROM THE FORMAT OF DIAGNOSIS
    contains yes or not which are converted to binary elements.
    THE FIRST ELEMENT IS A NUMBER, NEEDS convertions
    https://archive.ics.uci.edu/ml/machine-learning-databases/acute/
    '''
    question_idx = {'yes':2, 'no':1}
    array = []
    with open(pmgr.original_filepath, 'r') as fin:
        for line in fin:
            row = []
            data = line.replace('\n', '').split('\t')
            row.append(float(data[0].replace(',', '.')))
            row.extend([question_idx[i] for i in data[1:]])
            array.append(row)
    return array

def execute_diagnosis(dataset_name="diagnosis"):
    # ORIGINAL FILE
    execute(dataset_name, convert)

if __name__ == "__main__":
    execute_diagnosis()
