from checker import *
import sys
import datetime
import mysql.connector

def checkeme():

    mydb = mysql.connector.connect(
        host="10.165.22.205",
        #host="10.167.11.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT domain FROM SSLDOMAINS_ssldomain2 WHERE daysleft < 20 AND skip='no'")
    domdom = mycursor.fetchall()
    # d = {"data":[]}
    for dom in domdom:



        domstr = ''.join(dom)
        domstrl = "'"+ domstr+ "'"



        try:
            expiration = sslchecker_notA(domstr)
            date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
            get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
            rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

            daysleft =  rExp - date_now

            dayl = daysleft.days



            val = ('0',expiration,date_now,dayl,domstr)
            # sql = """ UPDATE SSLDOMAINS_ssldomain2 SET status=%s,expiration=%s, date_now=%s, daysleft=%s WHERE domain=%s """ % ('0',expiration,date_now,daysleft,domstrl)
            sql = "UPDATE SSLDOMAINS_ssldomain2 SET status=%s,expiration=%s, date_now=%s, daysleft=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            # mydb.commit()
            print(domstr)
            print('goods')

        except:
            val = ('1','0',domstr)
            sql = "UPDATE SSLDOMAINS_ssldomain2 SET status=%s, daysleft=%s WHERE domain=%s"
            mycursor.execute(sql, val)
            # mycursor.execute(sql)
            print(domstr)
            print('nahhh')
    mydb.commit()



if __name__=='__main__':
    checkeme()

