from __future__ import unicode_literals

from django.db import models

# Create your models here.
#default ha nyuuryoku ga kara no toki ni hyouji sareru moji
class Data(models.Model):
	userdata = models.CharField('username', max_length = 255, default = 'NAME')
	datavalue = models.CharField('shop', max_length = 255, default = 'SHOP')

class User(models.Model):
	username = models.CharField('username', max_length = 255, default = 'NAME')
	starttime = models.IntegerField('starttime', default = 0)
	finishtime = models.IntegerField('finishtime', default = 0)
	hint_action1_1 = models.BooleanField('hint1_1', default = False)
