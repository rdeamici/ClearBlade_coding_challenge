import json
from time import sleep
import sysInfo

from clearblade.ClearBladeCore import System

# creates and returns two variables to hold messages 
# to be published to ClearBlade platform
def create_msgs():
    total, available = sysInfo.ram()
    num_processes = sysInfo.processes()
    temp = sysInfo.temp()
    bles = sysInfo.ble()
    model, serial = sysInfo.raspberry_model_serial()
    num_bles = len(bles)
    
    system_overview =  {
        'total_ram': total,
        'available_ram': available,
        'number_of_running_processes':num_processes,
        'device_temperature': temp,
        'number_ble_in_range': num_bles,
        "raspberry_model":model,
        "raspberry_serial_num":serial
    }
    
    bluetooth_devices = []
    for ble in bles:
        msg = {
            'address': ble['address']
        }

        if 'name' in ble:
            msg['name'] = ble['name']

        bluetooth_devices.append(msg)

    return system_overview, bluetooth_devices


def main():
    #send message to ClearBlade platform
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

if __name__ == "__main__":
    main()
