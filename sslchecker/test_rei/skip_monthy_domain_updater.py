#-*- coding: utf-8 -*-
import sys
import datetime
import mysql.connector

def updateme():



    mydb = mysql.connector.connect(
        host="10.165.22.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )
    mycursor = mydb.cursor()

    rdata = open('domain_update_email_monthly.txt')
    r = rdata.read()
    tList = list(r.split("\n"))
    tList = tList[:-1]


    for i in tList:
        try:
            y = 'yes'
            val = (y,i)
            sql = "UPDATE SSLDOMAINS_ssldomain2 SET skip=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            print(val)
            
        except Exception as e:
            print(x)
            print(e)
        try:
            www = 'www.'+ i
            y = 'yes'
            val2 = (y,www)
            sql2 = "UPDATE SSLDOMAINS_ssldomain2 SET skip=%s WHERE domain=%s"
            mycursor.execute(sql2, val2)
            print(val2)
            
        except Exception as e2:
            print(x2)
            print(e2)        

    mydb.commit()


if __name__=='__main__':
    updateme()
