import requests
import json
import threading
import xmltodict
import re



class namecheap_wrapper(object):
    _localmsgs = threading.local()


    def __init__(self, username, token):
        self.username = username
        self.url = 'https://api.namecheap.com/xml.response'
        self.apiuser = username
        self.apikey = token
        self.clientip = '175.100.204.34'


    def getLastFailureMessage(self):
        try:
            msg = self._localmsgs.lastFailureMsg
            self._localmsgs.lastFailureMsg = None;
            return msg;
        except:
            return None;


    def _verify_result(self, result):
        if result.status_code == 200:
            rescon = result.content
            jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
            return json.loads(jd_xml)
        self._localmsgs.lastFailureMsg = result.content;
        return False


    def nc_list_domain(self):
        ret = []

        def __request_append(page):

            params = {
                'ApiUser': self.apiuser,
                'ApiKey': self.apikey,
                'UserName': self.username,
                'Command': 'namecheap.domains.getList',
                'ClientIp': '175.100.204.34',
                'PageSize': '100',
                'Page': page
            }

            rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
            rescon = rVal.content
            jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
            jread = json.loads(jd_xml)


            try:
                for i in jread['ApiResponse']['CommandResponse']['DomainGetListResult']['Domain']:
                    i['@Expires'] = re.sub('T', ' ', i['@Expires'])
                    i['@Expires'] = re.sub('Z', '', i['@Expires'])
                    i['@Expires'] = re.sub('-', '/', i['@Expires'])

                    ret.append(i)
            except TypeError:
                return False

        page = 1
        while __request_append(page):
            print page
            page += 1

        return ret


    def nc_getDomInfo(self, domain):
        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.getInfo',
            'ClientIp': '175.100.204.34',
            'DomainName': domain
        }

        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        return self._verify_result(rVal)

    def nc_list_dns_nameservers(self, domain):
        SLD, _, TLD = domain.partition('.')

        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.getList',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD
        }

        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        rescon = rVal.content
        nc_nslist = []
        jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        jread = json.loads(jd_xml)

        for t in jread['ApiResponse']['CommandResponse']['DomainDNSGetListResult']['Nameserver']:
            nc_nslist.append(t)

        ret = {
            'nameservers': nc_nslist
        }

        return ret



    @staticmethod
    def counter(count):
        count+=1
        return str(count-1)


    def nc_list_dns_records(self, domain):

        SLD, _, TLD = domain.partition('.')

        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.getHosts',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD
        }


        response = requests.get('https://api.namecheap.com/xml.response', params=params)
        rescon = response.content
        jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        jread = json.loads(jd_xml)

        ret = {
            'records': []
        }
        for i in jread['ApiResponse']['CommandResponse']['DomainDNSGetHostsResult']['host']:
            ret['records'].append(i)

        return ret



    def nc_create_dns_record(self, domain, hostname, recordtype, address, ttl=600):

        __current = self.nc_list_dns_records(domain)
        SLD, _, TLD = domain.partition('.')


        tList = {
            '@Name': hostname,
            '@Type': recordtype,
            '@Address' : address
        }

        __current['records'].append(tList)
        count = 0

        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.setHosts',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD,
            'EmailType': '',
        }

        for i in __current['records']:
            count += 1

            cthis = self.counter(count)

            params['HostName' + cthis] = i['@Name']
            params['RecordType' + cthis] = i['@Type']
            params['Address' + cthis] = i['@Address']
            params['MXPref' + cthis] = ''
            params['TTL' + cthis] = ttl


        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        # rescon = rVal.content
        # jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        # jread = json.loads(jd_xml)
        # if jread['ApiResponse']['CommandResponse']['DomainDNSSetHostsResult']['@IsSuccess'] == 'true':
        #     res = True
        # else:
        #     res = False
        return self._verify_result(rVal)
        # return res



    def nc_update_dns_record(self, domain, hostname, recordtype, address, ttl=600):
        SLD, _, TLD = domain.partition('.')

        tList = {
            '@Name': hostname,
            '@Type': recordtype,
            '@Address' : address
        }

        tRec = {
            'records': []
        }

        tRec['records'].append(tList)
        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.setHosts',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD,
            'EmailType': '',
        }

        count = 0

        for i in tRec['records']:
            count+=1

            cthis = self.counter(count)

            params['HostName'+ cthis] = i['@Name']
            params['RecordType'+ cthis] = i['@Type']
            params['Address'+ cthis] = i['@Address']
            params['MXPref'+ cthis] = ''
            params['TTL' + cthis] = ttl


        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        # rescon = rVal.content
        # jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        # jread = json.loads(jd_xml)
        # if jread['ApiResponse']['CommandResponse']['DomainDNSSetHostsResult']['@IsSuccess'] == 'true':
        #     res = True
        # else:
        #     res = False
        return self._verify_result(rVal)
        # return res

    def nc_delete_dns_record(self, domain, hostname, recordtype, ttl=600):
        SLD, _, TLD = domain.partition('.')
        current = self.nc_list_dns_records(domain)

        for i in current['records']:
            if i['@Type'] == recordtype and i['@Name'] == hostname:
                current.remove(i)

        for i in current:
            print i , 'new'

        count = 0

        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.setHosts',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD,
            'EmailType': '',
        }

        for i in current['records']:
            count+=1

            cthis = self.counter(count)

            params['HostName'+ cthis] = i['@Name']
            params['RecordType'+ cthis] = i['@Type']
            params['Address'+ cthis] = i['@Address']
            params['MXPref'+ cthis] = ''
            params['TTL' + cthis] = ttl

        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        # rescon = rVal.content
        # jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        # jread = json.loads(jd_xml)
        # if jread['ApiResponse']['CommandResponse']['DomainDNSSetHostsResult']['@IsSuccess'] == 'true':
        #     res = True
        # else:
        #     res = False
        return self._verify_result(rVal)
        # return res


    def nc_set_nameserver(self, domain, nameservers=[]):

        SLD, _, TLD = domain.partition('.')

        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.setCustom',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD,
            'Nameservers': nameservers
        }

        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        # rescon = rVal.content
        # jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        # jread = json.loads(jd_xml)
        #
        # if jread['ApiResponse']['CommandResponse']['DomainDNSSetHostsResult']['@IsSuccess']=='true':
        #     res = True
        # else:
        #     res = False
        #
        # return res

        return self._verify_result(rVal)

    def nc_set_nameserver_default(self, domain):


        SLD, _, TLD = domain.partition('.')
        params = {
            'ApiUser': self.username,
            'ApiKey': self.apikey,
            'UserName': self.username,
            'Command': 'namecheap.domains.dns.setDefault',
            'ClientIp': '175.100.204.34',
            'SLD': SLD,
            'TLD': TLD,
        }
        rVal = requests.get('https://api.namecheap.com/xml.response', params=params)
        # rescon = rVal.content
        #
        # jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        # jread = json.loads(jd_xml)
        # try:
        #     if jread['ApiResponse']['CommandResponse']['DomainDNSSetDefaultResult']['@Updated'] == 'true':
        #         res = True
        #     else:
        #         res = False
        # except Exception:
        #     res = False

        return self._verify_result(rVal)
        # return res

