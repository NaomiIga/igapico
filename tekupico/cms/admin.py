from django.contrib import admin
from cms.models import *
# Register your models here.
#admin.site.register(Data)

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'starttime', 'finishtime',)
	list_display_links = ('username',)

class UsedhintAdmin(admin.ModelAdmin):
	list_display = ('username', '1_1', '1_2', '1_3',)
	list_display_links = ('username',)

class BeaconAdmin(admin.ModelAdmin):
	list_display = ('beacon_id', 'uuid', 'major', 'minor', 'category',)
	list_display_links = ('beacon_id',)

class ShopAdmin(admin.ModelAdmin):
	list_display = ('shopname', 'shop_id', 'beacon',)
	list_display_links = ('shopname', 'shop_id', 'beacon',)

class TreasureAdmin(admin.ModelAdmin):
	list_display = ('treasure', 'beacon',)
	list_display_links = ('treasure', 'beacon')

class HintAdmin(admin.ModelAdmin):
	list_display = ('hint_num', 'hint_sent',)
	list_display_links = ('hint_num', 'hint_sent')

class DataAdmin(admin.ModelAdmin):
	list_display = ('userdata', 'datavalue',)
	list_display_links = ('userdata',)
admin.site.register(User, UserAdmin)
admin.site.register(UsedHint, UsedhintAdmin)
admin.site.register(Beacon, BeaconAdmin)
admin.site.register(Shop_Beacon, ShopAdmin)
admin.site.register(Treasure_Beacon, TreasureAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Data, DataAdmin)

