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
import csv
import datetime
import unicodedata
from PIL import Image
import base64
import sys
sys.stdout = sys.stderr

#csrf_exemptはつけたい関数の上にそれぞれつけなきゃダメ
#csrfを無視するコマンド

#テスト用
@csrf_exempt
def post_test(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		new_data = Data.objects.create(
			userdata = datas.keys(),
			datavalue = datas.values(),
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
		temp = Shop_Beacon.objects.get(shopname = "COUNTER")
		temp.shop_id += 1
		temp.save()

		try:
			testname = User.objects.get(username = name)
			return HttpResponse(u'error')
		except User.DoesNotExist:
			new_data = User.objects.create(
			user_id = temp.shop_id,
			username = name,
			starttime = datetime.datetime.now(),
			)
			new_data.save()

			new_data = UsedHint.objects.create(
			username = name,
			)
			new_data.save()
			return HttpResponse(name)

	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#ユーザが行きたいショップをUserに保存
@csrf_exempt
def shoplog(request):
	if request.method == 'POST':

		shopbeacon = []

		datas = json.loads(request.body)

		name = datas.keys()
		shops = datas.values()

		update_data = User.objects.get(username = name[0])
		update_data.shopname = shops[0]
		update_data.save()

		count = 0

		for i in shops[0]:
			shop_data = Shop_Beacon.objects.get(shopname = i)
			shopbeacon.append({"major": shop_data.major, "minor": shop_data.minor})
			count += 1

		make_map(name[0], shops[0])   # ショップ名から座標にする関数

		return JsonResponse({"shop_beacon":shopbeacon, "count": count})

	else:
		response = HttpResponse()
		response['msg'] = 'NG'
	#return name

#飛んできた店名の配列からBeaconIDに変換する関数
def make_map(username, shopArr):
	shops1 = []
	shops2 = []
	shops3 = []

	#重ねる画像(鍵？)
	tmp = Image.open("/home/niga/igapico/tekupico/cms/pictures/key.png")
	#重ねる画像のリサイズ
	tmp = tmp.resize((50, 50))

	img1 = Image.open("/home/niga/igapico/tekupico/cms/static/img/map1F.png")
	img2 = Image.open("/home/niga/igapico/tekupico/cms/static/img/map2F.png")
	img3 = Image.open("/home/niga/igapico/tekupico/cms/static/img/MOP_map3F.png")

	for i in shopArr:
		datas = Shop_Beacon.objects.get(shopname = i)
		beacon_datas = KeyArea.objects.get(major = datas.major, minor = datas.minor)
		if datas.floor == 1:
			shops1.append((beacon_datas.xgrid, beacon_datas.ygrid))
			#shops1 = numpy.append(shops1, (beacon_datas.xgrid, beacon_datas.ygrid))
		elif datas.floor == 2:
			shops2.append((beacon_datas.xgrid, beacon_datas.ygrid))
			#shops2 = numpy.append(shops2, (beacon_datas.xgrid, beacon_datas.ygrid))
		elif datas.floor == 3:
			#shops3.append((beacon_datas.xgrid, beacon_datas.ygrid))
			shops3 = numpy.append(shops3, (beacon_datas.xgrid, beacon_datas.ygrid))

	for i in range(1,4):
		#画像を置く座標(左上を指定)

		if i == 1:
			for j in shops1:
				#元画像に重ねる、左上の座標を指定
				img1.paste(tmp, j, tmp)
		elif i == 2:
			for j in shops2:
				#元画像に重ねる、左上の座標を指定
				img2.paste(tmp, j, tmp)
		elif i == 3:
			for j in shops3:
				#元画像に重ねる、左上の座標を指定
				img3.paste(tmp, j, tmp)

	img1.save("/home/niga/igapico/tekupico/cms/static/img/User_Map_1F.png")
	img2.save("/home/niga/igapico/tekupico/cms/static/img/User_Map_2F.png")
	img3.save("/home/niga/igapico/tekupico/cms/static/img/User_Map_3F.png")

#鍵ゲットのとき
@csrf_exempt
def key_get(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		major = datas["major"]
		minor = datas["minor"]
		beacon = str(major) + "-" + str(minor)
		get_time = datetime.datetime.now()
		get_time_str = get_time.strftime("%Y-%m-%d %H:%M")
		key = "{" + beacon + ":" + get_time_str + "}"

		update_data = User.objects.get(username = name)
		if update_data.key == "key":
			keys = key
		else:
			key_data = update_data.key
			keys = key_data + ", " + key
		update_data.key = keys
		update_data.save()
	return HttpResponse("OK")


#宝ゲットのとき
@csrf_exempt
def treasure_check(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		major = datas["major"]
		minor = datas["minor"]
		treasure_number = treasure_num(major,minor)

		update_data = User.objects.get(username = name)
		watched_hint = UsedHint.objects.get(username = name)

		if treasure_number == 1:
			if update_data.treasure1 == None:
				update_data.treasure1 = datetime.datetime.now()
				if watched_hint.hint1_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint1_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 2:
			if update_data.treasure2 == None:
				update_data.treasure2 = datetime.datetime.now()
				if watched_hint.hint2_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint2_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 3:
			if update_data.treasure3 == None:
				update_data.treasure3 = datetime.datetime.now()
				if watched_hint.hint3_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint3_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 4:
			if update_data.treasure4 == None:
				update_data.treasure4 = datetime.datetime.now()
				if watched_hint.hint4_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint4_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 5:
			if update_data.treasure5 == None:
				update_data.treasure5 = datetime.datetime.now()
				if watched_hint.hint5_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint5_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 6:
			if update_data.treasure6 == None:
				update_data.treasure6 = datetime.datetime.now()
				if watched_hint.hint6_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint6_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 7:
			if update_data.treasure7 == None:
				update_data.treasure7 = datetime.datetime.now()
				if watched_hint.hint7_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint7_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 8:
			if update_data.treasure8 == None:
				update_data.treasure8 = datetime.datetime.now()
				if watched_hint.hint8_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint8_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 9:
			if update_data.treasure9 == None:
				update_data.treasure9 = datetime.datetime.now()
				if watched_hint.hint9_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint9_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0
		elif treasure_number == 10:
			if update_data.treasure10 == None:
				update_data.treasure10 = datetime.datetime.now()
				if watched_hint.hint10_3 != None:
					update_data.points += 1
					getpointnow = 1
				elif watched_hint.hint10_2 != None:
					update_data.points += 2
					getpointnow = 2
				else:
					update_data.points += 3
					getpointnow = 3
			else:
				getpointnow = 0

		update_data.save()

		#ここにポイント計算のこと書く？
		return JsonResponse({"treasure":treasure_number, "totalpoint":update_data.points, "getpoint":getpointnow}, safe=False)
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#とんできたビーコンの番号から、どの宝かを識別
def treasure_num(get_major, get_minor):
	data = Treasure_Beacon.objects.get(major=get_major, minor=get_minor)
	treasure_number = data.treasure
	return treasure_number
'''
# 初めてヒント見たときに呼ばれる
@csrf_exempt
def first(request):
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
		first_hint = u'ヒント1\n' + first_hint + u'\n'
		return JsonResponse({"hint1":first_hint})
	else:
		response = HttpResponse()
		response['msg'] = 'NG'
'''

# 2個目以降のヒント使うときによばれる
@csrf_exempt
def hint(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		tag = datas["treasureNo"]
		treasureNo = 'treasure' + str(tag)
		next_watch = datas["next_watch"]

		hint, hint_num = hint_check(name, tag, next_watch)

		return JsonResponse({"hint":hint, "hint_num":hint_num})
	else:
		response = HttpResponse()
		response['msg'] = 'NG'

#どれだけヒント使ってきたかをチェック まだ未完成　書き換え必須
def hint_check(name, treasureNo, next_watch):
	data = UsedHint.objects.get(username = name)

	#次を見るがtrueかfalseかを受け取るnext_watch
	if treasureNo == 1:
		#とりあえず飛んできた瞬間にhintにhint1を追加
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		#次を見るって押されてかつ2つ目のhintがNoneなら時間追加してhint_2を返す
		if next_watch == True and data.hint1_2 == None:
			hint_num = 2
			data.hint1_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		#次を見るって押されてかつ3つ目のhintがNoneなら時間追加してhint_2とhint_3を返す
		elif next_watch == True and data.hint1_3 == None:
			hint_num = 3
			data.hint1_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint1_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint1_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 2:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint2_2 == None:
			hint_num = 2
			data.hint2_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint2_3 == None:
			hint_num = 3
			data.hint2_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint2_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint2_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 3:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint3_2 == None:
			hint_num = 2
			data.hint3_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint3_3 == None:
			hint_num = 3
			data.hint3_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint3_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint3_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 4:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint4_2 == None:
			hint_num = 2
			data.hint4_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint4_3 == None:
			hint_num = 3
			data.hint4_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint4_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint4_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 5:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint5_2 == None:
			hint_num = 2
			data.hint5_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint5_3 == None:
			hint_num = 3
			data.hint5_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint5_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint5_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 6:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint6_2 == None:
			hint_num = 2
			data.hint6_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint6_3 == None:
			hint_num = 3
			data.hint6_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint6_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint6_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 7:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint7_2 == None:
			hint_num = 2
			data.hint7_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint7_3 == None:
			hint_num = 3
			data.hint7_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint7_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint7_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 8:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint8_2 == None:
			hint_num = 2
			data.hint8_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint8_3 == None:
			hint_num = 3
			data.hint8_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint8_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint8_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 9:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint9_2 == None:
			hint_num = 2
			data.hint9_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint9_3 == None:
			hint_num = 3
			data.hint9_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint9_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint9_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'

	elif treasureNo == 10:
		hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 1)
		hint = u'ヒント1\n' + hintdatas.hint_sent + u'\n\n'
		if next_watch == True and data.hint10_2 == None:
			hint_num = 2
			data.hint10_2 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
		elif next_watch == True and data.hint10_3 == None:
			hint_num = 3
			data.hint10_3 = datetime.datetime.now()
			data.save()
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
			hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
			hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n'
		elif next_watch == False:
			if data.hint10_2 == None:
				hint_num = 1
				hint = hint
			elif data.hint10_3 == None:
				hint_num = 2
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
			else:
				hint_num = 3
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 2)
				hint = hint + u'ヒント2\n' + hintdatas.hint_sent + u'\n\n'
				hintdatas = Hint.objects.get(treasure_num = treasureNo, hint_num = 3)
				hint = hint + u'ヒント3\n' + hintdatas.hint_sent + u'\n\n'
	else:
		print 'error'

	return hint, hint_num


#ショップリスト送る
@csrf_exempt
def shop_loading(request):
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

		shop_list=[]
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

#mapの画像作成
@csrf_exempt
def map(request):
	if request.method == 'POST':
		pic_url = []
		datas = json.loads(request.body)

		username = datas.values()

		pic_url.append("https://kinopio.mxd.media.ritsumei.ac.jp/static/img/Map_" + username[0].encode('utf_8') + "_1F.png")
		pic_url.append("https://kinopio.mxd.media.ritsumei.ac.jp/static/img/Map_" + username[0].encode('utf_8') + "_2F.png")
		pic_url.append("https://kinopio.mxd.media.ritsumei.ac.jp/static/img/Map_" + username[0].encode('utf_8') + "_3F.png")
		
		print pic_str

		return JsonResponse({"map":pic_url})

	else:
		response = HttpResponse()
		response['msg'] = 'NG'


#csvとして出力する
@csrf_exempt
def export_csv(request):
	userdata = User.objects.all()

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="userdata.csv"'

	writer = csv.writer(response)

	for i in userdata:
		writer.writerow([
			"%s" % unicodedata.normalize('NFKC', i.username).encode('sjis','ignore'),
			"%d" % i.points,
			"%s" % i.starttime,
			"%s" % i.finishtime,
			"%s" % i.treasure1,
			"%s" % i.treasure2,
			"%s" % i.treasure3,
			"%s" % i.treasure4,
			"%s" % i.treasure5,
			"%s" % i.treasure6,
			"%s" % i.treasure7,
			"%s" % i.treasure8,
			"%s" % i.treasure9,
			"%s" % i.treasure10,
			"%s" % unicodedata.normalize('NFKC', i.shopname).encode('sjis','ignore'),
		])

	return response

@csrf_exempt
def finish(request):
	if request.method == 'POST':
		datas = json.loads(request.body)
		name = datas["name"]   # ダブルクオート内はディクショナリーのキー
		User_Data = User.objects.get(username = name)
		UserId = User_Data.user_id
		Point = User_Data.points
		User_Data.finishtime = datetime.datetime.now()
		User_Data.save()

		return JsonResponse({"id":UserId, "point":Point})
	else:
		response = HttpResponse()
		response['msg'] = 'NG'
