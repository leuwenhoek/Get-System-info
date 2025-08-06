import matplotlib.pyplot as plt
import os
import json
import pandas as pd
    
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
        CPU_usage = {proc.get('id'):{proc.get('name'): proc.get('cpu', 0)} for proc in top_processes}
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


def saveimage(name):
    LOCATION_IMG_DIR = os.path.join("Scripts","IMAGE")
    IMG_IN = os.path.join("Scripts","IMAGE",name)

    if not os.path.exists(LOCATION_IMG_DIR):
        os.makedirs(LOCATION_IMG_DIR)
    else:
        pass

    plt.savefig(IMG_IN,dpi=300,bbox_inches='tight')
    return

def plotMemory():
    ARAM = give_data("Actual RAM")
    VRAM = give_data("Virtual RAM")

    #list form (Actaul RAM info, Virtual RAM info)

    total_space = [ARAM['Total memory'],VRAM['Total VRAM']]
    free_space = [ARAM['Free memory'],VRAM['Free VRAM']]
    consumed_space = [ARAM['Consumed memory (%)'],VRAM['Consumed VRAM (%)']]
    used_space = [ARAM['Used-up memory'],VRAM['Used-up VRAM']]


    df = pd.DataFrame({
        'Name' : ["Actual RAM","Virtual RAM"],
        'Total space' : [total_space[0],total_space[1]],
        'free space' : [free_space[0],free_space[1]],
        'consumed space' : [consumed_space[0],consumed_space[1]],
        'used space' : [used_space[0],used_space[1]]
        
    })

    ax = df.plot(x='Name',y=['Total space','free space','used space'],kind="bar")
    ax.set_axisbelow(True)
    plt.grid(True, which='both', axis='y', linestyle='-', linewidth=0.7, color='gray', zorder=0)
    plt.ylabel('Stats')
    plt.title("Memory info graph")

    for container in ax.containers:
        labels = [f'{float(value)} GB' for value in container.datavalues]
        ax.bar_label(container, labels=labels, label_type='center', color='black', fontsize=9)

    saveimage("MemoryInformation.png")

def plotProcess():
    cpu_process = [give_data("cpu-process")]
    cpu_name = []
    cpu_usage =[]
    
    for each_process in cpu_process:
        for key,values in each_process.items():
            for name,cpu in values.items():
                cpu_name.append(name)
                cpu_usage.append(cpu)

    df = pd.DataFrame({
        'Name' : [cpu_name[0],cpu_name[1], cpu_name[2], cpu_name[3], cpu_name[4], cpu_name[5], cpu_name[6], cpu_name[7], cpu_name[8],cpu_name[9]],
        'CPU' : [cpu_usage[0],cpu_usage[1],cpu_usage[2],cpu_usage[3],cpu_usage[4],cpu_usage[5],cpu_usage[6],cpu_usage[7],cpu_usage[8],cpu_usage[9]]
    })

    cpu = df[f'CPU']
    labels = df['Name']
    legend_labels = [f"{name} ({size}%)" for name, size in zip(labels, cpu)]

    plt.figure(figsize=(8, 8))
    patches, texts = plt.pie(
        cpu, 
        startangle=140,
        textprops={'fontsize': 9}  # size of the percentage text
    )

    plt.legend(patches, labels=legend_labels, loc='best', fontsize=9)  # Create legend using pie slices

    plt.axis('equal')  # Equal aspect ratio to make the pie circular
    plt.title('CPU Usage by Process')
    saveimage("ProcessInfo.png")


def main():
    return 0

if __name__ == "__main__":
    main()