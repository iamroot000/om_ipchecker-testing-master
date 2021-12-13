import sys
import sqlite3

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('connected')
    except Exception as e:
        print(e)

    return conn

def check(api):
    db_file = 'ipchecker.sqlite3'
    conn = create_connection(db_file)
    cur = conn.cursor()
    try:
        cur.execute("SELECT result FROM apichecker_table WHERE api LIKE '{}'".format(api))
        ret = cur.fetchone()
        tstr = ''.join(ret)
        if tstr == '1':
            return 1
        else:
            return 0
    except:
        return 0

if __name__=='__main__':
    print(check(sys.argv[1]))