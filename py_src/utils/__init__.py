import sys
from math import fabs
import time
from itertools import imap

PATHS = {
    "dataset_path": "datasets/{}/",
    "inner_data_path": "data/",
    "inner_ini_path": "ini/",
    "inner_results_path": "results/"
}

TEMPLATES = {
    "original_file": "original/{0}.original.txt",
    "tb_file": "{0}.{1}.ctx",
    "ini_file":"{0}.{1}.ini",
    "map_file":"{0}.map.txt",
    "thetas_file":"original/{0}.thetas.txt",
    "lat_file":"{0}.{1}.zephyr"
}

INI_TEMPLATE = """[sephirot]
context_path = {0}
lattice_path = {1}
type = {2}
transpose = {3}
"""

INI_TEMPLATE_PS = """
[tblocks]
mrows = 2
thetas = true
thetas_file = {0}
{1}
"""

class PathManager(object):
    def __init__(self, dataset_name):
        self.dataset_name = dataset_name
    @property
    def data_path(self):
        return PATHS['dataset_path'].format(self.dataset_name) + PATHS['inner_data_path']
    @property
    def ini_path(self):
        return PATHS['dataset_path'].format(self.dataset_name) + PATHS['inner_ini_path']
    @property
    def results_path(self):
        return PATHS['dataset_path'].format(self.dataset_name) + PATHS['inner_results_path']
    @property
    def original_filename(self):
        return TEMPLATES['original_file'].format(self.dataset_name)
    @property
    def original_filepath(self):
        return self.data_path + self.original_filename
    @property
    def thetas_filename(self):
        return TEMPLATES['thetas_file'].format(self.dataset_name)
    @property
    def thetas_filepath(self):
        return self.data_path + self.thetas_filename
    @property
    def tb_filename(self):
        return TEMPLATES['tb_file'].format(self.dataset_name, 'tb')
    @property
    def tb_filepath(self):
        return self.data_path + self.tb_filename
    @property
    def context_filename(self):
        return TEMPLATES['tb_file'].format(self.dataset_name, 'context')
    @property
    def context_filepath(self):
        return self.data_path + self.context_filename
    @property
    def clarified_context_filename(self):
        return TEMPLATES['tb_file'].format(self.dataset_name, 'clarified_context')
    @property
    def clarified_context_filepath(self):
        return self.data_path + self.clarified_context_filename
    @property
    def tb_ini_filename(self):
        return TEMPLATES['ini_file'].format(self.dataset_name, 'tb')
    @property
    def tb_ini_filepath(self):
        return self.ini_path + self.tb_ini_filename
    @property
    def tb_lat_filename(self):
        return TEMPLATES['lat_file'].format(self.dataset_name, 'tb')
    @property
    def tb_lat_filepath(self):
        return self.results_path + self.tb_lat_filename
    @property
    def attribute_map_filename(self):
        return TEMPLATES['map_file'].format(self.dataset_name)
    @property
    def attribute_map_filepath(self):
        return self.data_path + self.attribute_map_filename
    @property
    def context_ini_filename(self):
        return TEMPLATES['ini_file'].format(self.dataset_name, 'context')
    @property
    def context_ini_filepath(self):
        return self.ini_path + self.context_ini_filename
    @property
    def clarified_context_ini_filename(self):
        return TEMPLATES['ini_file'].format(self.dataset_name, 'clarified_context')
    @property
    def clarified_context_ini_filepath(self):
        return self.ini_path + self.clarified_context_ini_filename
    @property
    def context_lat_filename(self):
        return TEMPLATES['lat_file'].format(self.dataset_name, 'context')
    @property
    def context_lat_filepath(self):
        return self.results_path + self.context_lat_filename
    @property
    def clarified_context_lat_filename(self):
        return TEMPLATES['lat_file'].format(self.dataset_name, 'clarified_context')
    @property
    def clarified_context_lat_filepath(self):
        return self.results_path + self.clarified_context_lat_filename



