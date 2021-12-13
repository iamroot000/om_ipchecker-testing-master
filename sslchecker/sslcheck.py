from checker import *
import sys
import datetime
import mysql.connector

def checkeme(dList):

    mydb = mysql.connector.connect(
        #host="10.167.11.205",
        host="10.165.22.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor = mydb.cursor()

    lineList = [line.rstrip('\n') for line in open(dList)]

    for line in lineList:
        print(line)
        try:
            expiration = sslchecker_notA(line)
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
            rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

            daysleft =  rExp - date_now
            val = (line,expiration,daysleft,date_now,'0')
            sql = "INSERT INTO SSLDOMAINS_ssldomain2(domain,expiration,daysleft,date_now,status) VALUES(%s, %s, %s, %s, %s)"
            mycursor.execute(sql, val)
            print(expiration)
        print(daysleft)

        except:
            val = (line,'---','0',date_now,'1')
            sql = "INSERT INTO SSLDOMAINS_ssldomain2(domain,expiration,daysleft,date_now,status) VALUES(%s, %s, %s, %s, %s)"
            mycursor.execute(sql, val)


if __name__=='__main__':
    checkeme(sys.argv[1])                           
