# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.views import View
import json
from geoip import geolite2
from rest_framework.views import APIView
from rest_framework.response import Response
from geoip import open_database


class showInfo(APIView):
	"""docstring for ClassName"""

	def get(self,request):
		template_name = 'geo_api/index.html'

		return render(request, template_name)


class getInfo(APIView):
		

	def post(self, request):
	# def post(self, request, *args, **kwargs):
		# db = open_database('GeoIP2-City.mmdb')
		# g = db.lookup(ip_addr)
		# g = db.get_info()
		ip_addr = request.POST['get_ip']
		try:
			g = geolite2.lookup(ip_addr)

		
			if g is not None:

				rVal = {
					'ip': ip_addr,
					'country': g.country,
					'continent': g.continent,
					'timezone': g.timezone,
					'subdivisions': g.subdivisions,
				}

			else:

				rVal = {
					'ip': 'None',
					'country': 'None',
					'continent': 'None',
					'timezone': 'None',
					'subdivisions': 'None',
				}
		except ValueError as e:
			print(e)
			rVal = {
					'ip': 'Invalid Input',
					'country': 'Invalid Input',
					'continent': 'Invalid Input',
					'timezone': 'Invalid Input',
					'subdivisions': 'Invalid Input',
				}
			
		return Response(rVal)
		# return Response(g)

