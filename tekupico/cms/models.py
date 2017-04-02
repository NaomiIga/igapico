from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_unicode

# Create your models here.
#default ha nyuuryoku ga kara no toki ni hyouji sareru moji

# User log wo tameru
class User(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	starttime = models.DateTimeField('starttime', null=True, blank=True)
	finishtime = models.DateTimeField('finishtime', null=True, blank=True)
	treasure1 = models.DateTimeField('1time', null=True, blank=True)
	treasure2 = models.DateTimeField('2time', null=True, blank=True)
	treasure3 = models.DateTimeField('3time', null=True, blank=True)
	treasure4 = models.DateTimeField('3time', null=True, blank=True)
	treasure5 = models.DateTimeField('3time', null=True, blank=True)
	treasure6 = models.DateTimeField('3time', null=True, blank=True)
	treasure7 = models.DateTimeField('3time', null=True, blank=True)
	treasure8 = models.DateTimeField('3time', null=True, blank=True)
	treasure9 = models.DateTimeField('3time', null=True, blank=True)
	treasure10 = models.DateTimeField('3time', null=True, blank=True)
	shopname = models.CharField('shopname', max_length = 255, default = 'SHOP')

	def __unicode__(self):
		return smart_unicode(self.username)

# User no hint siyou jyoukyou
class UsedHint(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	treasure1_1 = models.DateTimeField('hint1-1', null=True, blank=True)
	treasure1_2 = models.DateTimeField('hint1-2', null=True, blank=True)
	treasure1_3 = models.DateTimeField('hint1-3', null=True, blank=True)
	treasure2_1 = models.DateTimeField('hint2-1', null=True, blank=True)
	treasure2_2 = models.DateTimeField('hint2-2', null=True, blank=True)
	treasure2_3 = models.DateTimeField('hint2-3', null=True, blank=True)
	treasure3_1 = models.DateTimeField('hint3-1', null=True, blank=True)
	treasure3_2 = models.DateTimeField('hint3-2', null=True, blank=True)
	treasure3_3 = models.DateTimeField('hint3-3', null=True, blank=True)
	treasure4_1 = models.DataTimeField('hint4-1', null=True, blank=True)
	treasure4_2 = models.DataTimeField('hint4-2', null=True, blank=True)
	treasure4_3 = models.DataTimeField('hint4-3', null=True, blank=True)
	treasure5_1 = models.DataTimeField('hint5-1', null=True, blank=True)
	treasure5_2 = models.DataTimeField('hint5-2', null=True, blank=True)
	treasure5_3 = models.DataTimeField('hint5-3', null=True, blank=True)
	treasure6_1 = models.DataTimeField('hint6-1', null=True, blank=True)
	treasure6_2 = models.DataTimeField('hint6-2', null=True, blank=True)
	treasure6_3 = models.DataTimeField('hint6-3', null=True, blank=True)
	treasure7_1 = models.DataTimeField('hint7-1', null=True, blank=True)
	treasure7_2 = models.DataTimeField('hint7-2', null=True, blank=True)
	treasure7_3 = models.DataTimeField('hint7-3', null=True, blank=True)
	treasure8_1 = models.DataTimeField('hint8-1', null=True, blank=True)
	treasure8_2 = models.DataTimeField('hint8-2', null=True, blank=True)
	treasure8_3 = models.DataTimeField('hint8-3', null=True, blank=True)
	treasure9_1 = models.DataTimeField('hint9-1', null=True, blank=True)
	treasure9_2 = models.DataTimeField('hint9-2', null=True, blank=True)
	treasure9_3 = models.DataTimeField('hint9-3', null=True, blank=True)
	treasure10_1 = models.DataTimeField('hint10-1', null=True, blank=True)
	treasure10_2 = models.DataTimeField('hint10-2', null=True, blank=True)
	treasure10_3 = models.DataTimeField('hint10-3', null=True, blank=True)
	


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

# Not Change: beacon list
class Beacon(models.Model):
	beacon_id = models.IntegerField('beacon', default = 0)
	uuid = models.IntegerField('uuid', default = 0)
	major = models.IntegerField('major', default = 0)
	minor = models.IntegerField('minor', default = 0)
	category = models.CharField('category', max_length = 255, default = 'CATEGORY')

# Not Change: Hint list
class Hint(models.Model):
	treasure_num = models.IntegerField('treasure_num', default = 0)
	hint_num = models.IntegerField('hint_num', default = 0)
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
