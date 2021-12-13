#-*- coding: utf-8 -*-
from checker import *
import sys
import datetime
import mysql.connector
from testscan import portscan

def updateme():

    mydb = mysql.connector.connect(
        host="10.165.22.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT domain FROM domain_sslcheckertest WHERE skip='no'")

    domdom = mycursor.fetchall()

    for dom in domdom:
    	domstr = ''.join(dom[0]).encode('utf-8')

        try:
            expiration = sslchecker_notA(domstr)
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
            rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

            daysleft =  rExp - date_now

            dayl = daysleft.days

            port80 = portscan(domstr)[0]
            port443 = portscan(domstr)[1]
            val = ('0',expiration,date_now,dayl,port80,port443,domstr)
            sql = "UPDATE domain_sslcheckertest SET status=%s, expiration=%s, date_now=%s, daysleft=%s, port80=%s, port443=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            print(val)
            print('Fuiyohhhh')
        except:
            port80 = portscan(domstr)[0]
            port443 = portscan(domstr)[1]
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            val = ('1','0','0',date_now,port80,port443,domstr)
            sql = "UPDATE domain_sslcheckertest SET status=%s, expiration=%s, daysleft=%s, date_now=%s, port80=%s, port443=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            print(val)
            print('Haiyahhhh')
	mydb.commit()


if __name__=='__main__':
    updateme()

