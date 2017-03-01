from __future__ import unicode_literals

from django.db import models

# Create your models here.
#default ha nyuuryoku ga kara no toki ni hyouji sareru moji
class Data(models.Model):
	userdata = models.CharField('username', max_length = 255, default = 'NAME')
	datavalue = models.CharField('shop', max_length = 255, default = 'SHOP')