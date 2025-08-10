import platform
import psutil
import json
import time
import os

# Global declarations
FILENAME = "db.json"
ABS_LOCATION = os.path.join("main","Scripts", "Data")
JSON_LOCATE = os.path.join(ABS_LOCATION, FILENAME)

def convertDATA(value, want_to="GB", roundof=2):
    try:
        if value is None or not isinstance(value, (int, float)) or value < 0:
            return "unable to access"
        if want_to == "GB":
            return round(value / (1024**3), roundof)
        elif want_to == "MB":
            return round(value / (1024**2), roundof)
        else:
            raise Exception("Invalid command")
    except:
        return "unable to access"

def getOS():
    try:
        os_dict = {
            "Machine name": platform.node() if platform.node() else "unable to access",
            "OS name": platform.system() if platform.system() else "unable to access",
            "OS release": platform.release() if platform.release() else "unable to access",
            "OS version": platform.version() if platform.version() else "unable to access",
            "Processor architecture": platform.architecture() if platform.architecture() else ("unable to access", "unable to access"),
            "Processor": platform.processor() if platform.processor() else "unable to access"
        }
        return os_dict
    except:
        return {
            "Machine name": "unable to access",
            "OS name": "unable to access",
            "OS release": "unable to access",
            "OS version": "unable to access",
            "Processor architecture": ("unable to access", "unable to access"),
            "Processor": "unable to access"
        }

def getCPU():
    try:
        logicalcpu_count = psutil.cpu_count()
        Physicalcpu_count = psutil.cpu_count(logical=False)
        threads_per_core = logicalcpu_count / Physicalcpu_count if Physicalcpu_count else "unable to access"
        cpu_usage = psutil.cpu_percent(interval=1)

        data = {
            "Logical CPU": logicalcpu_count if logicalcpu_count is not None else "unable to access",
            "Physical CPU": Physicalcpu_count if Physicalcpu_count is not None else "unable to access",
            "Threads per core": threads_per_core if threads_per_core != "unable to access" else "unable to access",
            "CPU usage": cpu_usage if cpu_usage is not None else "unable to access"
        }
        return data
    except:
        return {
            "Logical CPU": "unable to access",
            "Physical CPU": "unable to access",
            "Threads per core": "unable to access",
            "CPU usage": "unable to access"
        }

def getMemory():
    try:
        memory = psutil.virtual_memory()
        memory_usage = convertDATA(memory.used) if memory.used is not None else "unable to access"
        memory_percent = memory.percent if memory.percent is not None else "unable to access"
        memory_total = convertDATA(memory.total) if memory.total is not None else "unable to access"
        memory_free = convertDATA(memory.free) if memory.free is not None else "unable to access"

        physical_RAM = {
            "Total memory": memory_total,
            "Free memory": memory_free,
            "Consumed memory (%)": memory_percent,
            "Used-up memory": memory_usage
        }

        swap = psutil.swap_memory()
        swap_usage = convertDATA(swap.used) if swap.used is not None else "unable to access"
        swap_percent = swap.percent if swap.percent is not None else "unable to access"
        swap_total = convertDATA(swap.total) if swap.total is not None else "unable to access"
        swap_free = convertDATA(swap.free) if swap.free is not None else "unable to access"

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
        return {
            "Actual RAM": {
                "Total memory": "unable to access",
                "Free memory": "unable to access",
                "Consumed memory (%)": "unable to access",
                "Used-up memory": "unable to access"
            },
            "Virtual RAM": {
                "Total VRAM": "unable to access",
                "Free VRAM": "unable to access",
                "Consumed VRAM (%)": "unable to access",
                "Used-up VRAM": "unable to access"
            }
        }

