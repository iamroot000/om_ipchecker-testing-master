import sqlite3
import sys, socket


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('connected')
    except Exception as e:
        print(e)

    return conn


def checkme(cleanfile):

    lineList = [line.rstrip('\n') for line in open(cleanfile)]
    db_file = 'ipchecker.sqlite3'
    conn = create_connection(db_file)

    cur = conn.cursor()

    for line in lineList:
        try:
            ip_add = socket.gethostbyname(line)
            print(line+': '+ip_add)
            hey = (line,ip_add,'0')
            try:
                cur.execute('INSERT INTO apichecker_table(api,ip,result) VALUES(?,?,?)',hey)
                conn.commit()
            except Exception as e:
                print(e)
        except:
            oy = (line,'None','0')
            cur.execute('INSERT INTO apichecker_table(api,ip,result) VALUES(?,?,?)',oy)

    cur.close()

if __name__=="__main__":
    # checkmetoo(sys.argv[1])
    checkme(sys.argv[1])
    # create_connection()