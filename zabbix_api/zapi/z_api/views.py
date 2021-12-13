# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from lib.zabbix_api import zabbixAPI
from lib.settings import URL, USER, PASS
from django.shortcuts import render, get_object_or_404
from django.views import View
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from pprint import pprint

class zabMonitoring(APIView):

	def post(self, request):
		# try:
		z = zabbixAPI(URL, USER, PASS)
		rVal = z.getAllTriggeredTriggers()

		pprint(z.getAllTriggeredTriggers())

		# rVal = []
		# x = []
		# t = {}


		# if x in res:	

		# 	module = ''
		# 	handler = ''

		# 	if 'db' in x['eventDescription'] or x['hostname']:
		# 		handler = 'db'
		# 		module = '1'

	 #        t = {
	 #            'eventName': None,
	 #            'eventDescription': x['eventDescription'],
	 #            'level': x['level'],
	 #            'module': module,
	 #            'handling': handler.decode('utf-8'),
	 #            'details': {'origin': x['ip'], 'errorMsg': x['eventDescription']},
	 #            'ip': x['ip'],
	 #            'hostname': x['hostname'],
	 #        }
	#       	rVal.append(t)
		return Response(rVal)
		# except:
			# return Response({
	  #           'status': 'Bad request',
	  #           'message': 'API Error , kindly contact Sys Ad.'
   #      	}, status=status.HTTP_400_BAD_REQUEST)