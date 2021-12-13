import mysql.connector


def hoy():
    mydb = mysql.connector.connect(
        host="10.167.11.205",
        user="argususer",
        passwd="S22c350",
        database="argus"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT username, token, provider FROM domains_account")
    accounts = mycursor.fetchall()

    for acc in accounts:
        print(acc[1])


if __name__=='__main__':
    hoy()
