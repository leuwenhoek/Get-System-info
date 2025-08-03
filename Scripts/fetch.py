import platform
import psutil
import json
import os

#Global declarations
filename="data.json"
ABS_LOCATION = os.path.join("Scripts","Data")
JSON_LOCATE = os.path.join(ABS_LOCATION,filename)

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

def convertDATA(value,want_to="GB",roundof=2):
    if want_to == "GB":
        return round(value/(1024**3),roundof)
    else:
        raise("Invalid command")

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

def submit_to_JSON():
    OS = getOS()
    CPU = getCPU()
    MEMORY = getMemory()
    data = {
        "OS":OS,
        "CPU" : CPU,
        "MEMORY" : MEMORY,
        }
    return data

def create_JSON():  

    data = submit_to_JSON()
    if not os.path.exists(ABS_LOCATION):
        os.makedirs(ABS_LOCATION)
    else:
        pass

    with open(JSON_LOCATE,"w") as f:
        json.dump(data,f,indent=4)
    return 0

def main():
    return 0

if __name__ == "__main__":
    create_JSON()
    main()