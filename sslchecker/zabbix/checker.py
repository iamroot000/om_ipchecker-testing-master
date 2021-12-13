import os, ipaddress, sys, time
import socket, ssl, datetime
from pytz import timezone

def _resolveip(mydomain):
    out_list = []
    _domain = mydomain.replace('https://', '').replace('http://', '').strip()
    _dns = "8.8.8.8"
    _out = os.popen("nslookup {} {}".format(_domain, _dns))
    for i in _out.read().split('\n'):
        if len(i) != 0:
            out_list.append(i)

    try:
        # print(out_list[-1].split('Address:')[-1].strip())
        nsnum = -1
        myip = ipaddress.ip_address(unicode(out_list[nsnum].split('Address:')[-1].strip()))
        while True:
            if len(str(myip).split(':')) > 1:
                nsnum = nsnum - 2
                myip = ipaddress.ip_address(unicode(out_list[nsnum].split('Address:')[-1].strip()))
                # print(nsnum)
            else:
                return [myip]
    except Exception as e:
        # print(str(e))
        return []

def sslcheckercurl(mydomain):
    for iii in range(0,3):
        _ip = _resolveip(mydomain)
        # print(_ip)
        if len(_ip) == 1:
            _cmd = os.popen("curl -vI https://{0} --resolve {0}:443:{1} --max-time 10 2>&1 | grep 'expire date:'".format(mydomain, _ip[-1]))
            _cmdout = _cmd.read().split('\n')
            # print(_cmdout)
            if len(_cmdout) == 2:
                for i in _cmdout:
                    if len(i) != 0:
                        date_str1 = i.split('date:')[-1].strip()
                        date_dt1 = datetime.datetime.strptime(date_str1, '%b %d %H:%M:%S %Y %Z')
                        date_now_fmt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        date_now = datetime.datetime.strptime(date_now_fmt, '%Y-%m-%d %H:%M:%S')
                        expiration_date = date_dt1 - date_now
                        return int(str(expiration_date).split()[0])

        else:
            # print("no IP")
            return 0
        time.sleep(5)
    return 0

def sslcheckerOut(dom, port=443, timeout=10, value=None):
    sock = socket.create_connection((dom, port), timeout=timeout)
    context = ssl.create_default_context()
    sslsock =  context.wrap_socket(sock, server_hostname=dom)
    getssl = sslsock.getpeercert()
    changedt_format = getssl[value]
    to_format = ssl.cert_time_to_seconds(changedt_format)
    new_ssldt_format = datetime.datetime.fromtimestamp(to_format)
    return new_ssldt_format

def sslchecker_notB(dom):
    return sslcheckerOut(dom, value="notBefore")


def sslchecker_notA(dom):
    return sslcheckerOut(dom, value="notAfter")

if __name__ == '__main__':
    # print(_resolveip(sys.argv[1]))
    print(sslcheckercurl(sys.argv[1]))


