#!/usr/bin/env python
# coding: utf-8
# Create your views here.

from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
#from models import *
from models import Data
#from mdoels import User
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from datetime import datetime
import json

#csrf_exemptはつけたい関数の上にそれぞれつけなきゃダメ
#csrfを無視するコマンド
@csrf_exempt
def post_test(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = "default"
		#print request.body
		print datas
		#print datas[0]["StartTime"]
		#print datakeys
		#count = len(datas)
		#for x in range(len(datas)):
		new_data = Data.objects.create(
			userdata = datas.keys(),
			#whatdata = datas[x].keys(),
			datavalue = datas.values(),
			#datavalue = float(datas[x].values()),
		)
		new_data.save() #デーベ保存

		return HttpResponse(u'post succeed')
	else:
		response = HttpResponse()
		response['msg'] = 'NG'


@csrf_exempt
def pico_login(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]

		try:
			testname = User.objects.get(username = name)
		except:
			new_data = User.objects.create(
			usename = name,
			)
			new_data.save()
			print ('ログイン完了')
		else:
			raise ValidationError('This name already sign up...')
	else:
		response = HttpResponse()
		response['msg'] = 'NG'
