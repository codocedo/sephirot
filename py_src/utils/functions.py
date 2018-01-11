import sys
from math import fabs
import time

'''
    Takes function f and execute it using *args
    The first argument should be a path to some file
    It measures the execution time and writes it to args[0]+'.time'
'''
def measure_exec_time(f,path,*args):
    start = time.time()
    ret = f(*args)
    stop = time.time()
    with open(path+".time.txt",'w') as f:
        f.write("%s\n"%(stop - start))
    return ret

def write_cfg(path,name,type=6,contextPath="",more="",empty_value=""):
    transpose = "false"
    if type == 6:
        transpose = "true"
    with open(path,'w') as f:
        str="[sephirot]\ncontext_path = datasets/{0}/data/{0}.ijgs.{2}.ctx\nlattice_path = datasets/{0}/results/{0}.ijgs.{2}.zephyr\ntype = {1}\ntranspose = {4}\n\n[tblocks]\nmrows = 2\nthetas = true\nthetas_file = datasets/{0}/data/original/{0}.ijgs.thetas.txt\n{3}\n"
        f.write(str.format(name,type,contextPath,more,transpose))
    print "\t->Configuration file written to:", path

# FOR WHEN THE ENTRY TABLE IS A MATRIX
def save_ctx(path, table):
    with open(path,'w') as f:
        for i in table:
            s = str(int(i[0]))
            for j in range(1,len(i)):
                s+=","+str(int(i[j]))
            f.write(s+'\n')

# FOR WHEN THE ENTRY TABLE IS ACTUALLY A DICTIONARY AND NOT A MATRIX
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
            
# READS A SINGLE LINE FILE WHICH CONTAINS THE THETA VALUES FOR EACH DIMENSION
def read_thetas(path):
    with open(path,'r') as f:
        lines = f.readlines()
        return [float(theta) for theta in lines[0].strip().split(',')]



def binnarize(path,data,thetas,withFile = False,empty_value=0):
    if not withFile:
        table,table_clear = make_it_clear(data,thetas,empty_value)
        save_formal_context(path.format(''),table)
        print "\t->Formal Context file written in",path.format('')
        save_formal_context(path.format('cl'),table_clear)
        print "\t->Clarified context file written in",path.format('cl')
    else:
        f1 = open(path.format(''),'w')
        f2 = open(path.format('cl'),'w')
        make_it_clear_with_file(data,thetas,f1,f2,empty_value)
        print "\t->Formal Context file written in",path.format('')
        print "\t->Clarified context file written in",path.format('cl')


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
            print '\r\t->Binnarazing with file things (%0.2f)'%(it*100.0/total),'%',
            sys.stdout.flush()
            it+=1.0
            newrow = []
            for k,z in enumerate(abs(x-y)):
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
            print '\r\t->Binnarazing things (%0.2f)'%(it*100.0/total),'%',
            sys.stdout.flush()
            it+=1.0
            aid = (i,j)
            newrow = []
            for k,z in enumerate(abs(x-y)):
                if x[k] != empty_value and y[k] != empty_value and z <= thetas[k]:
                    newrow.append(k)

            if str(newrow) not in uniques:
                table_clear[aid]=newrow
                uniques.add(str(newrow))
            table[aid] = newrow
    print ''
    return table,table_clear


def save_data2context(data,path):
    f = open(path,'w')
    for i in data:
        f.write(str(str([float(j) for j in i]))[1:-1].replace(' ','')+'\n')
    f.close()
