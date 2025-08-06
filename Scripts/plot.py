import matplotlib.pyplot as plt
import os
import json
import pandas as pd

# Global declarations
filename = "data.json"
ABS_LOCATION = os.path.join("Scripts", "Data")
JSON_LOCATE = os.path.join(ABS_LOCATION, filename)

def loadData():
    try:
        with open(JSON_LOCATE, "r") as f:
            data = json.load(f)
            return data
    except:
        return {}

def give_data(want="na"):
    try:
        data = loadData()
        return_data = None
        SubDisk_info = {}
        top_processes = {}

        if want == "na":
            return_data = 0
        elif want == "Actual RAM":
            return_data = data.get('MEMORY', {}).get('Actual RAM', {})
        elif want == "Virtual RAM":
            return_data = data.get('MEMORY', {}).get('Virtual RAM', {})
        elif want == "Each Disk":
            SubDisk_info = data.get('DISK', {}).get('Each Disk', {})
            return_data = SubDisk_info
        elif want == "Write count":
            SubDisk_info = data.get('DISK', {}).get('Each Disk', {})
            W_count = [w.get('Write count', 0) for w in SubDisk_info.values()]
            return_data = W_count
        elif want == "Read count":
            SubDisk_info = data.get('DISK', {}).get('Each Disk', {})
            R_count = [w.get('Read count', 0) for w in SubDisk_info.values()]
            return_data = R_count
        elif want == "process":
            top_processes = data.get('PROCESS', {}).get('top_processes', {})
            return_data = top_processes
        elif want == "cpu-process":
            top_processes = data.get('PROCESS', {}).get('top_processes', {})
            CPU_usage = {proc.get('id', 0): {proc.get('name', 'Unknown'): proc.get('cpu', 0)} for proc in top_processes}
            return_data = CPU_usage
        elif want == "memory-process":
            top_processes = data.get('PROCESS', {}).get('top_processes', {})
            Memory_usage = {memory.get('id', 0): {memory.get('name', 'Unknown'): memory.get('memory', 0)} for memory in top_processes}
            return_data = Memory_usage
        else:
            raise Exception("INVALID command")
        return return_data
    except:
        return None

def saveimage(name):
    try:
        LOCATION_IMG_DIR = os.path.join("Scripts", "IMAGE")
        IMG_IN = os.path.join("Scripts", "IMAGE", name)

        if not os.path.exists(LOCATION_IMG_DIR):
            os.makedirs(LOCATION_IMG_DIR)

        plt.savefig(IMG_IN, dpi=300, bbox_inches='tight')
        return 0
    except:
        return 1

def plotMemory():
    try:
        ARAM = give_data("Actual RAM")
        VRAM = give_data("Virtual RAM")

        if not ARAM or not VRAM:
            return 1

        total_space = [ARAM.get('Total memory', 0), VRAM.get('Total VRAM', 0)]
        free_space = [ARAM.get('Free memory', 0), VRAM.get('Free VRAM', 0)]
        consumed_space = [ARAM.get('Consumed memory (%)', 0), VRAM.get('Consumed VRAM (%)', 0)]
        used_space = [ARAM.get('Used-up memory', 0), VRAM.get('Used-up VRAM', 0)]

        df = pd.DataFrame({
            'Name': ["Actual RAM", "Virtual RAM"],
            'Total space': [total_space[0], total_space[1]],
            'free space': [free_space[0], free_space[1]],
            'consumed space': [consumed_space[0], consumed_space[1]],
            'used space': [used_space[0], used_space[1]]
        })

        ax = df.plot(x='Name', y=['Total space', 'free space', 'used space'], kind="bar")
        ax.set_axisbelow(True)
        plt.grid(True, which='both', axis='y', linestyle='-', linewidth=0.7, color='gray', zorder=0)
        plt.ylabel('Stats')
        plt.title("Memory info graph")

        for container in ax.containers:
            labels = [f'{float(value)} GB' for value in container.datavalues]
            ax.bar_label(container, labels=labels, label_type='center', color='black', fontsize=9)

        saveimage("MemoryInformation.png")
        return 0
    except:
        return 1

def plotCpuProcess():
    try:
        cpu_process = give_data("cpu-process")
        if not cpu_process:
            return 1

        cpu_name = []
        cpu_usage = []

        for key, values in cpu_process.items():
            for name, cpu in values.items():
                cpu_name.append(name)
                cpu_usage.append(cpu)

        if len(cpu_name) < 10 or len(cpu_usage) < 10:
            return 1

        df = pd.DataFrame({
            'Name': cpu_name[:10],
            'CPU': cpu_usage[:10]
        })

        cpu = df['CPU']
        labels = df['Name']
        legend_labels = [f"{name} ({size}%)" for name, size in zip(labels, cpu)]

        plt.figure(figsize=(8, 8))
        patches, texts = plt.pie(
            cpu,
            startangle=140,
            textprops={'fontsize': 9}
        )

        plt.legend(patches, labels=legend_labels, loc='best', fontsize=9)
        plt.axis('equal')
        plt.title('CPU Usage by Process')
        saveimage("CpuProcessInfo.png")
        return 0
    except:
        return 1

def plotMemoryProcess():
    try:
        memory_process = give_data("memory-process")
        if not memory_process:
            return 1

        memory_percentage = []
        process_name = []

        for id, package in memory_process.items():
            for name, memory in package.items():
                process_name.append(name)
                memory_percentage.append(memory)

        if len(process_name) < 10 or len(memory_percentage) < 10:
            return 1

        df = pd.DataFrame({
            'Name': process_name[:10],
            'Memory in use': memory_percentage[:10]
        })

        memory = df['Memory in use']
        labels = df['Name']
        legend_labels = [f"{name} ({size}%)" for name, size in zip(labels, memory)]

        plt.figure(figsize=(8, 8))
        patches, texts = plt.pie(
            memory,
            startangle=140,
            textprops={'fontsize': 9}
        )

        plt.legend(patches, labels=legend_labels, loc='best', fontsize=9)
        plt.axis('equal')
        plt.title('Memory Usage by top 10 programs(according to CPU usage)')
        saveimage("MemoryProcessInfo.png")
        return 0
    except:
        return 1

def main():
    try:
        plotMemory()
        plotCpuProcess()
        plotMemoryProcess()
        return 0
    except:
        return 1

if __name__ == "__main__":
    main()