#!/bin/bash

cp /opt/crb/user_inventory.sh /opt/user_inventory_real.sh

manufacturer=$(/usr/sbin/dmidecode -s chassis-manufacturer)
# hack because the first serial number is blank on s10-3
serial=$(/usr/sbin/dmidecode | /bin/grep -E 'Serial Number:[[:space:]]*[^[:space:]]+' | /bin/sed 's/.*: \(.*\)/\1/;q')
model=$(/usr/sbin/dmidecode -s system-product-name)
dCount=$(/sbin/fdisk -l | /bin/grep '^Disk /dev/' | wc -l)

/bin/sed -i "s/<manufacturer>/$(echo $manufacturer)/g" /opt/user_inventory_real.sh
/bin/sed -i "s/<serial>/$(echo $serial)/g" /opt/user_inventory_real.sh
/bin/sed -i "s/<model>/$(echo $model)/g" /opt/user_inventory_real.sh
/bin/sed -i "s/<dCount>/$(echo $dCount)/g" /opt/user_inventory_real.sh
