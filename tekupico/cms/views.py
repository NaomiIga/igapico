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
import datetime
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

#ユーザ登録(ダブり確認)する関数、今のままだとこの瞬間が開始時刻
@csrf_exempt
def pico_login(request):
	if request.method == 'POST':
		datas = json.loads(request.body)  #追記
		#name = datas["name"]
		name = datas

		try:
			testname = User.objects.get(username = name)
		except:
			new_data = User.objects.create(
			username = name,
			starttime = datetime.datetime.today()
			)
			new_data.save()

			new_data = UsedHint.objects.create(
			username = name,
			)
			new_data.save()
			return HttpResponse(u'登録完了')
		else:
			return HttpResponse(u'This name already sign up...')
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#ユーザが行きたいショップをUserに保存
@csrf_exempt
def shoplog(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		#name = datas["name"]

		name = datas.keys()
		#whatdata = datas[x].keys(),
		shops = datas.values()
		#datavalue = float(datas[x].values()),

		update_data = User.objects.get(username = name)
		update_data.shopname = shops
		update_data.save()

		num_list = shop_connect(shops)   #ショップとビーコンを紐づけるshop_connect関数に飛ぶ
		num_list = json.dumps(num_list, ensure_ascii=False)  #json形式にする
		return JsonResponse(num_list, content_type='application/json')  #json返す

	else:
		response = HttpResponse()
		response['msg'] = 'NG'
	return name

#飛んできた店ID(店名？)の配列からBeaconIDに変換する関数
def shop_connect(shopArr):
	num_list = [] #結果のbeaconNOを格納する配列

	for i in shopArr:
		num_list.append(Shop_Beacon.objects.get(shopname = i))
		#num_list.append(Shop_Beacon.objects.get(shop_id = i))

	return num_list



#宝ゲットのときにそれを反映
@csrf_exempt
def treasure_check(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		major = datas["major"]
		minor = datas["minor"]
		treasure_num = treasure_num(major,minor)

		treasure = 'treasure' + treasure_num

		update_data = User.objects.get(username = name)
		update_data.treasure = datetime.datetime.today()
		update_data.save()
		return treasure_num
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#とんできたビーコンの番号から、どの宝かを識別
def treasure_num(get_major, get_minor):
	#data = Treasure_Beacon.objects.get(major = get_major and minor = get_minor)
	data = Treasure_Beacon.objects.get(major = get_major)
	if data.minor == get_minor:
		treasure_num = data.treasure
	return treasure_num

#ヒント使うときによばれる
@csrf_exempt
def hint(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		treasureNo = datas["treasureNo"]
		
		check = UsedHint(name, treasureNo)

		for i in range(3):
			if check[i] = "":

		update_data = User.objects.get(username = name)
		update_data.treasure = datetime.datetime.today()
		update_data.save()
		return treasure_num
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#どれだけヒント使ってきたかをチェック まだ未完成　書き換え必須
def hint_check(name, treasureNo):
	data = UsedHint.objects.get(username = name)

	if treasureNo == "treasure1":
		check = data.treasure1
	elif treasureNo == "treasure2":
		check = data.treasure2
	elif treasureNo == "treasure3":
		check = data.treasure3
	else:
		break

	return check