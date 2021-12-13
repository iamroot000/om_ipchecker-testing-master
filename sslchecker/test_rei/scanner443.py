#-*- coding: utf-8 -*-
import sys
import datetime
import mysql.connector

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

        print domstr
        print type(domstr)

if __name__=="__main__":
	scanme()

