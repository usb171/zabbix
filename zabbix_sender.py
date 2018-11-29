import subprocess
from ZabbixSender import ZabbixSender, ZabbixPacket

_HOST = "SENSORES"
_PORT_ZABBIX = 10051
_SERVER_ZABBIX = "zabbixcv.ddns.net"

server = ZabbixSender(_SERVER_ZABBIX, _PORT_ZABBIX)
packet = ZabbixPacket()

temp = float(subprocess.Popen("mosquitto_sub -h srcv.ddns.net -p 9999 -t 002/temp -C 1", shell=True, stdout=subprocess.PIPE).stdout.read().decode())
humi = float(subprocess.Popen("mosquitto_sub -h srcv.ddns.net -p 9999 -t 002/humi -C 1", shell=True, stdout=subprocess.PIPE).stdout.read().decode())
packet.add(_HOST,'temp', temp)
packet.add(_HOST,'humi', humi)
server.send(packet)
print(server.status)


