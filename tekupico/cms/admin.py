from django.contrib import admin
from cms.models import *
# Register your models here.
#admin.site.register(Data)

class UserAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'username', 'starttime', 'finishtime', 'treasures', 'points', 'relationship', 'Parents',)
	list_display_links = ('username',)
	search_fields = ['user_id', 'username',]

class UsedHintAdmin(admin.ModelAdmin):
	list_display = ('username',)
	list_display_links = ('username',)

class BeaconAdmin(admin.ModelAdmin):
	list_display = ('beacon_id', 'uuid', 'major', 'minor', 'category',)
	list_display_links = ('beacon_id',)

class Shop_BeaconAdmin(admin.ModelAdmin):
	list_display = ('shopname', 'shop_id', 'major', 'minor', 'floor')
	list_display_links = ('shopname', 'shop_id', 'major', 'minor',)
	search_fields = ['shopname', 'floor']

class TreasureAdmin(admin.ModelAdmin):
	list_display = ('treasure', 'beacon_id',)
	list_display_links = ('treasure', 'beacon_id',)

class HintAdmin(admin.ModelAdmin):
	list_display = ('treasure_num', 'hint_num', 'hint_sent',)
	list_display_links = ('hint_num', 'hint_sent',)

class DataAdmin(admin.ModelAdmin):
	list_display = ('userdata', 'datavalue',)
	list_display_links = ('userdata',)

class KeyAreaAdmin(admin.ModelAdmin):
	list_display = ('major', 'minor', 'xgrid', 'ygrid',)
	list_display_links = ('major', 'minor',)

class Shop_ladiesAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_mensAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_mensladiesAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_kidsAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_familyAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_innerAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_bagAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_shoesAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_varietyAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_jewelryAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_cosmeticsAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_otherAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)


admin.site.register(User, UserAdmin)
admin.site.register(UsedHint, UsedHintAdmin)
admin.site.register(Beacon, BeaconAdmin)
admin.site.register(Shop_Beacon, Shop_BeaconAdmin)
admin.site.register(Treasure_Beacon, TreasureAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(KeyArea, KeyAreaAdmin)
admin.site.register(Shop_ladies, Shop_ladiesAdmin)
admin.site.register(Shop_mens, Shop_mensAdmin)
admin.site.register(Shop_mensladies, Shop_mensladiesAdmin)
admin.site.register(Shop_kids, Shop_kidsAdmin)
admin.site.register(Shop_family, Shop_familyAdmin)
admin.site.register(Shop_inner, Shop_innerAdmin)
admin.site.register(Shop_bag, Shop_bagAdmin)
admin.site.register(Shop_shoes, Shop_shoesAdmin)
admin.site.register(Shop_variety, Shop_varietyAdmin)
admin.site.register(Shop_jewelry, Shop_jewelryAdmin)
admin.site.register(Shop_cosmetics, Shop_cosmeticsAdmin)
admin.site.register(Shop_other, Shop_otherAdmin)
