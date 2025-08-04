import matplotlib.pyplot as plt
import pandas as pd
import os
import json
    
filename="data.json"
ABS_LOCATION = os.path.join("Scripts","Data")
JSON_LOCATE = os.path.join(ABS_LOCATION,filename)

def give_data(want="na"):
    data = loadData()
    return_data = None
    SubDisk_info = {}
    top_processes = {}
    if want == "na":
        return_data = 0

        # Actual memory info
    elif want == "Actual RAM":
        ActualMemory = data.get('MEMORY',{}).get('Actual RAM',{})
        return_data = ActualMemory

        # Virtual memory info
    elif want == "Virtual RAM":
        VirtualMemory = data.get('MEMORY',{}).get('Virtual RAM',{})
        return_data = VirtualMemory

        # Each Sub-Disk info
    elif want == "Each Disk":
        SubDisk_info
        SubDisk_info = data.get('DISK',{}).get('Each Disk',{})
        return_data = SubDisk_info

        # Each Sub-Disk write key info
    elif want == "Write count":
        SubDisk_info = data.get('DISK',{}).get('Each Disk',{})
        W_count = [w.get('Write count') for w in SubDisk_info.values()]
        return_data = W_count
    
        # Each Sub-Disk Read key info
    elif want == "Read count":
        SubDisk_info = data.get('DISK',{}).get('Each Disk',{})
        R_count = [w.get('Read count') for w in SubDisk_info.values()]
        return_data = R_count
    
        # top process info
    elif want == "process":
        top_processes = data.get('PROCESS',{}).get('top_processes',{})
        return_data = top_processes

        # CPU process info
    elif want == "cpu-process":
        top_processes = data.get('PROCESS',{}).get('top_processes',{})
        CPU_usage = {proc.get('name'): proc.get('cpu', 0) for proc in top_processes}
        return_data = CPU_usage

        # Memory process info
    elif want == "memory-process":
        top_processes = data.get('PROCESS',{}).get('top_processes',{})
        Memory_usage = {memory.get('name'): memory.get('memory',0) for memory in top_processes}
        return_data = Memory_usage

    else:
        raise SyntaxError("INVALID command")
    return return_data 

def loadData():
    data = None
    with open(JSON_LOCATE,"r") as f:
        data
        data = json.load(f)
        return data


def main():
    ARAM = give_data("Actual RAM")
    VRAM = give_data("Virtual RAM")
    Each_Disk = give_data("Each Disk")
    Write_count = give_data("Write count")
    Read_count = give_data("Read count")
    Process = give_data("process")
    CPU_process = give_data("cpu-process")
    Memory_process = give_data("memory-process")

    
    return 0

if __name__ == "__main__":
    main()