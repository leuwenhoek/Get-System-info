import platform
import psutil
import json
import os

#Global declarations
filename="data.json"
ABS_LOCATION = os.path.join("Scripts","Data")
JSON_LOCATE = os.path.join(ABS_LOCATION,filename)

def convertDATA(value,want_to="GB",roundof=2):
    if want_to == "GB":
        return round(value/(1024**3),roundof)
    else:
        raise("Invalid command")

def getOS():
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    machine_name = platform.node()
    architecture = platform.architecture()
    processor = platform.processor()

    os_dict = {
            "Machine name" : machine_name,
            "OS name" : os_name,
            "OS release" : os_release,
            "OS version" : os_version,
            "Processor architecture" : architecture,
            "Processor" : processor
        }

    return os_dict

def getCPU():
    logicalcpu_count = psutil.cpu_count()
    Physicalcpu_count = psutil.cpu_count(logical=False)
    threads_per_core = logicalcpu_count/Physicalcpu_count
    cpu_usage = psutil.cpu_percent(interval=1)

    data = {
        "Logical CPU" : logicalcpu_count,
        "Physical CPU" : Physicalcpu_count,
        "Threads per core" : threads_per_core,
        "CPU usage" : cpu_usage # In 1 sec
    }

    return data


def getMemory():
    # Physical RAM data
    memory = psutil.virtual_memory()
    memory_usage = convertDATA(memory.used)
    memory_percent = memory.percent
    memory_total = convertDATA(memory.total)
    memory_free = convertDATA(memory.free)

    physical_RAM = {
        "Total memory" : memory_total,
        "Free memory" : memory_free,
        "Consumed memory (%)" : memory_percent,
        "Used-up memory" : memory_usage
    }

    #temporary RAM in DISK
    swap = psutil.swap_memory()
    swap_usage = convertDATA(swap.used)
    swap_percent = swap.percent
    swap_total = convertDATA(swap.total)
    swap_free = convertDATA(swap.free)

    Virtual_RAM = {
        "Total VRAM" : swap_total,
        "Free VRAM" : swap_free,
        "Consumed VRAM (%)" : swap_percent,
        "Used-up VRAM" : swap_usage
    }

    data = {
        "Actual RAM" : physical_RAM,
        "Virtual RAM" : Virtual_RAM,
        
    }

    return data

def getDisk():
    i = 0
    disk = psutil.disk_usage(give_MachineType())
    iodisk = psutil.disk_io_counters(perdisk=True)
    iodict = {}
    disk_dict = {}

    disk_total = convertDATA(disk.total)
    disk_used = convertDATA(disk.used)
    disk_free = convertDATA(disk.free)
    disk_percent = round(disk.percent,2)

    disk_dict = {
        "Total space" : disk_total,
        "Used space" : disk_used,
        "Free space" : disk_free,
        "Used percentage" : disk_percent
    }

    for disk_,stats in iodisk.items():

        i=i+1
        iodisk_name = disk_
        read_count = stats.read_count
        write_count = stats.write_count
        write_size = convertDATA(stats.write_bytes)
        read_size = convertDATA(stats.read_bytes)
        iodict = {
            f"Disk {i}": {
                "Disk name" : iodisk_name,
                "Write count" : write_count,
                "Read count" : read_count,
                "Written size" : write_size,
                "Readed size" : read_size,
            }
        }
    
    data = {
        "Combined Disk" : disk_dict,
        "Each Disk" : iodict
    }

    return data

def convertTIME(time,want_to="sec to hrs"):
    result = None

    def isValid():
        if time > 24 or time <= 0:
            return False
        else:
            return True
        
    if want_to == "sec to hrs":
        result = time/3600
        result = round(result,4)
        if isValid:
            return result
        else:
            return False
    return "fcked up"

def getBattery():
    battery = psutil.sensors_battery()
    battery_left = battery.percent

    On_charge = None
    if battery.power_plugged:
        On_charge
        On_charge = "Yes"    
    else:
        On_charge = "No"    
    
    Estimated_time = None
    if battery.secsleft == psutil.POWER_TIME_UNKNOWN:
        Estimated_time
        Estimated_time = "Not available"
    elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
        Estimated_time = "Infinite (charging)"
    
    else:
        if convertTIME(time=battery.secsleft) != True:
            Estimated_time = "Unrealistic value given by the OS."
        else:
            Estimated_time = convertTIME(time=battery.secsleft)

    data ={
        "Battery left" : battery_left,
        "Is charging" : On_charge,
        "Estimated Time left" : Estimated_time
    }

    return data

def submit_to_JSON():
    OS = getOS()
    CPU = getCPU()
    MEMORY = getMemory()
    DISK = getDisk()
    BATTERY = getBattery()
    data = {
        "OS":OS,
        "CPU" : CPU,
        "MEMORY" : MEMORY,
        "DISK" : DISK,
        "BATTERY" : BATTERY
        }
    
    return data


def give_MachineType():
    locate = None
    if platform.system() == "Windows":
        locate = "C:\\"
    else:
        locate = "/"
    return locate


def create_JSON():  

    final_data = submit_to_JSON()
    if not os.path.exists(ABS_LOCATION):
        os.makedirs(ABS_LOCATION)
    else:
        pass

    with open(JSON_LOCATE,"w") as f:
        json.dump(final_data,f,indent=4)
    return 0

def main():
    create_JSON()
    return 0

if __name__ == "__main__":
    main()