import datetime, os, json





f = open("/opt/sslchecker/zabbix/domain_list.txt", "r")

domainlist = f.read().split('\n')

rVal = {

    "data":[]

}

for i in domainlist:

    domlist = i.split(',')

    if len(domlist[0]) != 0 and len(domlist) ==2:

        rVal['data'].append({

            "{#VAULTDOMAIN}": domlist[0].strip(),

            "{#RESOLVE}": domlist[-1].strip()

        })





print(json.dumps(rVal, indent=4))
#print(rVal)

