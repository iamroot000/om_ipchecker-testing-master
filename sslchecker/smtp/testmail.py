from smtppp import *
import mysql.connector
from datetime import date, timedelta


def autosend():


    email_content = '''Test'''

    # email_subject = 'SSL Expiration Alert ( '+ current_date + ' to ' +   days_after+' )'

    email_subject = 'TEST MAIL'

    # print(sendemail(mail_content=email_content,mail_subject=email_subject))
    # print(sendMail(['nikko.aratan@m1om.me'],'SSL Expiration Alert',email_content))


    print(sendMail(['nikko.aratan@m1om.me'], email_subject, email_content))


if __name__ == '__main__':
    autosend()

