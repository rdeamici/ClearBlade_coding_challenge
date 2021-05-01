import string
import json
from time import sleep
import sysInfo

from bluepy.btle import Scanner, DefaultDelegate
from clearblade.ClearBladeCore import System,Query, Developer

def create_msgs():
    total, available = sysInfo.ram()
    processes = sysInfo.processes()
    temp = sysInfo.temp()
    bles = sysInfo.ble()
    num_bles = len(bles)
    system_overview =  {
        'total ram': total,
        'available ram': available,
        'number of running processes':processes,
        'Device Temperature': temp,
        'Number of Bluetooth Devices in Range': num_bles
    }
    bluetooth_devices = []
    for ble in bles:
        msg = {
            'address': ble['addr']
        }

        if 'name' in ble:
            msg['name'] = ble['name']

        bluetooth_devices.append(msg)

    return system_overview, bluetooth_devices

#send message to Broker
SystemKey = 'c4dfbc880ce891a09fe8eb92eb9d01'
SystemSecret = 'C4DFBC880CC0D8A8B5FCE5B4DB44'
admin_email = 'rtdeamicis@gmail.com'
admin_pw = 'H1r3m3pls'

mySystem = System(SystemKey, SystemSecret)
admin = mySystem.User(admin_email, admin_pw)

mqtt = mySystem.Messaging(admin)
sys_overview, bles = create_msgs()

mqtt.connect()

for ble in bles:
    print(json.dumps(ble)) # debug print statement
    mqtt.publish('ble/_platform',json.dumps(ble))
    sleep(1)

mqtt.publish('sysinfo',json.dumps(sys_overview))

mqtt.disconnect()

