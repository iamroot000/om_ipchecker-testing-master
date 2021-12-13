import requests
import json
import threading



ENDPOINTS= {
    "listdomains":"/v1/domains?limit=1000",
    "retrievedomain":"/v1/domains/{0}",
    'listdnsrecords':"/v1/domains/{0}/records",
    'creatednsrecord':"/v1/domains/{0}/records",
    'editdnsrecord': "/v1/domains/{0}/records/{1}/{2}"

}

class godaddy_wrapper(object):
    _localmsgs = threading.local();
    def __init__(self,username,token):
        self.url = 'https://api.godaddy.com'
        self.header={
            'Authorization': 'sso-key {0}:{1}'.format(username,token),
        }
        #self._localmsgs = self._localmsgs = object();#threading.local();
    def getLastFailureMessage(self):
        try:
            msg = self._localmsgs.lastFailureMsg
            self._localmsgs.lastFailureMsg = None;
            return msg;
        except:
            return None;

    def _verify_result(self, result, preent=1):
        try:
            if preent:
                print "GD: %s" % result.content;
            return json.loads(result.content);
        except:
            if result.status_code == 200:
                return '{"status":"success"}';
            self._localmsgs.lastFailureMsg = result.content;
            return False

    def list_domains(self,endpoint=ENDPOINTS['listdomains']):
        rVal = requests.get('{0}{1}'.format(self.url,endpoint),headers=self.header)
        return self._verify_result(rVal,preent=0)

    def retrieve_domain(self, domain ,endpoint=ENDPOINTS['retrievedomain']):
        rVal = requests.get('{0}{1}'.format(self.url, endpoint.format(domain)), headers=self.header)
        return self._verify_result(rVal)

    def list_dns_records(self,domain,endpoint=ENDPOINTS['listdnsrecords']):

        rVal = requests.get('{0}{1}'.format(self.url, endpoint.format(domain)), headers=self.header)
        return self._verify_result(rVal)

    def create_dns_record(self,domain,hostname,type, content, endpoint=ENDPOINTS['creatednsrecord'], ttl=600,priority=None):
        print ttl,'shit'
        data=[
            {
                'data':content,
                'name':hostname,
                'ttl':ttl,
                'type':type
            }
        ]

        if data[0]['type'] == 'MX' or data[0]['type']=='SRV':
            if priority == None:
                priority = 1
            data[0]['priority']= priority

        if ttl == None or ttl < 600 or ttl==0 or ttl=='':
            ttl=600

        data[0]['ttl']=ttl
        print data
        rVal = requests.patch('{0}{1}'.format(self.url,endpoint.format(domain)),json=data,headers=self.header);

        return self._verify_result(rVal)

    def delete_dns_record(self,domain, hostname, r_type, endpoint=ENDPOINTS['creatednsrecord']):

        current = self.list_dns_records(domain)

        for i in current:
            if i['type'] == r_type and i['name']== hostname:
                print i
                current.remove(i)

        print "_+_____"
        for i in current:
            print i , 'new'

        rVal = requests.put('{0}{1}'.format(self.url, endpoint.format(domain)), json=current, headers=self.header)
        return self._verify_result(rVal)

    def edit_dns_record(self,domain, hostname, r_type, content, endpoint=ENDPOINTS['editdnsrecord'],ttl=None,priority=None):
        data = [
            {
                'data': content,
                'name': hostname,
                'ttl': 600,
                'type': r_type
            }
        ]

        if data[0]['type'] == 'MX' or data[0]['type']=='SRV':
            if priority == None:
                priority = 1
            data[0]['priority']= priority

        if ttl == None or ttl < 600:
            data[0]['ttl']=600

        rVal = requests.put('{0}{1}'.format(self.url, endpoint.format(domain,r_type,hostname)), json=data, headers=self.header)
        return self._verify_result(rVal)
