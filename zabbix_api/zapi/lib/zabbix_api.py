# -*- coding: utf-8 -*-
from pyzabbix.api import ZabbixAPI
from datetime import datetime,timedelta
from pprint import pprint
import json
import time
import re


class zabbixAPI(object):

    def __init__(self,URL,username,password):

        self.zapi = ZabbixAPI(url=URL, user=username, password=password)
        self.hcache = {}

    def getAllTriggeredTriggers(self):

        req =  {
            'only_true':'extend',
            'selectHosts':'extend',
            'selectLastEvent':'extend',
            'selectGroups':'extend',
            'expandDescription':'extend',
            'maintenance':False,
            'active':True,
            'monitored':True
        }


        triggers = self.zapi.do_request('trigger.get',req)
        rVal = []

        for i in triggers['result']:
            elem = {
                'name':i['description'],
                'hostid':i['hosts'][0]['hostid'],
                'hostname':i['hosts'][0]['name'],
                'severity':int(i['priority']),
                'groupname':[group['name'] for group in i['groups'] if group['name'].lower() != 'discovered hosts']
            }

            elem['ip'] = self.hcache[elem['hostid']].host_ip if elem['hostid'] and elem[
                'hostid'] in self.hcache else None
            elem['groupname'] = self.hcache[elem['hostid']].groups if elem['hostid'] and elem[
                'hostid'] in self.hcache else None


            if 'lastEvent' in i and i['lastEvent']:
                elem['clock'] = datetime.fromtimestamp(int(i['lastEvent']['clock']))
            rVal.append(elem)

        # jVal = json.dumps(rVal)

        # return jVal
        # rrVal = {

        # }
        tVal = []
        module = ''
        handler = ''
        ip = ''
        ggIP = []
        for x in rVal:

            req2 = {
                "output": "extend",
                "hostids": x['hostid']
            }
            gIP = self.zapi.do_request('hostinterface.get',req2)

            for p in gIP['result']:
                res = {
                    'ip': p['ip']
                }                

            if "MySQL" in x['name']:
                handler = 'Contact Tyler, the contact information of the current officer is +phone, Telegram: tg'
                module = '1'
            if "PM2" in x['name']:
                handler = 'Contact Quincy, the contact information of the current officer is +phone, Telegram: tg'
                module = '3'
            if "SSL" in x['name']:
                handler = 'Contact OM Duty, the contact information of the current officer is +phone, Telegram: tg'
                module = '1'
                # if 'ebet' in x['name'] or x['hostname']:
                #     handler = 'Contact Tyler, the contact information of the current officer is +phone, Telegram: tg'
                #     module = '1'
                # elif 'cpms' in x['name'] or x['hostname']:   
                #     handler = 'Contact Cyrus, the contact information of the current officer is +phone, Telegram: tg'
                #     module = '1' 
                # elif 'fpms' in x['name'] or x['hostname']:
                #     handler = 'Contact Poe, the contact information of the current officer is +phone, Telegram: tg'
                #     module = '1'
                # elif 'pms' in x['name'] or x['hostname']:
                #     handler = 'Contact Poe, the contact information of the current officer is +phone, Telegram: tg'
                #     module = '1'
            # elif 'pm2' in x['name'] or x['hostname']:
            #     handler = 'Contact Quincy, the contact information of the current officer is +601123077987, Telegram: quincy'
            #     module = '3'
            # elif 'ssl' in x['name'] or x['hostname']:
            #     handler = 'Contact OM Duty, the contact information of the current officer is +phone, Telegram: tg'
            #     module = '1'





            if x['severity'] == 5:
                level = 1
            elif x['severity'] == 4:
                level = 2
            elif x['severity'] == 3:
                level = 2
            elif x['severity'] == 2:
                level = 3
            elif x['severity'] == 1:
                level = 3

            q = {
                'eventName': x['name'],
                'eventDescription': x['name'],
                'level': level,
                'module': module,
                'handling': handler,
                # 'handling': handler.decode('utf-8'),
                'details': {'origin': res['ip'], 'errorMsg': x['name']},
                'ip': res['ip'],
                'hostname': x['hostname'],
                'hostid': x['hostid']
            }
            tVal.append(q)


            
        return tVal

##############################################

    # def getAllEvents(self,daysfromnow=3,showLost=False,timenow=datetime.now(),severity=None):

    #     req = {
    #         'time_from': str(int(time.mktime((timenow-timedelta(days=daysfromnow)).timetuple()))),
    #         'time_to':str(int(time.mktime(timenow.timetuple()))),
    #         'selectHosts':'extend',
    #         "select_acknowledges": "extend",
    #         'selectRelatedObject':'extend',
    #     }

    #     if severity:
    #         req['severities'] = 1

    #     events = self.zapi.do_request('event.get',req)
    #     rVal = []


    #     for i in events['result']:
    #         if len(i['hosts']) >0:

    #             elem = {
    #                 'hostname':i['hosts'][0]['name'] if i['hosts'] else None,
    #                 'eventid':int(i['eventid']),
    #                 'hostid':i['hosts'][0]['hostid'] if i['hosts'] else None,
    #                 'clock':datetime.fromtimestamp(int(i['clock'])),
    #                 'severity':int(i['severity']),
    #                 'name':i['name'],
    #                 'suppressed':True if int(i['suppressed']) != 0 else False,
    #                 'value':int(i['value']),
    #                 'ip':None,
    #                 'groupname': None,
    #                 'r_eventid':None,
    #                 'resolvetime':None,
    #             }


    #             elem['ip'] = self.hcache[elem['hostid']].host_ip if elem['hostid'] and elem['hostid'] in self.hcache else None
    #             elem['groupname'] = self.hcache[elem['hostid']].groups if elem['hostid'] and elem['hostid'] in self.hcache else None

    #             if i['r_eventid'] != '0':
    #                 elem['r_eventid'] = i['r_eventid']

    #             if elem['ip'] or showLost == True:
    #                 if i['hosts'] and i['hosts'][0]['maintenance_status'] != '1':
    #                     rVal.append(elem)

    #     todel = []

    #     for i in rVal:
    #         if i['r_eventid']:
    #             for p in rVal:
    #                 if p['eventid'] == int(i['r_eventid']):
    #                     todel.append(p)
    #                     i['value'] = p['value']
    #                     i['resolvetime'] = p['clock']
    #                     break

    #     for i in todel:
    #         if i in rVal:
    #             rVal.remove(i)

    #     rVal.sort(key=lambda item: item['clock'], reverse=True)

    #     return rVal

    # def get_all_hosts(self,filter=None,savetomodel=False):
    #     #print 'get_all_hosts'
    #     rVal = []
    #     req = self.zapi.do_request('host.get', {
    #         'selectGroups': 'extend',
    #         'selectInterfaces':'extend',
    #         'selectParentTemplates':'extend'
    #     })['result']

    #     return type(req)


if __name__=='__main__':

    URL = 'http://10.165.13.161:45689/'
    username = 'Admin'
    password='sherCock1407'

    z = zabbixAPI(URL,username,password)
    pprint(z.getAllTriggeredTriggers())
    # pprint(z.get_all_hosts())