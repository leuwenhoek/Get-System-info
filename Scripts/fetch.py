import platform
import psutil
import json
import time
import os

# Global declarations
FILENAME = "data.json"
ABS_LOCATION = os.path.join("Scripts", "Data")
JSON_LOCATE = os.path.join(ABS_LOCATION, FILENAME)

def convertDATA(value, want_to="GB", roundof=2):
    try:
        if want_to == "GB":
            return round(value / (1024**3), roundof)
        elif want_to == "MB":
            return round(value / (1024**2), roundof)
        else:
            raise Exception("Invalid command")
    except:
        return 0

def getOS():
    try:
        os_dict = {
            "Machine name": platform.node(),
            "OS name": platform.system(),
            "OS release": platform.release(),
            "OS version": platform.version(),
            "Processor architecture": platform.architecture(),
            "Processor": platform.processor()
        }
        return os_dict
    except:
        return {}

def getCPU():
    try:
        logicalcpu_count = psutil.cpu_count()
        Physicalcpu_count = psutil.cpu_count(logical=False)
        threads_per_core = logicalcpu_count / Physicalcpu_count
        cpu_usage = psutil.cpu_percent(interval=1)

        data = {
            "Logical CPU": logicalcpu_count,
            "Physical CPU": Physicalcpu_count,
            "Threads per core": threads_per_core,
            "CPU usage": cpu_usage
        }
        return data
    except:
        return {}

def getMemory():
    try:
        memory = psutil.virtual_memory()
        memory_usage = convertDATA(memory.used)
        memory_percent = memory.percent
        memory_total = convertDATA(memory.total)
        memory_free = convertDATA(memory.free)

        physical_RAM = {
            "Total memory": memory_total,
            "Free memory": memory_free,
            "Consumed memory (%)": memory_percent,
            "Used-up memory": memory_usage
        }

        swap = psutil.swap_memory()
        swap_usage = convertDATA(swap.used)
        swap_percent = swap.percent
        swap_total = convertDATA(swap.total)
        swap_free = convertDATA(swap.free)

        Virtual_RAM = {
            "Total VRAM": swap_total,
            "Free VRAM": swap_free,
            "Consumed VRAM (%)": swap_percent,
            "Used-up VRAM": swap_usage
        }

        data = {
            "Actual RAM": physical_RAM,
            "Virtual RAM": Virtual_RAM
        }
        return data
    except:
        return {}

def getDisk():
    try:
        disk = psutil.disk_usage(give_MachineType())
        iodisk = psutil.disk_io_counters(perdisk=True)
        iodict = {}
        disk_dict = {}

        disk_total = convertDATA(disk.total)
        disk_used = convertDATA(disk.used)
        disk_free = convertDATA(disk.free)
        disk_percent = round(disk.percent, 2)

        disk_dict = {
            "Total space": disk_total,
            "Used space": disk_used,
            "Free space": disk_free,
            "Used percentage": disk_percent
        }

        i = 0
        for disk_name, stats in iodisk.items():
            i = i + 1
            read_count = stats.read_count
            write_count = stats.write_count
            write_size = convertDATA(stats.write_bytes)
            read_size = convertDATA(stats.read_bytes)
            iodict[f"Disk {i}"] = {
                "Disk name": disk_name,
                "Write count": write_count,
                "Read count": read_count,
                "Written size": write_size,
                "Readed size": read_size
            }

        data = {
            "Combined Disk": disk_dict,
            "Each Disk": iodict
        }
        return data
    except:
        return {}

def convertTIME(time, want_to="sec to hrs"):
    try:
        if want_to == "sec to hrs":
            result = time / 3600
            result = round(result, 4)
            if time > 24 or time <= 0:
                return False
            return result
        return "Invalid conversion"
    except:
        return False

def getBattery():
    try:
        battery = psutil.sensors_battery()
        battery_left = battery.percent

        On_charge = "No"
        if battery.power_plugged:
            On_charge = "Yes"

        Estimated_time = "Not available"
        if battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            Estimated_time = "Not available"
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            Estimated_time = "Infinite (charging)"
        else:
            if convertTIME(time=battery.secsleft) != False:
                Estimated_time = convertTIME(time=battery.secsleft)
            else:
                Estimated_time = "Unrealistic value given by the OS."

        data = {
            "Battery left": battery_left,
            "Is charging": On_charge,
            "Estimated Time left": Estimated_time
        }
        return data
    except:
        return {}

def getNetwork():
    try:
        network = psutil.net_io_counters(pernic=True)
        ActiveNet = {}
        NotinuseNet = {}
        i = 0
        y = 0

        for net_name, net in network.items():
            if net.bytes_recv != 0 or net.bytes_sent != 0:
                i = i + 1
                ActiveNet[f"Network name {i}"] = {
                    "Network name": net_name,
                    "Data downloaded": convertDATA(net.bytes_recv),
                    "Data uploaded": convertDATA(net.bytes_sent),
                    "Total packets uploaded": net.packets_sent,
                    "Total packets received": net.packets_recv
                }
            else:
                y = y + 1
                NotinuseNet[f"Network name {y}"] = {
                    "Network name": net_name
                }

        data = {
            "Active networks": ActiveNet,
            "Inactive networks": NotinuseNet
        }
        return data
    except:
        return {}

def getProcess():
    try:
        process = list(psutil.process_iter(['pid', 'name', 'memory_percent']))
        process_list = []

        for p in process:
            try:
                p.cpu_percent(interval=None)
            except:
                pass

        time.sleep(1)

        for task in process:
            try:
                cpu_percent = task.cpu_percent(interval=None) / psutil.cpu_count()
                process_list.append({
                    'id': None,
                    'pid': task.info['pid'],
                    'name': task.info['name'],
                    'cpu': round(cpu_percent, 4),
                    'memory': round(task.info['memory_percent'], 4)
                })
            except:
                pass

        sorted_list = sorted(process_list, key=lambda x: x['cpu'], reverse=True)
        top_list = sorted_list[:10]

        item = [i for i in range(1, len(top_list) + 1)]
        for d, new_id in zip(top_list, item):
            d['id'] = new_id

        data = {
            'top_processes': top_list
        }
        return data
    except:
        return {}

def submit_to_JSON():
    try:
        data = {
            "OS": getOS(),
            "CPU": getCPU(),
            "MEMORY": getMemory(),
            "DISK": getDisk(),
            "BATTERY": getBattery(),
            "NETWORK": getNetwork(),
            "PROCESS": getProcess()
        }
        return data
    except:
        return {}

def give_MachineType():
    try:
        if platform.system() == "Windows":
            return "C:\\"
        return "/"
    except:
        return "/"

def create_JSON():
    try:
        final_data = submit_to_JSON()
        if not os.path.exists(ABS_LOCATION):
            os.makedirs(ABS_LOCATION)

        with open(JSON_LOCATE, "w") as f:
            json.dump(final_data, f, indent=4)
        return 0
    except:
        return 1

def main():
    try:
        create_JSON()
        return 0
    except:
        return 1

if __name__ == "__main__":
    main()