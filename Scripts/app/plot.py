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
            W_count = [w.get('Write count', "unable to access") for w in SubDisk_info.values()]
            return_data = W_count
        elif want == "Read count":
            SubDisk_info = data.get('DISK', {}).get('Each Disk', {})
            R_count = [w.get('Read count', "unable to access") for w in SubDisk_info.values()]
            return_data = R_count
        elif want == "process":
            top_processes = data.get('PROCESS', {}).get('top_processes', {})
            return_data = top_processes
        elif want == "cpu-process":
            top_processes = data.get('PROCESS', {}).get('top_processes', {})
            CPU_usage = {proc.get('id', 0): {proc.get('name', 'Unknown'): proc.get('cpu', "unable to access")} for proc in top_processes}
            return_data = CPU_usage
        elif want == "memory-process":
            top_processes = data.get('PROCESS', {}).get('top_processes', {})
            Memory_usage = {memory.get('id', 0): {memory.get('name', 'Unknown'): memory.get('memory', "unable to access")} for memory in top_processes}
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

def plotCpuProcess():
    try:
        cpu_process = give_data("cpu-process")
        if not cpu_process:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("CpuProcessInfo.png")
            return 1

        cpu_name = []
        cpu_usage = []
        
        # Only collect processes with actual usage > 0
        for key, values in cpu_process.items():
            for name, cpu in values.items():
                if cpu != "unable to access" and cpu > 0:
                    cpu_name.append(name)
                    cpu_usage.append(cpu)

        # Check if we have any valid data
        if len(cpu_name) == 0:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, "No valid CPU usage data available", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("CpuProcessInfo.png")
            return 1

        # Sort by usage (descending) and take top 10
        data_pairs = list(zip(cpu_name, cpu_usage))
        data_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 10 or all available data if less than 10
        top_data = data_pairs[:min(10, len(data_pairs))]
        cpu_name_filtered = [item[0] for item in top_data]
        cpu_usage_filtered = [item[1] for item in top_data]
        
        # Generate colors for each slice
        colors = plt.cm.Set3(range(len(cpu_name_filtered)))

        plt.figure(figsize=(10, 8))
        
        # Create pie chart with only valid data
        wedges, texts, autotexts = plt.pie(
            cpu_usage_filtered,
            autopct='%1.2f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9}
        )
        
        # Improve text visibility
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
        
        # Create legend with process names and percentages
        legend_labels = [f"{name} ({usage:.2f}%)" for name, usage in zip(cpu_name_filtered, cpu_usage_filtered)]
        plt.legend(wedges, legend_labels, title="Processes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
        
        plt.title('CPU Usage by Process', fontsize=14, fontweight='bold')
        plt.axis('equal')
        saveimage("CpuProcessInfo.png")
        return 0
        
    except Exception as e:
        plt.figure(figsize=(8, 8))
        plt.text(0.5, 0.5, f"Error generating CPU process chart: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=12, color='red')
        plt.axis('off')
        saveimage("CpuProcessInfo.png")
        return 1

def plotMemoryProcess():
    try:
        memory_process = give_data("memory-process")
        if not memory_process:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryProcessInfo.png")
            return 1

        memory_percentage = []
        process_name = []
        
        # Only collect processes with actual memory usage > 0
        for id, package in memory_process.items():
            for name, memory in package.items():
                if memory != "unable to access" and memory > 0:
                    process_name.append(name)
                    memory_percentage.append(memory)

        # Check if we have any valid data
        if len(process_name) == 0:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, "No valid memory usage data available", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryProcessInfo.png")
            return 1

        # Sort by memory usage (descending) and take top 10
        data_pairs = list(zip(process_name, memory_percentage))
        data_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 10 or all available data if less than 10
        top_data = data_pairs[:min(10, len(data_pairs))]
        process_name_filtered = [item[0] for item in top_data]
        memory_percentage_filtered = [item[1] for item in top_data]
        
        # Generate colors for each slice
        colors = plt.cm.Set2(range(len(process_name_filtered)))

        plt.figure(figsize=(10, 8))
        
        # Create pie chart with only valid data
        wedges, texts, autotexts = plt.pie(
            memory_percentage_filtered,
            autopct='%1.3f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9}
        )
        
        # Improve text visibility
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
        
        # Create legend with process names and percentages
        legend_labels = [f"{name} ({memory:.3f}%)" for name, memory in zip(process_name_filtered, memory_percentage_filtered)]
        plt.legend(wedges, legend_labels, title="Processes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
        
        plt.title('Memory Usage by Top Programs', fontsize=14, fontweight='bold')
        plt.axis('equal')
        saveimage("MemoryProcessInfo.png")
        return 0
        
    except Exception as e:
        plt.figure(figsize=(8, 8))
        plt.text(0.5, 0.5, f"Error generating memory process chart: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=12, color='red')
        plt.axis('off')
        saveimage("MemoryProcessInfo.png")
        return 1

def plotMemory():
    try:
        ARAM = give_data("Actual RAM")
        VRAM = give_data("Virtual RAM")

        if not ARAM or not VRAM:
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryInformation.png")
            return 1

        # Check if any critical data is "unable to access"
        total_space = [ARAM.get('Total memory', "unable to access"), VRAM.get('Total VRAM', "unable to access")]
        free_space = [ARAM.get('Free memory', "unable to access"), VRAM.get('Free VRAM', "unable to access")]
        used_space = [ARAM.get('Used-up memory', "unable to access"), VRAM.get('Used-up VRAM', "unable to access")]

        if any(x == "unable to access" for x in total_space + free_space + used_space):
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryInformation.png")
            return 1

        # Convert to numeric values, handling any potential string values
        try:
            total_space = [float(x) if x != "unable to access" else 0 for x in total_space]
            free_space = [float(x) if x != "unable to access" else 0 for x in free_space]
            used_space = [float(x) if x != "unable to access" else 0 for x in used_space]
        except (ValueError, TypeError):
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "Invalid data format in memory information", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryInformation.png")
            return 1

        df = pd.DataFrame({
            'Memory Type': ["Actual RAM", "Virtual RAM"],
            'Total Space (GB)': total_space,
            'Free Space (GB)': free_space,
            'Used Space (GB)': used_space
        })

        # Create a more visually appealing bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(df['Memory Type']))
        width = 0.25
        
        bars1 = ax.bar([i - width for i in x], df['Total Space (GB)'], width, 
                      label='Total Space', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x, df['Free Space (GB)'], width, 
                      label='Free Space', color='#2ecc71', alpha=0.8)
        bars3 = ax.bar([i + width for i in x], df['Used Space (GB)'], width, 
                      label='Used Space', color='#e74c3c', alpha=0.8)

        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{height:.1f} GB', ha='center', va='bottom', fontsize=9)

        ax.set_xlabel('Memory Type', fontweight='bold')
        ax.set_ylabel('Space (GB)', fontweight='bold')
        ax.set_title('Memory Information Overview', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Memory Type'])
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        saveimage("MemoryInformation.png")
        return 0
        
    except Exception as e:
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Error generating memory chart: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=12, color='red')
        plt.axis('off')
        saveimage("MemoryInformation.png")
        return 1
        
    except Exception as e:
        plt.figure(figsize=(8, 8))
        plt.text(0.5, 0.5, f"Error generating CPU process chart: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=12, color='red')
        plt.axis('off')
        saveimage("CpuProcessInfo.png")
        return 1


def plotMemoryProcess():
    try:
        memory_process = give_data("memory-process")
        if not memory_process:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryProcessInfo.png")
            return 1

        memory_percentage = []
        process_name = []
        
        # Only collect processes with actual memory usage > 0
        for id, package in memory_process.items():
            for name, memory in package.items():
                if memory != "unable to access" and memory > 0:
                    process_name.append(name)
                    memory_percentage.append(memory)

        # Check if we have any valid data
        if len(process_name) == 0:
            plt.figure(figsize=(8, 8))
            plt.text(0.5, 0.5, "No valid memory usage data available", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryProcessInfo.png")
            return 1

        # Sort by memory usage (descending) and take top 10
        data_pairs = list(zip(process_name, memory_percentage))
        data_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 10 or all available data if less than 10
        top_data = data_pairs[:min(10, len(data_pairs))]
        process_name_filtered = [item[0] for item in top_data]
        memory_percentage_filtered = [item[1] for item in top_data]
        
        # Generate colors for each slice
        colors = plt.cm.Set2(range(len(process_name_filtered)))

        plt.figure(figsize=(10, 8))
        
        # Create pie chart with only valid data
        wedges, texts, autotexts = plt.pie(
            memory_percentage_filtered,
            autopct='%1.3f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 9}
        )
        
        # Improve text visibility
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
        
        # Create legend with process names and percentages (matching original format)
        legend_labels = [f"{name} ({memory:.4f}%)" for name, memory in zip(process_name_filtered, memory_percentage_filtered)]
        plt.legend(wedges, legend_labels, title="Processes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
        
        plt.title('Memory Usage by Top Programs', fontsize=14, fontweight='bold')
        plt.axis('equal')
        saveimage("MemoryProcessInfo.png")
        return 0
        
    except Exception as e:
        plt.figure(figsize=(8, 8))
        plt.text(0.5, 0.5, f"Error generating memory process chart: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=12, color='red')
        plt.axis('off')
        saveimage("MemoryProcessInfo.png")
        return 1

def plotMemory():
    try:
        ARAM = give_data("Actual RAM")
        VRAM = give_data("Virtual RAM")

        if not ARAM or not VRAM:
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryInformation.png")
            return 1

        # Check if any critical data is "unable to access"
        total_space = [ARAM.get('Total memory', "unable to access"), VRAM.get('Total VRAM', "unable to access")]
        free_space = [ARAM.get('Free memory', "unable to access"), VRAM.get('Free VRAM', "unable to access")]
        used_space = [ARAM.get('Used-up memory', "unable to access"), VRAM.get('Used-up VRAM', "unable to access")]

        if any(x == "unable to access" for x in total_space + free_space + used_space):
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "Data not provided due to some errors", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryInformation.png")
            return 1

        # Convert to numeric values, handling any potential string values
        try:
            total_space = [float(x) if x != "unable to access" else 0 for x in total_space]
            free_space = [float(x) if x != "unable to access" else 0 for x in free_space]
            used_space = [float(x) if x != "unable to access" else 0 for x in used_space]
        except (ValueError, TypeError):
            plt.figure(figsize=(8, 6))
            plt.text(0.5, 0.5, "Invalid data format in memory information", 
                     horizontalalignment='center', verticalalignment='center', 
                     fontsize=12, color='red')
            plt.axis('off')
            saveimage("MemoryInformation.png")
            return 1

        df = pd.DataFrame({
            'Memory Type': ["Actual RAM", "Virtual RAM"],
            'Total Space (GB)': total_space,
            'Free Space (GB)': free_space,
            'Used Space (GB)': used_space
        })

        # Create a more visually appealing bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = range(len(df['Memory Type']))
        width = 0.25
        
        bars1 = ax.bar([i - width for i in x], df['Total Space (GB)'], width, 
                      label='Total Space', color='#3498db', alpha=0.8)
        bars2 = ax.bar(x, df['Free Space (GB)'], width, 
                      label='Free Space', color='#2ecc71', alpha=0.8)
        bars3 = ax.bar([i + width for i in x], df['Used Space (GB)'], width, 
                      label='Used Space', color='#e74c3c', alpha=0.8)

        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{height:.1f} GB', ha='center', va='bottom', fontsize=9)

        ax.set_xlabel('Memory Type', fontweight='bold')
        ax.set_ylabel('Space (GB)', fontweight='bold')
        ax.set_title('Memory Information Overview', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(df['Memory Type'])
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        saveimage("MemoryInformation.png")
        return 0
        
    except Exception as e:
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Error generating memory chart: {str(e)}", 
                 horizontalalignment='center', verticalalignment='center', 
                 fontsize=12, color='red')
        plt.axis('off')
        saveimage("MemoryInformation.png")
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