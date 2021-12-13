import mysql.connector
from pt3.aliyun import aladdin
from pt3.dnscom import dnscom_wrapper
from pt3.dnspod import CN
from pt3.godaddycom import godaddy_wrapper
from pt3.namecheap import namecheap_wrapper
from pt3.namecom import namecom_wrapper
from pt3.namesilo import namesilo_wrapper



def hoy():


    mydb_accounts = mysql.connector.connect(
        host="10.167.11.205",
        user="argususer",
        passwd="S22c350",
        database="argus"
    )

    mycursor_acc = mydb_accounts.cursor()
    mycursor_acc.execute("SELECT username, token, provider FROM domains_account")
    accounts = mycursor_acc.fetchall()


    #provider: dnspod.cn , godaddy.com , name.com , aliyun , namecheap.com , dns.com , namesilo.com

    for acc in accounts:

        username = acc[0]
        token = acc[1]
        provider = acc[2]

        try:

            if provider == 'dnspod.cn':
                print('username: ' + username)
                # print('token: ' + token)
                dns_dnspod = CN(username,token)

                dom_dnspod = dns_dnspod.getDomainList()
                print('###dnspod###')
                print(type(dom_dnspod))
            elif provider == 'godaddy.com':
                print('username: ' + username)
                # print('token: ' + token)
                dns_godaddy = godaddy_wrapper(username,token)

                dom_godaddy = dns_godaddy.list_domains()
                print('###godaddy###')
                print(type(dom_godaddy))
            elif provider == 'name.com':
                print('username: ' + username)
                # print('token: ' + token)
                dns_name = namecom_wrapper(username,token)

                dom_name = dns_name.list_domains()
                print('###name###')
                print(type(dom_name))
            elif provider == 'aliyun':
                print('username: ' + username)
                # print('token: ' + token)
                dns_aliyun = aladdin(username,token)

                dom_aliyun = dns_aliyun.getDomainList()
                print('###aliyun###')
                print(type(dom_aliyun))
            elif provider == 'namecheap.com':
                print('username: ' + username)
                # print('token: ' + token)
                dns_namecheap = namecheap_wrapper(username,token)

                dom_namecheap = dns_namecheap.nc_list_domain()
                print('###namecheap###')
                print(type(dom_namecheap))
            elif provider == 'dns.com':
                print('username: ' + username)
                # print('token: ' + token)
                dns_dns = dnscom_wrapper(username,token)

                dom_dns = dns_dns.retrieve_domain()
                print('###dns###')
                print(type(dom_dns))
            elif provider == 'namesilo.com':
                print('username: ' + username)
                # print('token: ' + token)
                dns_namesilo = namesilo_wrapper(username,token)

                dom_namesilo = dns_namesilo.retrieve_domain()
                print('###namesilo###')
                print(type(dom_namesilo))
        except:
            print('provider not added')


    # print(dick)


if __name__=='__main__':
    hoy()
