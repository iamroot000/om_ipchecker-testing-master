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

    mycursor.execute("SELECT domain, business_unit FROM SSLDOMAINS_ssldomain2 WHERE skip='no' AND port443='open' AND status='1'")
    domdom = mycursor.fetchall()

    doms = list()


    for dom in domdom:
		strdom = str(dom[0].encode('utf-8')) + ' - ' + str(dom[1].encode('utf-8'))
		doms.append(strdom)

    domains = '\n'.join(doms)
    print(domains)

    if not domains:
        email_content = '''Hi OM,
    
        All domains are fine.\n \n'''


        email_subject = 'Monthly Task: Port443 Open but no SSL Cert'

       	#print(sendMail(['nikko.aratan@m1om.me'],email_subject,email_content))


        print(sendMail(['omgroup@m1om.me'], email_subject, email_content))
    else:

        email_content = '''Hi OM,
    
        Please verify the following domain(s):\n \n''' + domains


        email_subject = 'Monthly Task: Port443 Open but no SSL Cert'

       	#print(sendMail(['yroll.macalino@m1om.me'],email_subject,email_content))


        print(sendMail(['omgroup@m1om.me'], email_subject, email_content))


if __name__ == '__main__':
    autosend()

