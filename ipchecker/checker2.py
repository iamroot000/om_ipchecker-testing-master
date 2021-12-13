import mysql.connector
import sys, socket


def checkmetoo(cleanfile):

    mydb = mysql.connector.connect(
        host="10.167.11.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor = mydb.cursor()

    lineList = [line.rstrip('\n') for line in open(cleanfile)]

    for line in lineList:
        # try:
        sql = "SELECT ip FROM gameapi_ipchecker WHERE api LIKE %s"
        val = (line,)
        mycursor.execute(sql, val)
        rVal = mycursor.fetchall()


        tstr = ''.join(rVal[0],)
        # except TypeError:
        #     print('none')

        try:
            ip_add = socket.gethostbyname(line)
            print(line + ': ' + '(old:' + tstr + ' || new:' + ip_add + ')')
            if tstr == ip_add:
                val = ('1',line)
                sql = "UPDATE gameapi_ipchecker SET result=%s WHERE api=%s"
                mycursor.execute(sql, val)
        except Exception:
            print(line + ': ' + '(old:' + tstr + ' || new:' + 'None' + ')')
    mydb.commit()




if __name__=="__main__":
    checkmetoo(sys.argv[1])

