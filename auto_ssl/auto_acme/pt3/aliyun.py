#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
@author: Nico
@note: Aliyun Cloud API caller
'''

import urllib
import base64
from Crypto.Hash import HMAC,SHA
import time,random,requests,datetime
import json
import threading


def getHMACSig(dParams,key):
    '''
    Signature generation as per https://www.alibabacloud.com/help/doc-detail/34279.htm
    :param dParams: Parameters in dictionary form
    :param key: AccessKeySecret
    :return: returns signature in base64
    '''
    strQueryCanonical = "GET&%2F&"; #ignore uri lol
    #generate the string to sign from the sorted/canonicalized form
    for i in sorted(dParams.keys()):
        strQueryCanonical += urllib.quote_plus(urllib.urlencode({i:dParams[i]})) + "%26"# + '\n'
    strQueryCanonical = strQueryCanonical[:-3] #remove last 3 characters, derp algo
    #print strQueryCanonical;
    return base64.b64encode(HMAC.new(key + "&",strQueryCanonical,SHA).digest()) #append ampersand to key as per documentation, b64-encode the raw signature (not hex digested)


class aladdin(object):

    @staticmethod
    def getHMACSig(dParams, key):
        '''
        Signature generation as per https://www.alibabacloud.com/help/doc-detail/34279.htm
        :param dParams: Parameters in dictionary form
        :param key: AccessKeySecret
        :return: returns signature in base64
        '''
        strQueryCanonical = "GET&%2F&";  # ignore uri lol
        # generate the string to sign from the sorted/canonicalized form
        for i in sorted(dParams.keys()):
            strQueryCanonical += urllib.quote_plus(urllib.urlencode({i: dParams[i]})) + "%26"  # + '\n'
        strQueryCanonical = strQueryCanonical[:-3]  # remove last 3 characters, derp algo
        #print strQueryCanonical;
        return base64.b64encode(HMAC.new(key + "&", strQueryCanonical,
                                         SHA).digest())  # append ampersand to key as per documentation, b64-encode the raw signature (not hex digested)

    def __init__(self,keyid,keysecret,api_callback='dns.aliyuncs.com'):
        self.__id = str(keyid);
        self.__shh = str(keysecret);
        self.__api = api_callback;

    def __decorateAndSign(self,dParams):
        '''
        Magic
        :param dParams: params
        :return:
        '''
        #signature = getHMACSig(dParams,self.__shh);
        timenow = time.time();
        dParams['Format'] = "json";
        dParams['Version'] = "2015-01-09";
        dParams['AccessKeyId'] = self.__id;
        dParams['SignatureMethod'] = 'HMAC-SHA1';
        dParams['Timestamp'] = datetime.datetime.utcfromtimestamp(timenow).strftime("%Y-%m-%dT%H:%M:%SZ");
        dParams['SignatureVersion'] = '1.0';
        dParams['SignatureNonce'] = str(int(timenow * random.random()));
        dParams['Signature'] = self.getHMACSig(dParams,self.__shh);
        return True;

    def delRecord(self,record_id):
        dParams = {
            'Action' : 'DeleteDomainRecord',
            'RecordId' : record_id
        }
        self.__decorateAndSign(dParams);
        result = requests.get('https://%s' % self.__api,params=dParams);
        if (result.status_code != 200):
            print "AliFailed: HTTP code: %s, response: %s" % (result.status_code,result.content);
            return ;
        return json.loads(result.content);


    def updateRecord(self,record_id, rr, Type, value, ttl=None):
        dParams = {
            'Action' : 'UpdateDomainRecord',
            'RecordId' : record_id,
            'RR' : rr,
            'Type' : Type,
            'Value' : value,
        }
        if ttl:
            dParams['TTL'] = ttl;
        self.__decorateAndSign(dParams);
        result = requests.get('https://%s' % self.__api,params=dParams);
        if (result.status_code != 200):
            print "AliFailed: HTTP code: %s, response: %s" % (result.status_code,result.content);
            return ;
        return json.loads(result.content);


    def addRecord(self,domain, rr, Type, value, ttl=None):
        dParams = {
            'Action' : 'AddDomainRecord',
            'DomainName' : domain,
            'RR' : rr,
            'Type' : Type,
            'Value' : value,
        }
        if ttl:
            dParams['TTL'] = ttl;
        self.__decorateAndSign(dParams);
        result = requests.get('https://%s' % self.__api,params=dParams);
        if (result.status_code != 200):
            print "AliFailed: HTTP code: %s, response: %s" % (result.status_code,result.content);
            return ;
        return json.loads(result.content);

    def getRecords(self,domain,page=1,pagesize=500):
        '''
        Returns json response from Ali's DescribeDomainRecords routine in dictionary format
        :param domain: domain to retrieve records from
        :param page: page number
        :param pagesize: page size
        :return: JSON response in dictionary
        '''
        dParams = {
            'Action' : 'DescribeDomainRecords',
            'DomainName' : domain,
            'PageNumber' : page,
            'PageSize' : pagesize,
        }
        self.__decorateAndSign(dParams);
        result = requests.get('https://%s' % self.__api,params=dParams);
        if (result.status_code != 200):
            print "AliFailed: HTTP code: %s, response: %s" % (result.status_code,result.content);
            return ;
        return json.loads(result.content);

    def getDomainList(self,page=1,pagesize=100):
        '''
        Returns json response from Ali's DescribeDomains routine in dictionary format
        :param page: page number
        :param pagesize: page size
        :return: JSON response in dictionary
        '''
        dParams = {
            'Action' : 'DescribeDomains',
            'PageNumber' : page,
            'PageSize' : pagesize,
        }
        #dParams['KeyWord'] = 'com';
        self.__decorateAndSign(dParams);
        result = requests.get('https://%s' % self.__api,params=dParams);
        if (result.status_code != 200):
            print "AliFailed: HTTP code: %s, response: %s" % (result.status_code,result.content);
            return ;
        return json.loads(result.content);


#test = aladdin('LTAIjYTwTx5JWQHa','khoLu9oXv4B9kra0WiwVJrwjYuUrLr')



