from django.contrib import admin

from it_inventory.models import *

class ComputerAdmin(admin.ModelAdmin):
    list_display = ['csmanufacturer', 'csusername', 'csname', 'csmodel',
                    'cstotalphysicalmemory', 'dfreespace', 'oscaption','osversion','osservicepackmajorversion',
                    'osinstalldate','pmanufacturer','pname','xclientaddress','xupdated']
    list_filter = ['oscaption','osversion', 'csmodel']
    search_fields = ['bserialnumber','csmanufacturer', 'csusername', 'csname', 'csmodel',
                    'oscaption','osversion','pmanufacturer','pname','xclientaddress']
    list_filter = ['oscaption','osversion', 'csmodel']
admin.site.register(Computer, ComputerAdmin)
