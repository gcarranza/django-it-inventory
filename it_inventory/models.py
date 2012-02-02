from django.db import models
import cups
from django.conf import settings

class Computer(models.Model):
    serial_number = models.CharField(max_length=255, db_column='bSerialNumber') 
    manufacturer = models.CharField(max_length=255, db_column='csManufacturer') 
    user = models.CharField(max_length=255, db_column='csUserName', blank=True) 
    hostname = models.CharField(max_length=768, db_column='csName', blank=True) 
    model = models.CharField(max_length=768, db_column='csModel', blank=True) 
    memory = models.BigIntegerField(null=True, db_column='csTotalPhysicalMemory', blank=True) 
    hd_filesystem = models.CharField(max_length=768, db_column='dFileSystem', blank=True) 
    hd_size = models.BigIntegerField(null=True, db_column='dSize', blank=True) 
    hd_freespace = models.BigIntegerField(null=True, db_column='dFreeSpace', blank=True) 
    hd_count = models.IntegerField(null=True, db_column='dCount', blank=True) 
    os = models.CharField(max_length=768, db_column='osCaption', blank=True) 
    os_version = models.CharField(max_length=768, db_column='osVersion', blank=True) 
    os_service_pack = models.IntegerField(null=True, db_column='osServicePackMajorVersion', blank=True) 
    os_install_date = models.DateTimeField(null=True, db_column='osInstallDate', blank=True) 
    cpu_manufacturer = models.CharField(max_length=768, db_column='pManufacturer', blank=True) 
    cpu_name = models.CharField(max_length=768, db_column='pName', blank=True) 
    ip_address = models.CharField(max_length=120, db_column='xClientAddress', blank=True) 
    last_updated = models.DateTimeField(db_column='xUpdated', auto_now=True, blank=True, null=True) 
    battery_design = models.CharField(max_length=255, blank=True)
    battery_full = models.CharField(max_length=255, blank=True)
    mac_addr = models.TextField(blank=True)
    class Meta:
        unique_together = (('serial_number','manufacturer'),)

class Printer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    model =  models.CharField(max_length=255, blank=True)
    asset_tag = models.CharField(max_length=255, blank=True)
    toner_levels = models.CharField(max_length=1024, blank=True) 
    connection = models.CharField(max_length=1024,blank=True,null=True)
    
    cups.setServer(settings.CUPS_SERVER)
    c = cups.Connection()
    
    def update_data_from_cups(self):
        try:
            all_data = c.getPrinterAttributes(name=self.name)
        except: # Renew connection
            c = cups.Connection()
            all_data = c.getPrinterAttributes(name=self.name)
        self.location = all_data.get('printer-location', '')
        self.uri = all_data.get('printer-uri-supported', '')
        self.model = all_data.get('printer-make-and-model', '')
        self.connection = all_data.get('device-uri','')
        marker_names = all_data.get('marker-names', '')
        marker_levels = all_data.get('marker-levels', '')
        if marker_names and marker_levels:
            toner_txt = ''
            # I've never seen this used.
            #toner_high_level = all_data.get('toner_high_level', '')
            for name, level in zip(marker_names, marker_levels):
                # A value of -1 indicates the level is unavailable, -2 indicates unknown, and -3 indicates the level is unknown but has not yet reached capacity
                print level
                if level != -1 and level != -2:
                    if level == -3:
                        level = "Not at capacity"
                    toner_txt += '%s: %s, ' % (name, level,)
            self.toner_levels = toner_txt[:-2]
        
        self.save()
    
    @property
    def state(self):
        try:
            state = self.c.getPrinterAttributes(name=self.name, requested_attributes=['printer-state'])['printer-state']
        except:
            c = cups.Connection()
            state = self.c.getPrinterAttributes(name=self.name, requested_attributes=['printer-state'])['printer-state']
        if state == 3:
            return "Idle"
        elif state == 4:
            return "Printing"
        elif state == 5:
            return "Stopped"
        else:
            return state
    
    @property
    def state_reason(self):
        try:
            state_reasons = self.c.getPrinterAttributes(name=self.name, requested_attributes=['printer-state-reasons'])['printer-state-reasons']
            txt = ''
            for reason in state_reasons:
                txt += '%s, ' % (reason,)
            return txt[:-2]
        except:
            c = cups.Connection()
