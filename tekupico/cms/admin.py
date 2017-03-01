from django.contrib import admin
from cms.models import Data
# Register your models here.
#admin.site.register(Data)

class DaraAdmin(admin.ModelAdmin):
	list_display = ('userdata', 'datavalue',)
	list_display_links = ('userdata',)
admin.site.register(Data, DaraAdmin)