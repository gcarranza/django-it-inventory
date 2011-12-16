from it_inventory.models import *
from django.core.management.base import BaseCommand, CommandError
import cups
from django.conf import settings


class Command(BaseCommand):
    help = 'Search and add cups printers'
    
    def handle(self, *args, **options):
        cups.setServer(settings.CUPS_SERVER)
        c = cups.Connection()
        printers = c.getPrinters()
        for name, printer in printers.iteritems():
            inv_printer = Printer.objects.get_or_create(name=name)[0]
            inv_printer.location = printer.get('printer-location', '')
            inv_printer.uri = printer.get('printer-uri-supported', '')
            inv_printer.model = printer.get('printer-make-and-model', '')
            inv_printer.save()
