from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
#default ha nyuuryoku ga kara no toki ni hyouji sareru moji

# User log wo tameru
class User(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	starttime = models.IntegerField('starttime', default = 0)
	finishtime = models.IntegerField('finishtime', default = 0)
	treasure1 = models.DateTimeField('treasure1', default = 0)
	treasure2 = models.DateTimeField('treasure2', default = 0)
	treasure3 = models.DateTimeField('treasure3', default = 0)
	shopname = models.CharField('shopname', max_length = 255, default = 'SHOP')

# User no hint siyou jyoukyou
class UsedHint(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	#treasure1 = models.DateTimeField(default = timezone.now)
	#treasure2 = models.DateTimeField(default = timezone.now)
	#treasure3 = models.DateTimeField(default = timezone.now)
	treasure1_1 = models.IntegerField('1_1time', default = 0)
	treasure1_2 = models.IntegerField('1_2time', default = 0)
	treasure1_3 = models.IntegerField('1_3time', default = 0)
	#treasure2_1 = models.IntegerField('2_1time', default = 0)
	#treasure2_2 = models.IntegerField('2_2time', default = 0)
	#treasure2_3 = models.IntegerField('2_3time', default = 0)
	#treasure3_1 = models.IntegerField('3_1time', default = 0)
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

# test
class Data(models.Model):
	userdata = models.CharField('username', max_length = 255, default = 'NAME')
	datavalue = models.CharField('shop', max_length = 255, default = 'SHOP')
