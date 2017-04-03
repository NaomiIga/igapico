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

#テスト用
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
		name = datas["name"]
		#name = datas

		
		if User.objects.get(username = name) is None:
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
			return HttpResponse(u'error')
		
		'''try:
			testname = User.objects.get(username = name)
			return HTTPResponse(u'error')
		except User.DoesNotExist:
			new_data = User.objects.create(
			username = name[0],
			starttime = datetime.datetime.now(),
			)
			new_data.save()

			new_data = UsedHint.objects.create(
			username = name[0],
			)
			new_data.save()
			return HttpResponse(name)'''

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

#飛んできた店名の配列からBeaconIDに変換する関数
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

		treasure = 'treasure' + str(treasure_num)

		update_data = User.objects.get(username = name)
		update_data.treasure = datetime.datetime.today()
		update_data.save()

		#ここにポイント計算のこと書く


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

# 初めてヒント見たときに呼ばれる
@csrf_exempt
def hint_first(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		tag = datas["treasureNo"]

		# DBに使用時間を格納
		usedhintdatas = UsedHint.objects.get(username = name)
		if tag == 1:
			usedhintdatas.hint1_1 = datetime.datetime.now()
		elif tag == 2:
			usedhintdatas.hint2_1 = datetime.datetime.now()
		elif tag == 3:
			usedhintdatas.hint3_1 = datetime.datetime.now()
		usedhintdatas.save()

		hintdatas = Hint.objects.get(treasure_num = tag, hint_num = 1)
		first_hint = hintdatas.hint_sent
		first_hint = 'ヒント1\n' + first_hint
		return JsonResponse({"hint1":first_hint})
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

# 2個目以降のヒント使うときによばれる
@csrf_exempt
def hint(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		tag = datas["treasureNo"]
		treasureNo = 'treasure' + str(tag)

		hint = hint_check(name, tag)

		return JsonResponse({"hint":hint})
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#どれだけヒント使ってきたかをチェック まだ未完成　書き換え必須
def hint_check(name, treasureNo):
	data = UsedHint.objects.get(username = name)

	if treasureNo == "treasure1":
		if data.hint1_2 == None:
			data.hint1_2 = datetime.datetime.now()
			data.save()
			hint = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
		elif data.hint1_3 == None:
			data.hint1_3 = datetime.datetime.now()
			data.save()
			hint = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
	elif treasureNo == "treasure2":
		if data.hint2_2 == None:
			data.hint2_2 = datetime.datetime.now()
			data.save()
			hint = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
		elif data.hint2_3 == None:
			data.hint2_3 = datetime.datetime.now()
			data.save()
			hint = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
	elif treasureNo == "treasure3":
		if data.hint3_2 == None:
			data.hint3_2 = datetime.datetime.now()
			data.save()
			hint = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
		elif data.hint3_3 == None:
			data.hint3_3 = datetime.datetime.now()
			data.save()
			hint = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
	else:
		print 'error'

	return hint

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
	if request.method == 'POST':
		shops = {}
		shop_list = []
		for i in Shop_ladies.objects.all():
			shop_list.append(i.shop_name)
		shops["ladies"] = shop_list

		shop_list = []
		for i in Shop_mens.objects.all():
			shop_list.append(i.shop_name)
		shops["mens"] = shop_list

		shop_list = []
		for i in Shop_ladiesmens.objects.all():
			shop_list.append(i.shop_name)
		shops["ladiesmens"] = shop_list

		shop_list = []
		for i in Shop_kids.objects.all():
			shop_list.append(i.shop_name)
		shops["kids"] = shop_list

		shop_list = []
		for i in Shop_sports.objects.all():
			shop_list.append(i.shop_name)
		shops["sports"] = shop_list

		shop_list = []
		for i in Shop_shoesbag.objects.all():
			shop_list.append(i.shop_name)
		shops["shoesbag"] = shop_list

		shop_list = []
		for i in Shop_fassiongoods.objects.all():
			shop_list.append(i.shop_name)
		shops["fassiongoods"] = shop_list

		shop_list = []
		for i in Shop_goodsvariety.objects.all():
			shop_list.append(i.shop_name)
		shops["goodsvariety"] = shop_list

		shop_list = []
		for i in Shop_accessory.objects.all():
			shop_list.append(i.shop_name)
		shops["accessory"] = shop_list

		for i in Shop_food.objects.all():
			shop_list.append(i.shop_name)
		shops["food"] = shop_list

		shop_list = []
		for i in Shop_service.objects.all():
			shop_list.append(i.shop_name)
		shops["service"] = shop_list

		shop_list = []
		for i in Shop_limited.objects.all():
			shop_list.append(i.shop_name)
		shops["limited"] = shop_list

		return JsonResponse(shops, safe = False)

	else:
		response = HttpResponse()
		response['msg'] = 'NG'
