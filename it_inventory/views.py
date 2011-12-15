from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from it_inventory.models import *

def get_post_or_none(post, key, integer=False):
    if key in post:
        return post[key]
    else:
        if integer:
            return None
        return ''

@permission_required('inventory.change_computer')
def capture_login(request):
    """
    A computer runs some get data to the server and this view collects it
    """
    if not request.GET:
        return HttpResponse('Y U NO SEND DATA!?')
    data = request.GET
    computer = Computer.objects.get_or_create(
        bserialnumber = data['bSerialNumber'],
        csmanufacturer = data['csManufacturer'],   
    )[0]
    computer.csusername = get_post_or_none(data,'csUserName')
    computer.csname = get_post_or_none(data,'csName')
    computer.csmodel = get_post_or_none(data,'csModel')
    computer.cstotalphysicalmemory = get_post_or_none(data,'csTotalPhysicalMemory',True)
    computer.dfilesystem = get_post_or_none(data,'dFilesystem')
    computer.dsize = get_post_or_none(data,'dDize',True)
    computer.dfreespace = get_post_or_none(data,'dFreeSpace',True)
    computer.dcount = get_post_or_none(data,'dCount',True)
    computer.oscaption = get_post_or_none(data,'osCaption')
    computer.osversion = get_post_or_none(data,'osVersion')
    computer.osservicepackmajorversion = get_post_or_none(data,'osServicePackMajorVersion',True)
    #computer.osinstalldate = get_post_or_none(data,'osInstallDate')
    computer.pmanufacturer = get_post_or_none(data,'pManufacturer')
    computer.pname = get_post_or_none(data,'pName')
    computer.xclientaddress = get_post_or_none(data,'xClientAddress')
    #computer.xupdated = get_post_or_none(data,'xUpdated')
    computer.save()
    return HttpResponse('Great Success!')