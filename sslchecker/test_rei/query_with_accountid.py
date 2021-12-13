#-*- coding: utf-8 -*-
import sys
import datetime
import mysql.connector
import threading
import socket
from checker import *
from testscan import portscan

def scanme():


    mydb = mysql.connector.connect(
        host="10.165.22.205",
        user="argususer",
        passwd="S22c350",
        database="argus"
    )

    mycursor = mydb.cursor()

    mydb2 = mysql.connector.connect(
        host="10.165.22.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor2 = mydb2.cursor()

    mycursor.execute("SELECT domains_domain.domain, domains_account.business_unit_id FROM domains_domain, domains_account WHERE domains_domain.account_id = domains_account.username")
    domdom = mycursor.fetchall()
    print('hey')
    for dom in domdom:
        
        dom_name_str = ''.join(dom[0]).encode('utf-8')
        dom_bu_str = ''.join(dom[1]).encode('utf-8')
        www_dom = 'www.'+ dom_name_str.decode('utf-8')
        print(www_dom)

        print(dom_name_str,dom_bu_str)


        try:
            expiration = sslchecker_notA(dom_name_str)
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
            rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

            daysleft =  rExp - date_now

            dayl = daysleft.days


            port80 = portscan(dom_name_str)[0]
            port443 = portscan(dom_name_str)[1]
            val = ('no','0',expiration,date_now,dayl,port80,port443,dom_name_str,dom_bu_str)
            sql = "INSERT INTO domain_sslcheckertest(skip,status,expiration,date_now,daysleft,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor2.execute(sql, val)
            print(val)
            print(dom_name_str)
            print('goods')
        except:
            port80 = portscan(dom_name_str)[0]
            port443 = portscan(dom_name_str)[1]
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            val = ('no','1','0','0',date_now,port80,port443,dom_name_str,dom_bu_str)
            sql = "INSERT INTO domain_sslcheckertest(skip,status,expiration,daysleft,date_now,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor2.execute(sql, val)
            print(val)
            print(dom_name_str)
            print('nahhh')

        try:
            expiration = sslchecker_notA(www_dom)
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
            rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

            daysleft =  rExp - date_now

            dayl = daysleft.days


            port80 = portscan(www_dom)[0]
            port443 = portscan(www_dom)[1]
            val = ('no','0',expiration,date_now,dayl,port80,port443,www_dom,dom_bu_str)
            sql = "INSERT INTO domain_sslcheckertest(skip,status,expiration,date_now,daysleft,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor2.execute(sql, val)
            print(val)
            print(www_dom)
            print('goods')
        except:
            port80 = portscan(www_dom)[0]
            port443 = portscan(www_dom)[1]
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            val = ('no','1','0','0',date_now,port80,port443,www_dom,dom_bu_str)
            sql = "INSERT INTO domain_sslcheckertest(skip,status,expiration,daysleft,date_now,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            mycursor2.execute(sql, val)
            print(val)
            print(www_dom)
            print('nahhh')
    mydb2.commit()

if __name__=="__main__":
    scanme()

