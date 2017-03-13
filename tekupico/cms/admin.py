from django.contrib import admin
from cms.models import Data
from cms.models import User
# Register your models here.
#admin.site.register(Data)

class DataAdmin(admin.ModelAdmin):
	list_display = ('userdata', 'datavalue',)
	list_display_links = ('userdata',)

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'starttime', 'finishtime',)
	list_display_links = ('username',)
admin.site.register(Data, DataAdmin)
admin.site.register(User, UserAdmin)
