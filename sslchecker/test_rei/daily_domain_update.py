#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from checker import *
import sys
import datetime
import mysql.connector
from testscan import portscan


def updateme():

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
    mycursor2.execute("SELECT domain FROM SSLDOMAINS_ssldomain2")

    domdom1 = mycursor.fetchall()
    domdom2 = mycursor2.fetchall()

    domlist2 = list()

    for x in domdom2:
        xdom = ''.join(x[0]).encode('utf-8')
        domlist2.append(xdom)

    for dom in domdom1:
        domstr = ''.join(dom[0]).encode('utf-8')
        bu_str = ''.join(dom[1]).encode('utf-8')
        www_dom = 'www.'.encode('utf-8')+ domstr
        if domstr not in domlist2:
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
                val = ('no','0',expiration,date_now,dayl,port80,port443,domstr,bu_str)
                sql = "INSERT INTO SSLDOMAINS_ssldomain2(skip,status,expiration,date_now,daysleft,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor2.execute(sql, val)
                print(val)
                print('goods')
            except:
                port80 = portscan(domstr)[0]
                port443 = portscan(domstr)[1]
                date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
                val = ('yes','1','0','0',date_now,port80,port443,domstr,bu_str)
                sql = "INSERT INTO SSLDOMAINS_ssldomain2(skip,status,expiration,daysleft,date_now,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor2.execute(sql, val)
                print(val)
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
                val = ('no','0',expiration,date_now,dayl,port80,port443,www_dom,bu_str)
                sql = "INSERT INTO SSLDOMAINS_ssldomain2(skip,status,expiration,date_now,daysleft,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor2.execute(sql, val)
                print(val)
                print(www_dom)
                print('goods')
            except:
                port80 = portscan(www_dom)[0]
                port443 = portscan(www_dom)[1]
                date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
                val = ('yes','1','0','0',date_now,port80,port443,www_dom,bu_str)
                sql = "INSERT INTO SSLDOMAINS_ssldomain2(skip,status,expiration,daysleft,date_now,port80,port443,domain,business_unit) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                mycursor2.execute(sql, val)
                print(val)
                print(www_dom)
                print('nahhh')
    mydb2.commit()


if __name__=='__main__':
    updateme()

