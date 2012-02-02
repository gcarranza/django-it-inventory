#!/bin/bash

cp /opt/user_inventory.sh /opt/user_inventory_real.sh

manufacturer=$(/usr/sbin/dmidecode -s chassis-manufacturer)

# hack because the first serial number is blank on s10-3
serial=$(/usr/sbin/dmidecode | /bin/grep -E 'Serial Number:[[:space:]]*[^[:space:]]+' | /bin/sed 's/.*: \(.*\)/\1/;q')

# Hack for Ohava computers that don't fill out serial number
dumb_serial='To be filled by O.E.M.'
if [ "$serial" = "$dumb_serial" ]
then
    serial=$(ifconfig | grep HWaddr | while read line; do echo $line | awk '{ print $1 " " $5 }'; done | sed 1q)
fi

model=$(/usr/sbin/dmidecode -s system-product-name)
dCount=$(/sbin/fdisk -l | /bin/grep '^Disk /dev/' | wc -l)

/bin/sed -i "s/<manufacturer>/$(echo $manufacturer)/g" /opt/user_inventory_real.sh
/bin/sed -i "s/<serial>/$(echo $serial)/g" /opt/user_inventory_real.sh
/bin/sed -i "s/<model>/$(echo $model)/g" /opt/user_inventory_real.sh
/bin/sed -i "s/<dCount>/$(echo $dCount)/g" /opt/user_inventory_real.sh