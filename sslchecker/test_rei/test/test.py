
from checker import *
import sys
import datetime
import mysql.connector

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
    mycursor2.execute("SELECT domain FROM domain_sslcheckertest")

    domdom1 = mycursor.fetchall()
    domdom2 = mycursor2.fetchall()



    for dom in domdom1:
        print(dom)
        print(type(dom))
        domstr = ''.join(dom).encode('utf-8')
        # print(type(domstr))
        print
        #if domstr in domdom2:
            # print('meron')
        #else:
            # print('wala')



    #     domstr = ''.join(dom)
    #     domstrl = "'"+ domstr+ "'"



    #     try:
    #         expiration = sslchecker_notA(domstr)
    #         date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
    #         get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
    #         rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

    #         daysleft =  rExp - date_now

    #         dayl = daysleft.days



    #         val = ('0',expiration,date_now,dayl,domstr)
    #         # sql = """ UPDATE SSLDOMAINS_ssldomain2 SET status=%s,expiration=%s, date_now=%s, daysleft=%s WHERE domain=%s """ % ('0',expiration,date_now,daysleft,domstrl)
    #         sql = "UPDATE SSLDOMAINS_ssldomain2 SET status=%s,expiration=%s, date_now=%s, daysleft=%s WHERE domain=%s"
    #         mycursor.execute(sql, val)
    #         # mydb.commit()
    #         print(domstr)
    #         print('goods')

    #     except:
    #         val = ('1','0',domstr)
    #         sql = "UPDATE SSLDOMAINS_ssldomain2 SET status=%s, daysleft=%s WHERE domain=%s"
    #         mycursor.execute(sql, val)
    #         # mycursor.execute(sql)
    #         print(domstr)
    #         print('nahhh')
    # mydb.commit()



if __name__=='__main__':
    updateme()

