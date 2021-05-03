import subprocess
import string
from bluepy.btle import Scanner

def run_sp(args):
    s = subprocess.check_output(args)
    return s


def ram():
    try:
        s = run_sp(["free","-m"])
    except:
        print("Error with subprocess in get_ram()")
        exit(1)
    
    lines = s.split('\n')
    ram = lines[1].split()
    total_ram = int(ram[1])
    available_ram = int(ram[6])
    return total_ram, available_ram


def processes():
    try:
        s = run_sp(["ps","-e"])
    except:
        print("Error with subprocess in get_num_processes")
        exit(1)

    return len(s.split("\n"))-1


def temp():
    try:
        s = run_sp(["vcgencmd","measure_temp"])
    except:
        print("Error with subprocess in get_temp()")
    c = float(s.split("=")[1].split("'")[0])
    f = (c*1.8)+32
    return f


def get_device_name(dev):
    for (sdtype, desc, value) in dev.getScanData():
        # remove non-printable characters from value
        value = filter(lambda x:x in string.printable, value)

        name = value if ('name' in desc.lower() and value) else ''
    	if name: break

    return name

def raspberry_model_serial():
    try:
        s = run_sp(["egrep", "Model.*:|Serial.*:", "/proc/cpuinfo"])
    except:
        print("Error with subprocess in raspberry_model_serial")
        exit(1)
        
    s = s.split('\n')
    serial = s[0].split(':')[1].strip()
    model = s[1].split(':')[1].strip()

    return model, serial


# get BLE devices in range
def ble():
    devices = Scanner().scan(4.0)
    msgs = []
    addrs = []
    for dev in devices:
        if dev.addr not in addrs:
            addrs.append(dev.addr)
            msg={'address':dev.addr}
            name = get_device_name(dev)
            # get device name if it has one
            if name:
                msg['name']=name

            msgs.append(msg)

        else:
            print('found duplicate addr')
            print(addrs)
            print(dev.addr)
    
    return msgs


if __name__ == "__main__" :
    tot, avail = ram()
    num_processes = processes()
    temp = temp()
    bles = ble()
    model, serial = raspberry_model_serial()

    print("current machine Model = '"+model+"'")
    print("Serial number = '"+serial+"'")
    print("total ram =",tot)
    print("available ram =",avail)
    print("number of current processes =",num_processes)
    print("temperature = {:.2f}'F".format(temp))
    print("BLE devices currently in range:")
    print("\tAddress\t\t\tName")
    for ble in bles:
        print("\t"+ble['address']+"\t"+ble.get('name',''))
