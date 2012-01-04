#!/bin/bash

function encode() {
   echo -n "$1" | od -A n -t x1 | tr -d '\n' | tr ' ' '%'
}

manufacturer='<manufacturer>'
serial='<serial>'
model='<model>'
dCount='<dCount>'
hostname=$(hostname)
memory=$(free -b | grep Mem: | awk '{ print $2; }')
dFileSystem=$(cat /etc/mtab | cut -d ' ' -f 2-3 | grep '^/ ' | cut -d ' ' -f 2)
dSize=$(df -B 1 / | sed -n 2p | awk '{ print $2; }')
dFreeSpace=$(df -B 1 / | sed -n 2p | awk '{ print $4; }')
os=$(lsb_release -d | cut -f 2)
os_version=$(uname -srvm)
osInstallDate=$(stat -c %y /var/log/installer)
pManufacturer=$(cat /proc/cpuinfo | grep vendor_id | sed 's/^[^:]*: //;q')
pName=$(cat /proc/cpuinfo | grep 'model name' | sed 's/^[^:]*: //;q')
user=$(whoami)
battery_design=$(cat /proc/acpi/battery/BAT0/info | grep -m1 'design capacity' | awk '{ print $3; }')
battery_full=$(cat /proc/acpi/battery/BAT0/info | grep -m1 'last full cap' | awk '{ print $4; }')
mac_addr=$(ifconfig | grep HWaddr | while read line; do echo $line | awk '{ print $1 " " $5 }'; done)

sRequest="http://10.4.5.23/inventory/capture_login?"
sRequest=$sRequest$"&bSerialNumber="$(encode "$serial")
sRequest=$sRequest$"&csManufacturer="$(encode "$manufacturer")
sRequest=$sRequest$"&csUserName="$(encode "$user")
sRequest=$sRequest$"&csModel="$(encode "$model")
sRequest=$sRequest$"&csName="$(encode "$hostname")
sRequest=$sRequest$"&csTotalPhysicalMemory="$(encode "$memory")
sRequest=$sRequest$"&dFileSystem="$(encode "$dFileSystem")
sRequest=$sRequest$"&dSize="$(encode "$dSize")
sRequest=$sRequest$"&dFreeSpace="$(encode "$dFreeSpace")
sRequest=$sRequest$"&dCount="$(encode "$dCount")
sRequest=$sRequest$"&osCaption="$(encode "$os")
sRequest=$sRequest$"&osInstallDate="$(encode "$osInstallDate")
sRequest=$sRequest$"&osVersion="$(encode "$os_version")
sRequest=$sRequest$"&pManufacturer="$(encode "$pManufacturer")
sRequest=$sRequest$"&pName="$(encode "$pName")
sRequest=$sRequest$"&battery_design="$(encode "$battery_design")
sRequest=$sRequest$"&battery_full="$(encode "$battery_full")
sRequest=$sRequest$"&mac_addr="$(encode "$mac_addr")

wget "$sRequest" -o /dev/null
