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


    #provider: dnspod.cn , godaddy.com , name.com , aliyun , namecheap.com , dns.com , namesilo.com

    for acc in accounts:

        username = acc[0]
        token = acc[1]
        provider = acc[2]

        try:

            if provider == 'dnspod.cn':
                print('username: ' + username)
                print('token: ' + token)
                print('dnspod')
            elif provider == 'godaddy.com':
                print('username: ' + username)
                print('token: ' + token)
                print('godaddy')
            elif provider == 'name.com':
                print('username: ' + username)
                print('token: ' + token)
                print('name')
            elif provider == 'aliyun':
                print('username: ' + username)
                print('token: ' + token)
                print('aliyun')
            elif provider == 'namecheap.com':
                print('username: ' + username)
                print('token: ' + token)
                print('namecheap')
            elif provider == 'dns.com':
                print('username: ' + username)
                print('token: ' + token)
                print('dns')
            elif provider == 'namesilo.com':
                print('username: ' + username)
                print('token: ' + token)
                print('namesilo')
        except:
            print('provider not added')


    # print(dick)


if __name__=='__main__':
    hoy()
