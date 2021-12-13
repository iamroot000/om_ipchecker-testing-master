import urllib
from time import mktime
from datetime import datetime
import requests
import json
import threading
import xmltodict
from hashlib import md5

class dnscom_wrapper(object):
    _localmsgs = threading.local()

    def __init__(self, username, token):
        # username not used but keep it for formality
        self.username = username
        self.apikey, _, self.apisecret = str(token).partition('_')

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

    # @staticmethod
    # def get_hash(key,secret):
    #     time = str(mktime(datetime.now().timetuple())).replace('.0','')
    #     thash = str('apiKey=' + key + '&domain=dns.com&timestamp='+ time+ secret)
    #     _hash = md5(thash.encode('utf-8')).hexdigest()
    #     print thash
    #     return _hash

    @staticmethod
    def sign(dParams, secret):
        asdf = [];
        for i in sorted(dParams.keys()):
            asdf.append((i, dParams[i]));

        asdf = urllib.urlencode(asdf);
        asdf += secret;
        # print asdf;
        return md5(asdf).hexdigest();


    def retrieve_domain(self):
    #DNS.COM doesnt have api for expiration date. set to None while waiting
        record = dict();
        # ret = list();
        toRead = list();

        def __request_append(page):
            params = {
                'apiKey': self.apikey,
                'timestamp': str(mktime(datetime.now().timetuple())).replace('.0', ''),
                'page': page,
                'pageSize': '20'
            }

            _hash = self.sign(params, self.apisecret)
            params['hash'] = _hash
            rVal = requests.post('https://www.dns.com/api/domain/list/', params=params)
            record['records'] = json.loads(rVal.content)['data']

            for i in record['records']['data']:
                toRead.append({'domain': i['domains'], 'expiry': 'None'})


            if 'nextPage' in record['records']:
                return True
            return False

        page = 1
        while __request_append(page):
            print page
            page += 1

        # for dom in toRead:
        #     dom = str(dom).encode('utf-8')
        #     exp = whois.query(dom)
        #     date, _, trash = str(exp.expiration_date).partition(' ')
        #     ret.append({'domain': dom, 'expiry': date})
        #     print ret

        return toRead

    def list_dns_records(self, domain):
        ret = dict();

        params = {
            'apiKey': self.apikey,
            'timestamp': str(mktime(datetime.now().timetuple())).replace('.0', ''),
            'domainID': domain,
            'pageSize': '20'
        }

        _hash = self.sign(params, self.apisecret)
        params['hash'] = _hash
        rVal = requests.post('https://www.dns.com/api/record/list/', params=params)
        tJson = json.loads(rVal.content)
        ret['records'] = tJson['data']['data']

        return ret

    def create_dns_record(self, domain, hostname, type, content, remark='', mx='', ttl=600):

        params = {
            'apiKey': self.apikey,
            'timestamp': str(mktime(datetime.now().timetuple())).replace('.0', ''),
            'domainID': domain,
            # 'viewID': viewID,
            'type': type,
            'host': hostname,
            'value': content,
            'TTL': ttl,
            'mx': mx,
            'remark': remark
        }

        _hash = self.sign(params, self.apisecret)
        params['hash'] = _hash
        rVal = requests.post('https://www.dns.com/api/record/create/', params=params)

        # return json.dumps(rVal.content)
        return self._verify_result(rVal)

    def delete_dns_record(self, domain, record_id):
        params = {
            'apiKey': self.apikey,
            'timestamp': str(mktime(datetime.now().timetuple())).replace('.0', ''),
            'domainID': domain,
            'recordID': record_id
        }

        _hash = self.sign(params, self.apisecret)
        params['hash'] = _hash
        rVal = requests.post('https://www.dns.com/api/record/remove/', params=params)

        return self._verify_result(rVal)

    def update_dns_record(self,domain,record_id,hostname,type,content,ttl=600):

        params = {
            'apiKey': self.apikey,
            'timestamp': str(mktime(datetime.now().timetuple())).replace('.0', ''),
            'domainID': domain,
            'recordID': record_id,
            'newtype': type,
            'newhost': hostname,
            'newvalue': content,
            'newttl': ttl
        }

        _hash = self.sign(params, self.apisecret)
        params['hash'] = _hash
        rVal = requests.post('https://www.dns.com/api/record/modify/', params=params)
        return json.dumps(rVal.content)
        # return self._verify_result(rVal)

    def list_nameservers(self,domain):
        return None

    def set_nameserver(self,domain,ns):
        return None


