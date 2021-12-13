import sys

def listme(apilist):

    content = open(apilist,'r').readlines()
    content_set = set(content)
    cleandata = open('clearapi.txt','w')

    for line in content_set:
        nline = line.strip('https://')
        tline = nline.partition('/')[0].rstrip()
        cleandata.write(tline.partition(':')[0].rstrip() + '\n')

if __name__=="__main__":
    listme(sys.argv[1])