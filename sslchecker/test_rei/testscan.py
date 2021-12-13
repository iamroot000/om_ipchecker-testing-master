import threading
import socket
#ip = socket.gethostbyname(target)

def portscan(target):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)# 

    try:
        cons = s.connect((target,443))
#        print(target,' Port :'," 443 is open.")
        https = 'open'

    except Exception as e: 
#    	print(target,' Port :'," 443 is close.")
        https = 'close'
    try:
        con = s.connect((target,80))
        # print(target,' Port :'," 80 is open.")
#        print(target,' Port :'," 80 is open.")
        http = 'open'
    except Exception as e: 
#    	print(target,' Port :'," 80 is close.")
        http = 'close'


    return http,https

if __name__=="__main__":
	print(portscan('b6549.com')[0])
