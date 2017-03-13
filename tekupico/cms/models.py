from __future__ import unicode_literals

from django.db import models

# Create your models here.
#default ha nyuuryoku ga kara no toki ni hyouji sareru moji
class User(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	starttime = models.IntegerField('starttime', default = 0)
	finishtime = models.IntegerField('finishtime', default = 0)
	hint_action1_1 = models.IntegerField('hint1_1', default = 0)
	treasure1 = models.IntegerField('treasure1', default = 0)

class Treasure_Beacon(models.Model):
	treasure = models.IntegerField('treasure', default = 0)
	beacon = models.IntegerField('beacon', default = 0)

class Shop_Beacon(models.Model):
	shopname = models.CharField('shopname', max_length = 255, default = 'SHOPNAME')
	shop_id = models.IntegerField('shop_id', default = 0)
	beacon = models.IntegerField('beacon', default = 0)

class Beacon(models.Model):
	beacon = models.IntegerField('beacon', default = 0)
	major = models.IntegerField('major', default = 0)
	minor = models.IntegerField('minor', default = 0)

class Hint(models.Model):
	hint_num = models.IntegerField('hint_number', default = 0)
	hint_sent = models.CharField('hint_sentence', max_length = 255, default = 'HINT')

class Data(models.Model):
	userdata = models.CharField('username', max_length = 255, default = 'NAME')
	datavalue = models.CharField('shop', max_length = 255, default = 'SHOP')
