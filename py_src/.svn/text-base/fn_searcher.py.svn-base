import json
import sys

lattice = {}
children={}

def print_childs(aid,depth=1):
    print "-"*depth,lattice[aid]['Extent']
    for x in children[aid]:
        if x in children:
            print_childs(x,depth+1)


def get_childs(aid,depth=1):
    out = set([])
    out.update(children[aid])
    for x in children[aid]:
        if x in children:
            out.update(get_childs(x,depth+1))
    return out


def read_lattice(lat_path):
    f = open(lat_path,'r')
    raw = f.read()
    data = json.loads(raw)
    suspicious = []
    for i in data['ConceptLattice']:
        lattice[i['id']] = i
        k =str(i['id'])
        
        if i['Stability']> 1:
            suspicious.append(i['id'])
        for e in i['Parents']:
            x = children.get(e,[])
            x.append(i['id'])
            children[e]=x

    for s in suspicious:
        print '\n',lattice[s]['Extent'],"@",lattice[s]['Stability'],'-',lattice[s]['Count']
        
        sextent = set(lattice[children[s][0]]['Extent'])
        
        for ch in children[s][1:]:
            print sextent,'intersection',lattice[ch]['Extent']
            sextent = sextent.intersection(set(lattice[ch]['Extent']))

        print 'FN:',set(lattice[s]['Extent']).difference(sextent),'---->',sextent
        childs = [(len(lattice[x]['Extent']),lattice[x]['Extent']) for x in get_childs(s)]
        childs.sort()
        print childs,len(get_childs(s)),'\n'




if __name__=="__main__":
    read_lattice(sys.argv[1])