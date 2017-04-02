from django.contrib import admin
from cms.models import *
# Register your models here.
#admin.site.register(Data)

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'starttime', 'finishtime', 'treasure1', 'treasure2', 'treasure3', 'treasure4', 'treasure5', 'treasure6', 'treasure7', 'treasure8', 'treasure9', 'treasure10')
	list_display_links = ('username',)

class UsedHintAdmin(admin.ModelAdmin):
	list_display = ('username',)
	list_display_links = ('username',)

class BeaconAdmin(admin.ModelAdmin):
	list_display = ('beacon_id', 'uuid', 'major', 'minor', 'category',)
	list_display_links = ('beacon_id',)

class Shop_BeaconAdmin(admin.ModelAdmin):
	list_display = ('shopname', 'shop_id', 'beacon_id',)
	list_display_links = ('shopname', 'shop_id', 'beacon_id',)

class TreasureAdmin(admin.ModelAdmin):
	list_display = ('treasure', 'beacon_id',)
	list_display_links = ('treasure', 'beacon_id')

class HintAdmin(admin.ModelAdmin):
	list_display = ('treasure_num', 'hint_num', 'hint_sent',)
	list_display_links = ('hint_num', 'hint_sent')

class DataAdmin(admin.ModelAdmin):
	list_display = ('userdata', 'datavalue',)
	list_display_links = ('userdata',)

class KeyAreaAdmin(admin.ModelAdmin):
	list_display = ('beacon_id', 'xgrid', 'ygrid',)
	list_display_links = ('beacon_id',)

class Shop_ladiesAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_mensAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_ladiesmensAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_kidsAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_sportsAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_shoesbagAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_fassiongoodsAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_goodsvarietyAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_accessoryAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_foodAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_serviceAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)

class Shop_limitedAdmin(admin.ModelAdmin):
	list_display = ('shop_name',)


admin.site.register(User, UserAdmin)
admin.site.register(UsedHint, UsedHintAdmin)
admin.site.register(Beacon, BeaconAdmin)
admin.site.register(Shop_Beacon, Shop_BeaconAdmin)
admin.site.register(Treasure_Beacon, TreasureAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(KeyArea, KeyAreaAdmin)
admin.site.register(Shop_ladies, Shop_ladiesmensAdmin)
admin.site.register(Shop_mens, Shop_mensAdmin)
admin.site.register(Shop_ladiesmens, Shop_ladiesmensAdmin)
admin.site.register(Shop_kids, Shop_kidsAdmin)
admin.site.register(Shop_sports, Shop_sportsAdmin)
admin.site.register(Shop_shoesbag, Shop_shoesbagAdmin)
admin.site.register(Shop_fassiongoods, Shop_fassiongoodsAdmin)
admin.site.register(Shop_goodsvariety, Shop_goodsvarietyAdmin)
admin.site.register(Shop_accessory, Shop_accessoryAdmin)
admin.site.register(Shop_food, Shop_foodAdmin)
admin.site.register(Shop_service, Shop_serviceAdmin)
admin.site.register(Shop_limited, Shop_limitedAdmin)

