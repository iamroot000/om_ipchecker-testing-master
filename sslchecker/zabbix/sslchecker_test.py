from checker import *
import sys
import datetime


def checkeme(dom):

    try:
        expiration = sslchecker_notA(dom)
        date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
        get_exp = datetime.datetime.strftime(expiration, '%Y-%m-%d %H:%M:%S')
        rExp = datetime.datetime.strptime(get_exp, '%Y-%m-%d %H:%M:%S')

        daysleft =  rExp - date_now
        
        print(dom)
        print(expiration)
        print(daysleft)

        return daysleft.days

    except Exception as e:
        print(str(e))
        return sslcheckercurl(dom)

if __name__=='__main__':
   print(int(checkeme(sys.argv[1])))

