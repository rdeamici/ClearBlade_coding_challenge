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
		msg={'addr':dev.addr}

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
SystemKey = 'c4dfbc880ce891a09fe8eb92eb9d01'
SystemSecret = 'C4DFBC880CC0D8A8B5FCE5B4DB44'
admin_email = 'rtdeamicis@gmail.com'
admin_pw = 'H1r3m3pls'

mySystem = System(SystemKey, SystemSecret)
admin = mySystem.User(admin_email, admin_pw)

mqtt = mySystem.Messaging(admin)

mqtt.connect()
for msg in msgs:
	print(json.dumps(msg)) # debug print statement
	mqtt.publish('ble/_platform',json.dumps(msg))
#	resp = code.execute(admin)
	sleep(1)
mqtt.disconnect()

