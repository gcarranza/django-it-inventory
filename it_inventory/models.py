from django.db import models
import cups

class Computer(models.Model):
    bserialnumber = models.CharField(max_length=255, db_column='bSerialNumber') 
    csmanufacturer = models.CharField(max_length=255, db_column='csManufacturer') 
    csusername = models.CharField(max_length=255, db_column='csUserName', blank=True) 
    csname = models.CharField(max_length=768, db_column='csName', blank=True) 
    csmodel = models.CharField(max_length=768, db_column='csModel', blank=True) 
    cstotalphysicalmemory = models.BigIntegerField(null=True, db_column='csTotalPhysicalMemory', blank=True) 
    dfilesystem = models.CharField(max_length=768, db_column='dFileSystem', blank=True) 
    dsize = models.BigIntegerField(null=True, db_column='dSize', blank=True) 
    dfreespace = models.BigIntegerField(null=True, db_column='dFreeSpace', blank=True) 
    dcount = models.IntegerField(null=True, db_column='dCount', blank=True) 
    oscaption = models.CharField(max_length=768, db_column='osCaption', blank=True) 
    osversion = models.CharField(max_length=768, db_column='osVersion', blank=True) 
    osservicepackmajorversion = models.IntegerField(null=True, db_column='osServicePackMajorVersion', blank=True) 
    osinstalldate = models.DateTimeField(null=True, db_column='osInstallDate', blank=True) 
    pmanufacturer = models.CharField(max_length=768, db_column='pManufacturer', blank=True) 
    pname = models.CharField(max_length=768, db_column='pName', blank=True) 
    xclientaddress = models.CharField(max_length=120, db_column='xClientAddress', blank=True) 
    xupdated = models.DateTimeField(db_column='xUpdated', blank=True, null=True) 
    battery = models.CharField(max_length=255, blank=True, help_text="Battery information, Linux only")
    class Meta:
        unique_together = (('bserialnumber','csmanufacturer'),)

class Printer(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    uri = models.CharField(max_length=255, blank=True)
    model =  models.CharField(max_length=255, blank=True)
    asset_tag = models.CharField(max_length=255, blank=True)
    
    cups.setServer('cups.cristoreyny.org')
    c = cups.Connection()
    
    @property
    def state(self):
        try:
            return self.c.getPrinterAttributes(name=self.name, requested_attributes=['printer-state-message'])['printer-state-message']
        except:
            c = cups.Connection()
    
    @property
    def state_reason(self):
        try:
            return self.c.getPrinterAttributes(name=self.name, requested_attributes=['printer-state-reasons'])['printer-state-reasons']
        except:
            c = cups.Connection()