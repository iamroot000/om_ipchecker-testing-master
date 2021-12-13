from smtppp import *
import mysql.connector
from datetime import date, timedelta


def autosend():
    mydb = mysql.connector.connect(
        host="10.165.22.205",
        #host="10.167.11.205",
        user="yrollrei",
        passwd="s22-C350",
        database="argus_v2"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT domain FROM SSLDOMAINS_ssldomain2 WHERE daysleft < 15 and skip='no'")
    domdom = mycursor.fetchall()

    doms = list()
    print(type(domdom))
    print(domdom)
    # domains = '\n'.join(domdom)
    current_date = date.today().isoformat()
    # days_before = (date.today()-timedelta(days=7)).isoformat()
    # days_after = (date.today() + timedelta(days=6)).isoformat()

    for dom in domdom:
        list_dom = list(dom)
        for d in list_dom:
            doms.append(d)

    domains = '\n'.join(doms)
    print(domains)

    if not domains:
        print("list is empty")
    else:

        email_content = '''Hi OM,
    
        Please check the SSL of the following domain(s):\n \n''' + domains

        # email_subject = 'SSL Expiration Alert ( '+ current_date + ' to ' +   days_after+' )'

        email_subject = 'RENEWAL ALERT: Your SSL certificate is expiring in 2 weeks'

        # print(sendemail(mail_content=email_content,mail_subject=email_subject))
        #print(sendMail(['yroll.macalino@m1om.me'],'SSL Expiration Alert',email_content))


        print(sendMail(['omgroup@m1om.me'], email_subject, email_content))


if __name__ == '__main__':
    autosend()

