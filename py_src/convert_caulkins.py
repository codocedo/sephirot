import sys

from utils import PathManager, execute, save_map

#from functions import make_it_clear

# 0: numerical 1: categorical 2: float
data_type = [0,1,1,1,2,1,2,1,2,2,2,2,2,2,2]
donotuse = [4,5,7]

'''
    The "Drug" field gives the drug type cited in the original data; "Drg Cde"
    indicates its coding into one of the ten types of drugs analyzed.
    
    The "Raw Qty" and "Units" field give the quantity as reported in the original
    data.  "Qin Grams" gives converts this quantity (or transaction size) into
    grams.
    
    "Low $" and "High $" give the bottom and top of the range of prices listed in
    the original data.  "Avg. $" is the midpoint of this range.  Similarly for "Lo
    Pur", "Hi Pur", and "Av Pur", all ranging between 0 and 100.  "Pure Qty" is
    the "Qin Grams" times the "Av Pur" divided by 100.
'''
# I DO NOT USE BOTH, WEIGHT AND GRAMS REPRESENTATION.

def convert(pmgr):
    f = open(pmgr.original_filepath, 'r')
    attribute_map = {}

    array = []
    for line in f:
        x=[i for i in line.strip().split('\t')]
        if (len(x) > 1):
            array.append(x)
    f.close()
    matrix = []
    for i in array:
        row = []
        for j in [k for k in range(len(i)) if k not in donotuse]:
            if (data_type[j] != 1):
                row.append (float(i[j]))
            else:
                x = attribute_map.get(i[j],len(attribute_map))
                attribute_map[i[j]] = x
                row.append(x)
        matrix.append(row)

    save_map(pmgr.attribute_map_filepath, attribute_map)
    print "\t-> Map of categorical attributes written in {}".format(pmgr.attribute_map_filepath)
    return matrix

def execute_caulkins(dataset_name="caulkins"):
    """
    Executes the conversion of format, reads the original dataset
    and generates input files for SEPHIROT.
    """
    execute(dataset_name, convert)

if __name__ == "__main__":
    # ORIGINAL FILE
    execute_caulkins()
    
    





