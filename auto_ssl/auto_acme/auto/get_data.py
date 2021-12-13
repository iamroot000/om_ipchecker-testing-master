import mysql.connector

def hoy():

    mydb = mysql.connector.connect(
        host="10.167.11.205",
        user="argususer",
        passwd="S22c350",
        database="argus"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT domain FROM SSLDOMAINS_ssldomain2")
    domdom = mycursor.fetchall()

