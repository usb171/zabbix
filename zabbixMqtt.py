import sys
import subprocess
from ZabbixSender import ZabbixSender, ZabbixPacket




class ZabbixMqttSender(object):
	"""docstring for ZabbixMqttSender"""
	def __init__(self, mqtt, portMqtt, zabbix, portZabbix, host, topc, key, form):
		super(ZabbixMqttSender, self).__init__()
		self.key = str(key)
		self.host = str(host)
		self.form = str(form)
		self.topc = str(topc)
		self.mqtt = str(mqtt)
		self.zabbix = str(zabbix)
		self.portMqtt = str(portMqtt)
		self.portZabbix = int(portZabbix)

		self.server = None
		self.packet = None

	def connectZabbixServer(self):
		self.server = ZabbixSender(self.zabbix, self.portZabbix)
		self.packet = ZabbixPacket()

	def send(self):
		value = subprocess.Popen("mosquitto_sub -h " + self.mqtt + " -p " + self.portMqtt + " -t " + self.topc + " -C 1", shell=True, stdout=subprocess.PIPE).stdout.read().decode()
		if self.form == "float":
			value = float(value)
		elif self.form == "int":
			value = int(float(value))
		elif self.form == "text":
			value = str(value)
		print(value)
		self.packet.add(self.host, self.key, value)
		self.server.send(self.packet)
		print(self.server.status)



def printHelper():
	print("\t-H\t\t Help")
	print("\t-f\t\t Format type value zabbix")
	print("\t-h\t\t Host Zabbix")
	print("\t-t\t\t Topic MQTT")
	print("\t-m\t\t Server MQTT")
	print("\t-z\t\t Server Zabbix")
	print("\t-k\t\t Key Zabbix")
	print("\t-pm\t\t Port Server MQTT")
	print("\t-pz\t\t Port Server Zabbix")
	print("")



if __name__ == '__main__':
	
	argv = sys.argv
	argSize = len(argv)

	try:
		mqtt = argv[argv.index("-m") + 1]
		zabbix = argv[argv.index("-z") + 1]
		portMqtt = argv[argv.index("-pm") + 1]
		portZabbix = argv[argv.index("-pz") + 1]
		topc = argv[argv.index("-t") + 1]
		host = argv[argv.index("-h") + 1]
		key = argv[argv.index("-k") + 1]
		form = argv[argv.index("-f") + 1]
	except ValueError:
		print("\n\tERRO de Parâmetro!!")
		print("\n\tEX: python3 zabbixMqtt.py -m srcv.ddns.net -pm 9999 -z zabbixcv.ddns.net -pz 10051 -h SENSORES -t 002/temp -k temp -f float\n")
		printHelper()
		quit()

	except IndexError:
		print("\n\tERRO de Parâmetro!!")
		print("\n\tEX: python3 zabbixMqtt.py -m srcv.ddns.net -pm 9999 -z zabbixcv.ddns.net -pz 10051 -h SENSORES -t 002/temp -k temp -f float\n")
		printHelper()
		quit()
			
	try:
		if argSize < 8:
			print("ZabbixMqttSender Helper\n")
			printHelper()
		else:
			'''
			print(mqtt)
			print(portMqtt)
			print(zabbix)
			print(portZabbix)
			print(host)
			print(topc)
			print(key)
			print(form)
			'''
			obj = ZabbixMqttSender(mqtt=mqtt, portMqtt=portMqtt, zabbix=zabbix, portZabbix=portZabbix, host=host, topc=topc, key=key, form=form)
			obj.connectZabbixServer()
			obj.send()

	except Exception as e:
		print(e)
		raise e
	
	



