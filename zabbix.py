#!/usr/bin/env python3
import os
import subprocess

key_temp = "temp"
key_humi = "humi"
_HOST = "SENSORES"
_SERVER_ZABBIX = "localhost"

_SERVER_MQTT = "srcv.ddns.net"
_PORT_MQTT = "9999"
_TOP_TEMP = "002/temp"
_TOP_HUMI = "002/humi"


temp = subprocess.Popen("mosquitto_sub -h %s -p %s -t %s -C 1" % (_SERVER_MQTT, _PORT_MQTT, _TOP_TEMP), shell=True, stdout=subprocess.PIPE).stdout.read().decode()
humi = subprocess.Popen("mosquitto_sub -h %s -p %s -t %s -C 1" % (_SERVER_MQTT, _PORT_MQTT, _TOP_HUMI), shell=True, stdout=subprocess.PIPE).stdout.read().decode()

os.system("zabbix_sender -z '%s' -p 10051 -s '%s' -k '%s' -o '%s'" % (_SERVER_ZABBIX, _HOST, key_temp, temp))
os.system("zabbix_sender -z '%s' -p 10051 -s '%s' -k '%s' -o '%s'" % (_SERVER_ZABBIX, _HOST, key_humi, humi))