def getDisk():
    try:
        disk = psutil.disk_usage(give_MachineType())
        iodisk = psutil.disk_io_counters(perdisk=True) or {}
        disk_dict = {}

        disk_total = convertDATA(disk.total) if disk.total is not None else "unable to access"
        disk_used = convertDATA(disk.used) if disk.used is not None else "unable to access"
        disk_free = convertDATA(disk.free) if disk.free is not None else "unable to access"
        disk_percent = round(disk.percent, 2) if disk.percent is not None else "unable to access"

        disk_dict = {
            "Total space": disk_total,
            "Used space": disk_used,
            "Free space": disk_free,
            "Used percentage": disk_percent
        }

        i = 0
        iodict = {}
        for disk_name, stats in iodisk.items():
            i = i + 1
            read_count = stats.read_count if stats.read_count is not None else "unable to access"
            write_count = stats.write_count if stats.write_count is not None else "unable to access"
            write_size = convertDATA(stats.write_bytes) if stats.write_bytes is not None else "unable to access"
            read_size = convertDATA(stats.read_bytes) if stats.read_bytes is not None else "unable to access"
            iodict[f"Disk {i}"] = {
                "Disk name": disk_name if disk_name else "unable to access",
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
        return {
            "Combined Disk": {
                "Total space": "unable to access",
                "Used space": "unable to access",
                "Free space": "unable to access",
                "Used percentage": "unable to access"
            },
            "Each Disk": {}
        }

def convertTIME(time, want_to="sec to hrs"):
    try:
        if time is None or time <= 0:
            return "unable to access"
        if want_to == "sec to hrs":
            result = time / 3600
            result = round(result, 4)
            if result > 24:
                return "unable to access"
            return result
        return "unable to access"
    except:
        return "unable to access"

def getBattery():
    try:
        battery = psutil.sensors_battery()
        if not battery:
            return {
                "Battery left": "unable to access",
                "Is charging": "unable to access",
                "Estimated Time left": "unable to access"
            }

        battery_left = battery.percent if battery.percent is not None else "unable to access"
        On_charge = "Yes" if battery.power_plugged else "No"
        Estimated_time = "Not available"

        if battery.secsleft == psutil.POWER_TIME_UNKNOWN:
            Estimated_time = "Not available"
        elif battery.secsleft == psutil.POWER_TIME_UNLIMITED:
            Estimated_time = "Infinite (charging)"
        else:
            converted_time = convertTIME(battery.secsleft)
            Estimated_time = converted_time if converted_time != "unable to access" else "Unrealistic value given by the OS."

        data = {
            "Battery left": battery_left,
            "Is charging": On_charge,
            "Estimated Time left": Estimated_time
        }
        return data
    except:
        return {
            "Battery left": "unable to access",
            "Is charging": "unable to access",
            "Estimated Time left": "unable to access"
        }

def getNetwork():
    try:
        network = psutil.net_io_counters(pernic=True) or {}
        ActiveNet = {}
        NotinuseNet = {}
        i = 0
        y = 0

        for net_name, net in network.items():
            if net.bytes_recv != 0 or net.bytes_sent != 0:
                i = i + 1
                ActiveNet[f"Network name {i}"] = {
                    "Network name": net_name if net_name else "unable to access",
                    "Data downloaded": convertDATA(net.bytes_recv) if net.bytes_recv is not None else "unable to access",
                    "Data uploaded": convertDATA(net.bytes_sent) if net.bytes_sent is not None else "unable to access",
                    "Total packets uploaded": net.packets_sent if net.packets_sent is not None else "unable to access",
                    "Total packets received": net.packets_recv if net.packets_recv is not None else "unable to access"
                }
            else:
                y = y + 1
                NotinuseNet[f"Network name {y}"] = {
                    "Network name": net_name if net_name else "unable to access"
                }

        data = {
            "Active networks": ActiveNet,
            "Inactive networks": NotinuseNet
        }
        return data
    except:
        return {
            "Active networks": {},
            "Inactive networks": {}
        }

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
                cpu_percent = task.cpu_percent(interval=None) / (psutil.cpu_count() or 1)
                process_list.append({
                    'id': None,
                    'pid': task.info['pid'] if task.info['pid'] is not None else "unable to access",
                    'name': task.info['name'] if task.info['name'] else "unable to access",
                    'cpu': round(cpu_percent, 4) if cpu_percent is not None else "unable to access",
                    'memory': round(task.info['memory_percent'], 4) if task.info['memory_percent'] is not None else "unable to access"
                })
            except:
                pass

        sorted_list = sorted(process_list, key=lambda x: x['cpu'] if x['cpu'] != "unable to access" else 0, reverse=True)
        top_list = sorted_list[:10]

        item = [i for i in range(1, len(top_list) + 1)]
        for d, new_id in zip(top_list, item):
            d['id'] = new_id

        data = {
            'top_processes': top_list
        }
        return data
    except:
        return {'top_processes': []}

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