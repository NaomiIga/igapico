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
import datetime
import json
import numpy
import time
from django.utils.encoding import *
from django.http.response import JsonResponse
from django.core import serializers

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
			username = name[0],
			starttime = datetime.datetime.now(),
			)
			new_data.save()

			new_data = UsedHint.objects.create(
			username = name[0],
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

		update_data = User.objects.get(username = name[0])
		update_data.shopname = shops[0]
		update_data.save()

		num_list = shop_connect(shops[0])   #ショップとビーコンを紐づけるshop_connect関数に飛ぶ
		##ここはdictionaly型にしてからじゃないとjsondumpしてください
		#num_list = json.dumps({"datas":num_list})  #json形式にする
		#return JsonResponse({num_list}, content_type='application/json)  #json返す
		return JsonResponse({"data":num_list})

	else:
		response = HttpResponse()
		response['msg'] = 'NG'
	#return name

#飛んできた店ID(店名？)の配列からBeaconIDに変換する関数
def shop_connect(shopArr):
	num_list = [] #結果のbeaconNOを格納する配列

	for i in shopArr:
		datas = Shop_Beacon.objects.get(shopname = i)
		beacon_datas = Beacon.objects.get(beacon_id = datas.beacon_id)
		num_list.append([beacon_datas.major, beacon_datas.minor])

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

		#for i in range(3):
			#if check[i] == "":


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
		print 'error'


	return check

'''
#鍵ビーコンの範囲をreturn
def ReturnKeyArea(beacon):
	xarea = []
	yarea = []
	for i in beacon:
		update_data = KeyArea.objects.get(beacon_id = i)
		xarea.append(update_data.xgrid)
		yarea.append(update_data.ygrid)

	return xarea, yarea
'''

#ショップリスト送る
@csrf_exempt
def shop_loading(request):
	'''
	if request.method == 'POST':
		datas = json.loads(request.body)
		category = datas["category"]   # ダブルクオート内はディクショナリーのキー

		shops = []

		if category == "ladies":
			for i in Shop_ladies.objects.all():
				shops.append(i.shop_name)
		elif category == "mens":
			for i in Shop_mens.objects.all():
				shops.append(i.shop_name)
		elif category == "ladiesmens":
			for i in Shop_ladiesmens.objects.all():
				shops.append(i.shop_name)
		elif category == "kids":
			for i in Shop_kids.objects.all():
				shops.append(i.shop_name)
		elif category == "sports":
			for i in Shop_sports.objects.all():
				shops.append(i.shop_name)
		elif category == "shoesbag":
			for i in Shop_shoesbag.objects.all():
				shops.append(i.shop_name)
		elif category == "fassiongoods":
			for i in Shop_fassiongoods.objects.all():
				shops.append(i.shop_name)
		elif category == "goodsvariety":
			for i in Shop_goodsvariety.objects.all():
				shops.append(i.shop_name)
		elif category == "accessory":
			for i in Shop_accessory.objects.all():
				shops.append(i.shop_name)
		elif category == "food":
			for i in Shop_food.objects.all():
				shops.append(i.shop_name)
		elif category == "service":
			for i in Shop_service.objects.all():
				shops.append(i.shop_name)
		elif category == "limited":
			for i in Shop_limited.objects.all():
				shops.append(i.shop_name)
		else:
			print 'error'
		return JsonResponse(shops, safe = False)
	else:
		response = HttpResponse()
		response['msg'] = 'NG'
	'''
	'''
	if request.method == 'POST':
		shops = {}
		count = 0
		#shop_list = []
		for i in Shop_ladies.objects.all():
			if count == 0:
				shops["Shop_ladies"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_ladies"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_ladies"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_mens.objects.all():
			if count == 0:
				shops["Shop_mens"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_mens"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_mens"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_ladiesmens.objects.all():
			if count == 0:
				shops["Shop_ladiesmens"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_ladiesmens"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_ladiesmens"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_kids.objects.all():
			if count == 0:
				shops["Shop_kids"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_kids"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_kids"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_sports.objects.all():
			if count == 0:
				shops["Shop_sports"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_sports"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_sports"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_shoesbag.objects.all():
			if count == 0:
				shops["Shop_shoesbag"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_shoesbag"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_shoesbag"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_fassiongoods.objects.all():
			if count == 0:
				shops["Shop_fassiongoods"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_fassiongoods"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_fassiongoods"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_goodsvariety.objects.all():
			if count == 0:
				shops["Shop_goodsvariety"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_goodsvariety"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_goodsvariety"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_accessory.objects.all():
			if count == 0:
				shops["Shop_accessory"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_accessory"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_accessory"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_food.objects.all():
			if count == 0:
				shops["Shop_food"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_food"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_food"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_service.objects.all():
			if count == 0:
				shops["Shop_service"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_service"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_service"] = {shop_list}

		#shop_list = []
		count = 0
		for i in Shop_limited.objects.all():
			if count == 0:
				shops["Shop_limited"] = {i.shop_name}
				count += 1
			else:
				shops["Shop_limited"].update({i.shop_name})
			#shop_list.append(i.shop_name)
			#shops["Shop_limited"] = {shop_list}

		shops['message'] = serializers.serialize('json', shops)
		return JsonResponse(shops)

	else:
		response = HttpResponse()
		response['msg'] = 'NG'
	'''
	if request.method == 'POST':
		shops = {}
		shop_list = []
		for i in Shop_ladies.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_ladies"] = shop_list

		shop_list = []
		for i in Shop_mens.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_mens"] = shop_list

		shop_list = []
		for i in Shop_ladiesmens.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_ladiesmens"] = shop_list

		shop_list = []
		for i in Shop_kids.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_kids"] = shop_list

		shop_list = []
		for i in Shop_sports.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_sports"] = shop_list

		shop_list = []
		for i in Shop_shoesbag.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_shoesbag"] = shop_list

		shop_list = []
		for i in Shop_fassiongoods.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_fassiongoods"] = shop_list

		shop_list = []
		for i in Shop_goodsvariety.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_goodsvariety"] = shop_list

		shop_list = []
		for i in Shop_accessory.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_accessory"] = shop_list

		for i in Shop_food.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_food"] = shop_list

		shop_list = []
		for i in Shop_service.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_service"] = shop_list

		shop_list = []
		for i in Shop_limited.objects.all():
			shop_list.append(i.shop_name)
		shops["Shop_limited"] = shop_list

		return JsonResponse(shops, safe = False)

	else:
		response = HttpResponse()
		response['msg'] = 'NG'
