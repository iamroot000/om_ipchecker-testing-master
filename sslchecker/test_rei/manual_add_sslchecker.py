#-*- coding: utf-8 -*-
import sys
import datetime
import mysql.connector
import threading
import socket
from checker import *
from testscan import portscan

def scanme(dom):

    mydb2 = mysql.connector.connect(
        host="10.165.22.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor2 = mydb2.cursor()
        
    try:
        business_unit =''
        expiration = sslchecker_notA(dom)
        date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
        get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
        rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

        daysleft =  rExp - date_now

        dayl = daysleft.days


        port80 = portscan(dom)[0]
        port443 = portscan(dom)[1]
        val = ('no','0',expiration,date_now,dayl,port80,port443,dom,business_unit)
        sql = "INSERT INTO SSLDOMAINS_ssldomain2(skip,status,expiration,date_now,daysleft,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor2.execute(sql, val)
        print(val)
        print(dom)
        print('goods')
    except:
        business_unit=''
        port80 = portscan(dom)[0]
        port443 = portscan(dom)[1]
        date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
        val = ('no','1','0','0',date_now,port80,port443,dom,business_unit)
        sql = "INSERT INTO SSLDOMAINS_ssldomain2(skip,status,expiration,daysleft,date_now,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        mycursor2.execute(sql, val)
        print(val)
        print(dom)
        print('nahhh')
    mydb2.commit()

if __name__=="__main__":
    print(scanme(sys.argv[1]))

