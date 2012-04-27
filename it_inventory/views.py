from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from it_inventory.models import *
import datetime

def get_post_or_none(post, key, return_blank=True, is_datetime=False):
    if is_datetime:
        try:
            return datetime.datetime.strptime(post[key].split(".")[0], "%Y-%m-%d %H:%M:%S")
        except:
            return None
    if key in post:
        return post[key]
    else:
        if return_blank:
            return ''
        return None

def capture_login(request):
    """
    A computer runs some get data to the server and this view collects it
    """
    if not request.GET:
        return HttpResponse('Y U NO SEND DATA!?')
    data = request.GET
    computer = Computer.objects.get_or_create(
        serial_number = data['bSerialNumber'],
        manufacturer = data['csManufacturer'],   
    )[0]
    computer.user = get_post_or_none(data,'csUserName')
    computer.hostname = get_post_or_none(data,'csName')
    computer.model = get_post_or_none(data,'csModel')
    computer.memory = get_post_or_none(data,'csTotalPhysicalMemory',True)
    computer.hd_filesystem = get_post_or_none(data,'dFilesystem')
    computer.hd_size = get_post_or_none(data,'dSize',True)
    computer.hd_freespace = get_post_or_none(data,'dFreeSpace',True)
    computer.hd_count = get_post_or_none(data,'dCount',True)
    computer.os = get_post_or_none(data,'osCaption')
    computer.os_version = get_post_or_none(data,'osVersion')
    #computer.os_service_pack = get_post_or_none(data,'osServicePackMajorVersion',True)
    computer.os_install_date = get_post_or_none(data,'osInstallDate',is_datetime=True)
    computer.cpu_manufacturer = get_post_or_none(data,'pManufacturer')
    computer.cpu_name = get_post_or_none(data,'pName')
    computer.ip_address = get_post_or_none(data,'xClientAddress')
    computer.battery_design = get_post_or_none(data,'battery_design')
    computer.battery_full = get_post_or_none(data,'battery_full')
    computer.mac_addr = get_post_or_none(data,'mac_addr')
    computer.save()
    return HttpResponse('Great Success!')