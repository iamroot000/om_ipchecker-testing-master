import datetime, os, sys







bash_script = os.popen(

    "curl -v -sS --resolve {} {}  2>&1 | grep 'expire' | awk -F'expire date: ' {}".format(sys.argv[1],

                                                                                          sys.argv[2],

                                                                                          "'{print $2}'"))

date_str1 = bash_script.read().strip()

date_dt1 = datetime.datetime.strptime(date_str1, '%b %d %H:%M:%S %Y %Z')

date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')

expiration_date = date_dt1 - date_now

print(int(str(expiration_date).split()[0]))