def measure_exec_time(f, path, *args):
    '''
    Takes function f and execute it using *args
    The first argument should be a path to some file
    It measures the execution time and writes it to args[0]+'.time'
    '''
    start = time.time()
    ret = f(*args)
    stop = time.time()
    with open(path+".time.txt",'w') as f:
        f.write("%s\n"%(stop - start))
    return ret

def save_map(path, attribute_map):
    '''
    Attribute map is a dictionary of strings to integers
    This method generates a file to store them
    '''
    with open(path, 'w') as f:
        m = [(j, i) for i, j in attribute_map.items()]
        m.sort()
        for j, i in m:
            f.write(str(j)+"\t"+str(i)+"\n")

def write_ini(ini_path, ctx_path, lat_path, ctx_type=6, thetas_path='', more=''):
    transpose = "false"
    if ctx_type == 6:
        transpose = "true"
    with open(ini_path, 'w') as f:
        f.write(
            INI_TEMPLATE.format(ctx_path, lat_path, ctx_type, transpose)
        )
        if ctx_type == 6:
            f.write(
                INI_TEMPLATE_PS.format(thetas_path, more)
            )   
    print "\t-> Configuration file written to:", ini_path

# FOR WHEN THE ENTRY TABLE IS A MATRIX
def save_ctx(path, table):
    with open(path,'w') as fout: 
        for i in table:
            fout.write(','.join([str(j) for j in i])+'\n')

# FOR WHEN THE ENTRY TABLE IS A DICTIONARY AND NOT A MATRIX
def save_formal_context(path,table):
    with open(path,'w') as f:
        keys = table.keys()
        keys.sort()
        for k in keys:
            if len(table[k]) > 0:
                i = table[k]
                s = str(int(i[0]))
                for j in range(1,len(i)):
                    s+=","+str(int(i[j]))
                f.write(s+'\n')

def read_thetas(path):
    '''
    READS A SINGLE LINE FILE WHICH CONTAINS THE THETA VALUES FOR EACH DIMENSION
    '''
    with open(path, 'r') as f:
        lines = f.readlines()
        return [float(theta) for theta in lines[0].strip().split(',')]

def binarize(pmgr, data, thetas, withFile = False, empty_value=0):
    if not withFile:
        table, table_clear = make_it_clear(data, thetas, empty_value)
        save_formal_context(pmgr.context_filepath, table)
        save_formal_context(pmgr.clarified_context_filepath, table_clear)
    else:
        f1 = open(pmgr.context_filepath, 'w')
        f2 = open(pmgr.clarified_context_filepath, 'w')
        make_it_clear_with_file(data, thetas, f1, f2, empty_value)

    print "\t-> Formal Context file written in: ", pmgr.context_filepath
    print "\t-> Clarified context file written in: ", pmgr.clarified_context_filepath

def binnarize(path, data, thetas, withFile = False, empty_value=0):
    if not withFile:
        table,table_clear = make_it_clear(data, thetas, empty_value)
        save_formal_context(path.format(''),table)
        print "\t-> Formal Context file written in",path.format('')
        save_formal_context(path.format('cl'),table_clear)
        print "\t-> Clarified context file written in",path.format('cl')
    else:
        f1 = open(path.format(''),'w')
        f2 = open(path.format('cl'),'w')
        make_it_clear_with_file(data,thetas,f1,f2,empty_value)
        print "\t-> Formal Context file written in",path.format('')
        print "\t-> Clarified context file written in",path.format('cl')


def make_it_tricontext(data,thetas):
    s=""
    for j,y in enumerate(data.T):
        for i,x in enumerate(y):
            trip = str(j)+" "+str(i)+" "
            for k,l in enumerate(y[i+1:]):
                if (fabs(x-l) <= thetas[j]):
                    s+=trip+str(k+i+1)+"\n"
                #print i,k+i+1, x, l

    return s



