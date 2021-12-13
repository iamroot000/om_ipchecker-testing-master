from checker import *
import sys
import datetime
import mysql.connector

def checkeme():

    mydb = mysql.connector.connect(
        #host="10.167.11.205",
        host="10.165.22.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT domain FROM cdn_cdndomain")
    domdom = mycursor.fetchall()
    # d = {"data":[]}
    for dom in domdom:



        domstr = ''.join(dom)
        domstrl = "'"+ domstr+ "'"



        try:
            checkaud = domainaudit(domstr)



            val = (checkaud,domstr)
            sql = "UPDATE cdn_cdndomain SET audit=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            print(val)
            print('goods')

        except:
            val = ('No',domstr)
            sql = "UPDATE cdn_cdndomain SET audit=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            print(val)
            print('nahhh')
    mydb.commit()



if __name__=='__main__':
    checkeme()
