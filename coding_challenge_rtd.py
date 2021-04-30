import string
from bluepy.btle import Scanner, DefaultDelegate
from clearblade.ClearBladeCore import System,Query, Developer


# get BLE devices in range
scanner = Scanner()
devices = scanner.scan(6.0)
addr_names = []
for dev in devices:
	addr = dev.addr
	name = ''

	for (sdtype, desc, value) in dev.getScanData():
		# remove non-printable characters from value
		value = filter(lambda x:x in string.printable, value)
		if 'name' in desc.lower() and value:
			name = value


	if name: name = '\tname: "{}"'.format(repr(name))

	msg = 'addr: {}{}'.format(addr, name)



#send message to Broker
SystemKey = 'c4dfbc880ce891a09fe8eb92eb9d01'
SystemSecret = 'C4DFBC880CC0D8A8B5FCE5B4DB44'
admin_email = 'rtdeamicis@gmail.com'
admin_pw = 'H1r3m3pls'

mySystem = System(SystemKey, SystemSecret)

admin = mySystem.User(
