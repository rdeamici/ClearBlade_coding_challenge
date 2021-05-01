import string
import json
from time import sleep
from bluepy.btle import Scanner, DefaultDelegate
from clearblade.ClearBladeCore import System,Query, Developer


# get BLE devices in range
scanner = Scanner()
devices = scanner.scan(4.0)
msgs = []
addrs = []
for dev in devices:
	if dev.addr not in addrs:
		addrs.append(dev.addr)
		msg={'address':dev.addr}

		# get device name if it has one
		for (sdtype, desc, value) in dev.getScanData():
			# remove non-printable characters from value
			value = filter(lambda x:x in string.printable, value)
			if 'name' in desc.lower() and value:
				msg['name'] = value

		msgs.append(msg)

	else:
		print('found duplicate addr')
		print(addrs)
		print(dev.addr)

#send message to Broker
SystemKey = 'b2adc7880cc2ba98aaeb8fe3e2e501'
SystemSecret = 'B2ADC7880CB8C6C4F1D9E380CE9C01'
admin_email = 'rtdeamicis@gmail.com'
admin_pw = 'H1r3m3pls'

mySystem = System(SystemKey, SystemSecret)
admin = mySystem.User(admin_email, admin_pw)

mqtt = mySystem.Messaging(admin)

mqtt.connect()
for msg in msgs:
	print(json.dumps(msg)) # debug print statement
	mqtt.publish('ble/_platform',json.dumps(msg))
	sleep(1)
mqtt.disconnect()

