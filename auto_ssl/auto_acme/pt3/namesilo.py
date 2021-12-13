import requests
import json
import threading
import xmltodict
import re



class namesilo_wrapper(object):
    _localmsgs = threading.local()


    def __init__(self,username, token):
        #username not used but keep it for formality
        self.username = username
        self.apikey = token


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

    #DONE
    def retrieve_domain(self):

        ret = list();
        toRead = list();

        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey
        }

        response = requests.get('https://www.namesilo.com/api/listDomains', params=params)

        rescon = response.content

        jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')), indent=3)
        jread = json.loads(jd_xml)

        for i in jread['namesilo']['reply']['domains']['domain']:
            toRead.append(i)

        for x in toRead:
            params2 = {
                'version': '1',
                'type': 'xml',
                'key': self.apikey,
                'domain': x
            }

            response2 = requests.get('https://www.namesilo.com/api/getDomainInfo', params=params2)
            rescon2 = response2.content
            jd_xml2 = json.dumps(xmltodict.parse(rescon2.decode('utf-8')))
            jread2 = json.loads(jd_xml2)
            expiry = jread2['namesilo']['reply']['expires']

            ret.append({'domain': x, 'expiry': re.sub('-', '/', expiry)})

        return ret


    def list_dns_records(self, domain):

        ret = dict();
        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey,
            'domain': domain
        }

        response = requests.get('https://www.namesilo.com/api/dnsListRecords', params=params)
        rescon = response.content
        jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        jread = json.loads(jd_xml)

        ret['records'] = jread['namesilo']['reply']['resource_record']

        return ret

    def create_dns_record(self, domain,hostname,type, content, ttl=3600):

        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey,
            'domain': domain,
            'rrtype': type,
            'rrhost': hostname,
            'rrvalue': content,
            'rrdistance': '',
            'rrttl': ttl,
        }
        rVal = requests.get('https://www.namesilo.com/api/dnsAddRecord', params=params)
        # rescon = response.content
        # jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        # jread = json.loads(jd_xml)

        return self._verify_result(rVal)

    def delete_dns_record(self,domain,record_id):

        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey,
            'domain': domain,
            'rrid': record_id
        }

        rVal = requests.get('https://www.namesilo.com/api/dnsDeleteRecord', params=params)

        return self._verify_result(rVal)

    def update_dns_record(self,domain,record_id, hostname, content,ttl=3600):

        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey,
            'domain': domain,
            'rrid': record_id,
            'rrhost': hostname,
            'rrvalue': content,
            'rrdistance': '',
            'rrttl': 3600

        }

        rVal = requests.get('https://www.namesilo.com/api/dnsUpdateRecord', params=params)

        return self._verify_result(rVal)

    def list_nameservers(self,domain):

        ret = dict();

        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey,
            'domain': domain,
        }

        rVal = requests.get('https://www.namesilo.com/api/getDomainInfo', params=params)
        rescon = rVal.content
        jd_xml = json.dumps(xmltodict.parse(rescon.decode('utf-8')))
        jread = json.loads(jd_xml)

        ret['nameservers'] = jread['namesilo']['reply']['nameservers']['nameserver']

        return ret

    @staticmethod
    def counter(count):
        count+=1
        return str(count-1)

    def set_nameserver(self,domain, ns):
    #this function can change nameserver of up to 200 domains
    #required atleast 2 nameservers
        count = 0

        params = {
            'version': '1',
            'type': 'xml',
            'key': self.apikey,
            'domain': domain,
        }

        for i in ns:
            count += 1

            cthis = self.counter(count)
            params['ns' + cthis] = i

        rVal = requests.get('https://www.namesilo.com/api/changeNameServers', params=params)

        return self._verify_result(rVal)

