import mysql.connector
import sys, socket


def checkme(cleanfile):


    mydb = mysql.connector.connect(
        host="10.167.11.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor = mydb.cursor()

    lineList = [line.rstrip('\n') for line in open(cleanfile)]

    for line in lineList:
        try:
            ip_add = socket.gethostbyname(line)
            print(line+': '+ip_add)
            val = (line,ip_add,'0')
            try:
                sql = "INSERT INTO gameapi_ipchecker(api,ip,result) VALUES(%s, %s, %s)"
                mycursor.execute(sql, val)

            except Exception as e:
                print(e)
        except:
            val = (line,'None','0')
            sql = "INSERT INTO gameapi_ipchecker(api,ip,result) VALUES(%s, %s, %s)"
            mycursor.execute(sql, val)

    mydb.commit()

if __name__=="__main__":
    # checkmetoo(sys.argv[1])
    checkme(sys.argv[1])
    # create_connection()