def make_it_clear_with_file(data,thetas,f1,f2,empty_value=0):
    uniques = set([])
    total = (len(data)**2)/2 - len(data)
    print total
    it = 0.0
    for i,x in enumerate(data):
        for j,y in enumerate(data[i+1:]):
            print '\r\t-> Binnarazing with file things (%0.2f)'%(it*100.0/total),'%',
            sys.stdout.flush()
            it+=1.0
            newrow = []
            for k,z in enumerate(imap(lambda s: abs(s[0]-s[1]), zip(x, y))):# [abs(a-b) for a, b in zip(x, y)]):
                if x[k] != empty_value and y[k] != empty_value and z <= thetas[k]:                    
                    newrow.append(k)
            newrow = str(newrow)[1:-1].replace(' ','')+'\n'
            if newrow != "":
                if newrow not in uniques:
                    f2.write(newrow)
                    uniques.add(newrow)
                f1.write(newrow)
    print ''


def make_it_clear(data,thetas,empty_value=0):
    table = {}
    table_clear = {}
    uniques = set([])
    total = (len(data)**2)/2 - len(data)
    it = 0.0
    
    for i,x in enumerate(data):
        for j,y in enumerate(data[i+1:]):
            print '\r\t-> Binarazing things (%0.2f)'%(it*100.0/total),'%',
            sys.stdout.flush()
            it+=1.0
            aid = (i,j)
            newrow = []
            for k,z in enumerate(imap(lambda s: abs(s[0]-s[1]), zip(x, y))):
                if x[k] != empty_value and y[k] != empty_value and z <= thetas[k]:
                    newrow.append(k)

            if str(newrow) not in uniques:
                table_clear[aid]=newrow
                uniques.add(str(newrow))
            table[aid] = newrow
    print ''
    return table, table_clear


def save_data2context(data,path):
    f = open(path,'w')
    for i in data:
        f.write(str(str([float(j) for j in i]))[1:-1].replace(' ','')+'\n')
    f.close()



def execute(dataset_name, convert):
    """
    Executes the conversion of format, reads the original dataset
    and generates input files for SEPHIROT.
    """
    # ************************************************
    # CONFIGURE PATHS 
    # ************************************************
    pmgr = PathManager(dataset_name)
    
    print "\nPROCESSING {0} DATASET IN: {1}".format(
        dataset_name,
        pmgr.original_filepath
    )

    if "/" in sys.argv[0]:
        print "ERROR: Please execute the script from within the scripts folder"
        exit()

    # ************************************************
    # CONVERT ORIGINAL FILE INTO ARRAY OF VALUES 
    # THAT CAN BE COMPARED USING A SIMILARITY VALUE
    # THIS WILL BE FED TO PATTERN STRUCTURES MINER
    # ************************************************
    data = convert(pmgr)

    # EXECUTE MEASURING TIME
    # THE METHOD TO SAVE THE CONTEXT MAY VARY
    measure_exec_time(
        save_ctx,
        pmgr.tb_filepath,
        pmgr.tb_filepath,
        data
    )
    print "\t-> Context file written in " + pmgr.tb_filepath
    
    # WRITE INI FILES FOR SEPHIROT FOR PATTERN STRUCTURES
    write_ini(
        pmgr.tb_ini_filepath,
        pmgr.tb_filepath,
        pmgr.tb_lat_filepath,
        pmgr.thetas_filepath,
        6,
        more="empty_value = -1\n"
    )


    # ************************************************
    # BINARIZATION PROCESS
    # ************************************************
    thetas = read_thetas(pmgr.thetas_filepath)

    # EXECUTE BINARIZATION MEASURING TIME
    # BINARIZATION WRITES BOTH THE CONTEXT AND CLARIFIED CONTEXT
    measure_exec_time(
        binarize,
        pmgr.context_filepath,
        pmgr,
        data,
        thetas,
        False,
        -1
    )

    # WRITE INI FILES FOR SEPHIROT FOR FCA
    write_ini(
        pmgr.context_ini_filepath,
        pmgr.context_filepath,
        pmgr.context_lat_filepath,
        0
    )
    # WRITE INI FILES FOR SEPHIROT FOR FCA WITH CLARIFIED CONTEXT
    write_ini(
        pmgr.clarified_context_ini_filepath,
        pmgr.clarified_context_filepath,
        pmgr.clarified_context_lat_filepath,
        0
    )