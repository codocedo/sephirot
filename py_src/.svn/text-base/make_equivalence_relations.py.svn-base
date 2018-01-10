#!/usr/bin/python
import sys
from numpy import array

def read_dataset(path):
    f = open(path,'r')
    data = f.read().split('\n')
    a = [d.split(',') for d in data if d!='']
    b = []
    for i in a:
        b.append([int(j) for j in i])
    return array(b)

def vect2str(vec):
    out = ''
    for i in vec:
        out+=str(i)+','
    return out[:len(out)-1]

if __name__ == "__main__":
    user=10
    movie=10
    matrix = read_dataset(sys.argv[1])
    min_sup = int(sys.argv[2])
    nusers,nmovies=matrix.shape
    result = 0
    f = open('equivalence_relation_output_ms'+str(min_sup)+'.ctx','w')
    g = open('equivalence_relation_map_ms'+str(min_sup)+'.ctx','w')
    for i in range(nusers):
        print i,result
        for j in range(i+1,nusers):
            x =matrix[i]-matrix[j]
            y = ((matrix[i] != 0) + (matrix[j] != 0))
            z = []
            for k in range(len(x)):
                if y[k] and x[k] == 0:
                    z.append(k)
            if len(z) >= min_sup:
                f.write(vect2str(z)+'\n')
                g.write(str(i)+','+str(j)+'\n')
                #print z[:len(z)-1]
                result +=1
            #print k,'(',matrix[i][k],',',matrix[j][k],'),',
            #print ''

    print len(z)
