import time
import paho.mqtt.client as mqtt
from ZabbixSender import ZabbixSender, ZabbixPacket

_SLEEP = 5

_PORT_MQTT = 9999
_SERVER_MQTT = "srcv.ddns.net"

_HOST = "SENSORES"
_PORT_ZABBIX = 10051
_SERVER_ZABBIX = "zabbixcv.ddns.net"

_TOPC_TEMP = "002/temp"
_TOPC_HUMI = "002/humi"


client = mqtt.Client()
client.connect(_SERVER_MQTT, _PORT_MQTT, 60)
server = ZabbixSender(_SERVER_ZABBIX, _PORT_ZABBIX)

def on_connect(client, userdata, flags, rc):
    client.subscribe(_TOPC_TEMP)
    client.subscribe(_TOPC_HUMI)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(float(msg.payload)))

    packet = ZabbixPacket()

    if msg.topic == _TOPC_TEMP:
    	packet.add(_HOST,'temp', float(msg.payload))
    	server.send(packet)
    	print(server.status)
    elif msg.topic == _TOPC_HUMI:
    	packet.add(_HOST,'humi', float(msg.payload))
    	server.send(packet)
    	print(server.status)

    del packet
    time.sleep(_SLEEP)

   
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()


