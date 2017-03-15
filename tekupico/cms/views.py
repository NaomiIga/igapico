#!/usr/bin/env python
# coding: utf-8
# Create your views here.

from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404,redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie
from models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from datetime import datetime
import json
import numpy
import time

#csrf_exemptはつけたい関数の上にそれぞれつけなきゃダメ
#csrfを無視するコマンド
@csrf_exempt
def post_test(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		#name = "default"
		#print request.body
		#print datas
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

#ユーザ登録する関数、今のままだとこの瞬間が開始時刻
@csrf_exempt
def pico_login(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]

		try:
			testname = User.objects.get(username = name)
		except:
			new_data = User.objects.create(
			username = name,
			starttime = time.time()
			)
			new_data.save()
			return HttpResponse(u'登録完了')
		else:
			return HttpResponse(u'This name already sign up...')
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#飛んできた店ID(店名？)の配列からBeaconIDに変換する関数
@csrf_exempt
def shop_connect(request):
	if request.method == 'POST':
		num_list = []
		datas = json.loads(request.body)
		name = datas["shopname"]

		for i in name:
			#num_list.append(Shop_Beacon.objects.get(shopname = i))
			num_list.append(Shop_Beacon.objects.get(shop_id = i))

	else:
		response = HttpResponse()
		response['msg'] = 'NG'

	return num_list

#宝ゲットのときにそれを反映、絶対エラーでそう
@csrf_exempt
def treasure_check(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]
		treasure = datas["treasure_id"]
		treasure = 'treasure' + treasure

		update_data = User.objects.get(username = name)
		update_data.treasure = True
		update_data.save()



	else:
		response = HttpResponse()
		response['msg'] = 'NG'
