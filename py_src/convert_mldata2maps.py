import sys

def read_mldata(path):
    f = open(path,'r')
    for line in f:
        data = line.split('|')
        print data


if __name__ == '__main__':
    path = sys.argv[1]
    read_mldata(path)