# Get-System-info

System Monitor is a Python-based tool that collects system performance metrics (CPU, memory, disk, battery, network, and processes) and visualizes them using bar and pie charts. It generates a JSON file with system data and produces graphical outputs for memory and process usage.

## Features
- **Data Collection**: Gathers system information using `psutil` and `platform` libraries.
- **Data Storage**: Saves metrics to a JSON file (`data.json`) for persistence.
- **Visualizations**:
  - Bar chart for physical and virtual memory usage.
  - Pie charts for CPU and memory usage by top 10 processes.
- **Modular Design**: Separated into `fetch.py` (data collection), `plot.py` (visualization), and `main.py` (orchestration).

## Requirements
- Python 3.6+
- Libraries: `psutil`, `matplotlib`, `pandas`
- Operating System: Windows or Unix-like (Linux, macOS)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/leuwenhoek/Get-System-info.git
   ```
2. Install dependencies:
   ```bash
   pip install psutil matplotlib pandas
   ```
3. Ensure the `Scripts/Data` and `Scripts/IMAGE` directories are writable for JSON and image outputs.

## Usage
1. Run the main script:
   ```bash
   python main.py
   ```
2. The script will:
   - Collect system metrics and save them to `Scripts/Data/data.json`.
   - Generate three plots saved in `Scripts/IMAGE`:
     - `MemoryInformation.png`: Bar chart of physical and virtual memory stats.
     - `CpuProcessInfo.png`: Pie chart of CPU usage by top 10 processes.
     - `MemoryProcessInfo.png`: Pie chart of memory usage by top 10 processes.

## Project Structure
- `fetch.py`: Collects system metrics (OS, CPU, memory, disk, battery, network, processes) and saves to JSON.
- `plot.py`: Loads JSON data and generates visualizations using `matplotlib` and `pandas`.
- `main.py`: Orchestrates data collection and plotting.
- `Scripts/Data/data.json`: Output file for system metrics.
- `Scripts/IMAGE/*.png`: Output directory for generated plots.

## Limitations
- **Error Handling**: Minimal error handling is implemented. The code may fail if:
  - `data.json` is missing, corrupted, or inaccessible.
  - Hardware-specific features (e.g., battery) are unavailable.
  - Disk or file permissions are restricted.
- **Bugs**: The `getDisk()` function in `fetch.py` overwrites disk I/O data, storing only the last disk's stats.
- **Platform Support**: Assumes Windows (`C:\`) or Unix-like (`/`) systems; may not work on other platforms.
- **Visualization**: Plots are basic and may have overlapping labels for large datasets.

## Future Improvements
- Add comprehensive error handling for file operations and `psutil` calls.
- Fix the disk I/O data overwrite bug in `getDisk()`.
- Enhance plot readability with dynamic sizing and better color schemes.
- Add support for more platforms and hardware

## Note

Point to be noted that `project is under development phase`.