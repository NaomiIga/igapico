from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
#default ha nyuuryoku ga kara no toki ni hyouji sareru moji

# User log wo tameru
class User(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	starttime = models.DateTimeField('starttime', null=True, blank=True)
	finishtime = models.DateTimeField('finishtime', null=True, blank=True)
	#treasure1 = models.DateTimeField(default=timezone.now)
	#treasure2 = models.DateTimeField(default=timezone.now)
	#treasure3 = models.DateTimeField(default=timezone.now)
	treasure1 = models.DateTimeField('1time', null=True, blank=True)
	treasure2 = models.DateTimeField('2time', null=True, blank=True)
	treasure3 = models.DateTimeField('3time', null=True, blank=True)
	shopname = models.CharField('shopname', max_length = 255, default = 'SHOP')

# User no hint siyou jyoukyou
class UsedHint(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	treasure1 = models.DateTimeField('hint1-1', null=True, blank=True)
	treasure2 = models.DateTimeField('hint2-1', null=True, blank=True)
	treasure3 = models.DateTimeField('hint3-1', null=True, blank=True)
	#treasure1 = models.IntegerField('1_1time', default = 0)
	#treasure1_2 = models.IntegerField('1_2time', default = 0)
	#treasure1_3 = models.IntegerField('1_3time', default = 0)
	#treasure2 = models.IntegerField('2_1time', default = 0)
	#treasure2_2 = models.IntegerField('2_2time', default = 0)
	#treasure2_3 = models.IntegerField('2_3time', default = 0)
	#treasure3 = models.IntegerField('3_1time', default = 0)
	#treasure3_2 = models.IntegerField('3_2time', default = 0)
	#treasure3_3 = models.IntegerField('3_3time', default = 0)


# Not Change: treasure and beaconNo wo himoduke
class Treasure_Beacon(models.Model):
	treasure = models.IntegerField('treasure', default = 0)
	beacon_id = models.IntegerField('beacon', default = 0)
	major = models.IntegerField('major', default = 0)
	minor = models.IntegerField('minor', default = 0)

# Not Change: ikitaiSHOP to beaconNo wo himoduke
class Shop_Beacon(models.Model):
	shopname = models.CharField('shopname', max_length = 255, default = 'SHOPNAME')
	shop_id = models.IntegerField('shop_id', default = 0)
	beacon_id = models.IntegerField('beacon', default = 0)
	major = models.IntegerField('major', default = 0)
	minor = models.IntegerField('minor', default = 0)

# Not Change: beacon list
class Beacon(models.Model):
	beacon_id = models.IntegerField('beacon', default = 0)
	uuid = models.IntegerField('uuid', default = 0)
	major = models.IntegerField('major', default = 0)
	minor = models.IntegerField('minor', default = 0)
	category = models.CharField('category', max_length = 255, default = 'CATEGORY')

# Not Change: Hint list
class Hint(models.Model):
	hint_num = models.IntegerField('hint_number', default = 0)
	hint_sent = models.CharField('hint_sentence', max_length = 255, default = 'HINT')

# Not Changed: Shop List(ladies)
class Shop_ladies(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(mens)
class Shop_mens(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(ladies/mens)
class Shop_ladiesmens(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(kids)
class Shop_kids(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(sports/outdor)
class Shop_sports(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(shoes/bag)
class Shop_shoesbag(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(fassiongooss)
class Shop_fassiongoods(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(goods/variety)
class Shop_goodsvariety(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(watch/accessory)
class Shop_accessory(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(food)
class Shop_food(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(service)
class Shop_service(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')

# Not Changed: Shop List(limited)
class Shop_limited(models.Model):
	shop_name = models.CharField('shop_name', max_length = 255, default = 'NAME')
# test
class Data(models.Model):
	userdata = models.CharField('username', max_length = 255, default = 'NAME')
	datavalue = models.CharField('shop', max_length = 255, default = 'SHOP')

class KeyArea(models.Model):
	beacon_id = models.IntegerField('beacon', default = 0)
	xgrid = models.IntegerField('x', default = 0)
	ygrid = models.IntegerField('y', default = 0)
