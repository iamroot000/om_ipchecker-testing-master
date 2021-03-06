import socket, ssl, datetime



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
    sslcheckerOut('wukongchat-web-test.neweb.me');



