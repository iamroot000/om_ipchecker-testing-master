import sys

def listme(apilist):

    content = open(apilist,'r').readlines()
    content_set = set(content)
    cleandata = open('domains.txt','w')

    for line in content_set:
        nline = line.strip()
        cleandata.write(nline + '\n')
    print('done')

if __name__=="__main__":
    listme(sys.argv[1])

