#-*- coding: utf-8 -*-
import sys
import datetime
import mysql.connector
import threading
import socket
import requests
from checker import *
from testscan import portscan

def scanme():

    mydb = mysql.connector.connect(
        #host="10.167.11.205",
        host="10.165.22.205",
        user="argususer",
        passwd="S22c350",
        database="argus"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT domain FROM domains_domain")
    domdom = mycursor.fetchall()
    # d = {"data":[]}
    for dom in domdom:

        domstr = ''.join(dom).encode('utf-8')
        # domstrl = "'"+ domstr+ "'"

        https = 'https://'+domstr
        http = 'http://'+domstr

        try:
        	print domstr
	        print requests.get(https)
	        print requests.get(http)
        	print sslchecker_notA(domstr)
        except Exception as e:
        	print e



if __name__=="__main__":
	scanme()

