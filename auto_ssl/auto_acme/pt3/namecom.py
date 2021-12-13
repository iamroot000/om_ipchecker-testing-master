import requests
import json
import base64
import re
import threading
from requests.adapters import HTTPAdapter

ENDPOINTS= {
    "listdomains":"/v4/domains",
    #"retrievedomain":"/api/domain/get/{0}",
    'retrievedomain':"/v4/domains/{0}",
    #'listdnsrecords':"/api/dns/list/{0}",
    'listdnsrecords':"/v4/domains/{0}/records",
    'creatednsrecord':"/v4/domains/{0}/records",
    'deletednsrecord':"/v4/domains/{0}/records/{1}",
    'setnameservers':"/v4/domains/{0}:setNameservers",
    'updatednsrecord':"/v4/domains/{0}/records/{1}",

}

adapt0r = HTTPAdapter(max_retries=10);
g_session = requests.Session();
g_session.mount('https://', adapt0r);
g_session.mount('http://', adapt0r);
class namecom_wrapper(object):
    _localmsgs = threading.local()
    _s = g_session;
    def __init__(self,username,token):
        #self._localmsgs = object();#threading.local();
        self.username=username
        self.url = 'https://api.name.com'
        self.header={
            'Authorization': 'Basic {0}'.format(base64.b64encode('{0}:{1}'.format(username,token))),
        }

    def getLastFailureMessage(self):
        try:
            msg = self._localmsgs.lastFailureMsg
            self._localmsgs.lastFailureMsg = None;
            return msg;
        except:
            return None;

    def _verify_result(self, result):
        if result.status_code==200:
            return json.loads(result.content)
        self._localmsgs.lastFailureMsg = result.content;
        return False

    def list_domains(self,endpoint=ENDPOINTS['listdomains']):
        ret = []

        def __request_append(page):
            rVal = self._s.get('{0}{1}?page={2}'.format(self.url, endpoint, page), headers=self.header)
            print self.header
            print rVal.headers;
            print rVal.status_code;
            if rVal.status_code == 403:
                print rVal.content;
            rVal = json.loads(rVal.content)
            if len(str(rVal)) < 65:
                print rVal
            if 'domains' not in rVal:
                return False;
            for i in rVal['domains']:
                i['expireDate'] = re.sub('T',' ',i['expireDate'])
                i['expireDate'] = re.sub('Z', '', i['expireDate'])
                i['expireDate'] = re.sub('-', '/', i['expireDate'])

                ret.append(i)


            if 'lastPage' in rVal:
                return True
            return False

        page = 1
        while __request_append(page):
            print page
            page +=1

        return ret

    def retrieve_domain(self, domain ,endpoint=ENDPOINTS['retrievedomain']):
        rVal = self._s.get('{0}{1}'.format(self.url, endpoint.format(domain)), headers=self.header)
        return self._verify_result(rVal)

    def list_dns_records(self,domain,endpoint=ENDPOINTS['listdnsrecords']):

        ret={
            'records':[]
        }

        def __request_append(page):
            rVal = self._s.get('{0}{1}?page={2}'.format(self.url, endpoint.format(domain), page), headers=self.header)

            rVal = json.loads(rVal.content)
            if 'records' in rVal:
                for i in rVal['records']:
                    ret['records'].append(i)

            if 'lastPage' in rVal:
                return True
            return False

        page = 1
        while __request_append(page):
            page += 1

        return ret

    def create_dns_record(self,domain,hostname,type, content, endpoint=ENDPOINTS['creatednsrecord'], ttl=300,priority=None):

        try:
            ttl = int(ttl)
        except:
            ttl=300

        data = {
            'domainName':domain,
            'host':hostname,
            'fqdn':'{0}.{1}'.format(hostname,domain),
            'type':type,
            'answer':content,
            'ttl':ttl
        }

        rVal = self._s.post('{0}{1}'.format(self.url,endpoint.format(domain)),data=json.dumps(data),headers=self.header)


        return self._verify_result(rVal)

    def set_nameserver(self,domain,nameservers,endpoint=ENDPOINTS['setnameservers']):

        data = {
            'nameservers':nameservers
        }

        rVal = self._s.post('{0}{1}'.format(self.url,endpoint.format(domain)),data=json.dumps(data),headers=self.header)
        return self._verify_result(rVal)

    def delete_dns_record(self,domain, record_id, endpoint=ENDPOINTS['deletednsrecord']):

        data = {
            "record_id":record_id,
        }

        rVal = self._s.delete('{0}{1}'.format(self.url,endpoint.format(domain,record_id)),data=json.dumps(data),headers=self.header)
        return self._verify_result(rVal);

    def update_dns_record(self,domain,record_id,hostname,type, content, endpoint=ENDPOINTS['updatednsrecord'], ttl=300):
        data = {
            'domainName':domain,
            'host':hostname,
            'fqdn':'{0}.{1}'.format(hostname,domain),
            'type':type,
            'answer':content,
            'ttl':ttl
        }

        #print self._s.put('{0}{1}'.format(self.url,endpoint.format(domain,record_id)),data=json.dumps(data),headers=self.header).content

        return self._verify_result(self._s.put('{0}{1}'.format(self.url, endpoint.format(domain, record_id)), data=json.dumps(data), headers=self.header));
