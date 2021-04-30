from bluepy.btle import Scanner, DefaultDelegate
import string

class ScanDelegate(DefaultDelegate):
	def __init__(self):
		DefaultDelegate.__init__(self)

	def handleDiscovery(self, dev,isNewDev, isNewData):
		if isNewDev:
			print("found a new device",dev.addr)
		elif isNewData:
			print('found new data from',dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
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

	output = 'addr: {}{}'.format(addr, name)
	print(output)
