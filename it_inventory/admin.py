from django.contrib import admin

from it_inventory.models import *

class ComputerAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'user', 'hostname', 'model',
                    'memory', 'hd_size_gb', 'hd_percent_free', 'os','os_version',
                    'os_install_date','cpu_name','ip_address','last_updated']
    list_filter = ['os','os_version', 'model']
    search_fields = ['serial_number','manufacturer', 'user', 'hostname', 'model',
                    'os','os_version','ip_address']
admin.site.register(Computer, ComputerAdmin)

class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'state_reason', 'toner_levels',)
admin.site.register(Printer, PrinterAdmin)
