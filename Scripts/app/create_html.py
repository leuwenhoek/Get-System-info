import os
import json
import plot as pt

# Global declarations
JSON_FILENAME = "data.json"
HTML_FILENAME = "index.html"
CSS_FILENAME = "style.css"
ABS_LOCATION = os.path.join("Scripts")
JSON_LOCATE = os.path.join(ABS_LOCATION,"Data", JSON_FILENAME)
HTML_LOCATE = os.path.join(ABS_LOCATION,"content",HTML_FILENAME)
CSS_LOCATE = os.path.join(ABS_LOCATION,"content",CSS_FILENAME)
CPU_GRAPH = "../IMAGE/CpuProcessInfo.png"
MEMORYINFO_GRAPH = "../IMAGE/MemoryInformation.png"
MEMORYPROC_GRAPH = "../IMAGE/MemoryProcessInfo.png"
def load_data():
    with open(JSON_LOCATE,'r') as f:
        data = json.load(f)
    return data


def get_data(want):
    data = load_data()
    mem_data = data["MEMORY"]
    given = want.lower()
    # --- OS Data ---
    if given == "os data":
        return data["OS"] 
        

    # --- CPU Data ---
    elif given == "cpu data":
        return data["CPU"]

    # --- RAM Data ---
    elif given == "aram data":
        return mem_data["Actual RAM"]
        

    elif given == "vram data":
        return mem_data["Virtual RAM"]
    
    elif given == "active network data":
        net_data = data["NETWORK"]["Active networks"]
        return net_data
    elif given == "inactive network data":
        inactive_data = data["NETWORK"]["Inactive networks"]
        return inactive_data
    elif given == "process data":
        top_processes = data["PROCESS"]["top_processes"]
        return top_processes
    else:
        raise Exception("Wrong command")




def content(want):

    os_data = get_data("os data")
    machine_name = os_data["Machine name"]
    OS_name = os_data["OS name"]
    OS_release = os_data["OS release"]
    OS_version = os_data["OS version"]
    pross_arch = os_data["Processor architecture"]   # may be a list
    pross = os_data["Processor"]

    cpu_data = get_data("cpu data")
    logical_CPU = cpu_data["Logical CPU"]
    Physical_CPU = cpu_data["Physical CPU"]
    Thread_perCore = cpu_data["Threads per core"]
    CPU_usage = cpu_data["CPU usage"]

    aRAM = get_data("aram data")
    total_aRAM = aRAM["Total memory"]
    free_aRAM = aRAM["Free memory"]
    consumed_aRAM = aRAM["Consumed memory (%)"]
    used_aRAM = aRAM["Used-up memory"]
    
    vRAM = get_data("vram data")
    total_vRAM = vRAM["Total VRAM"]
    free_vRAM = vRAM["Free VRAM"]
    consumed_vRAM = vRAM["Consumed VRAM (%)"]
    used_vRAM = vRAM["Used-up VRAM"]


    inactive_data = get_data("inactive network data")
    network = [v["Network name"] for v in inactive_data.values()]

    top_process = get_data("process data")
    top_process_html = ""
    for proc in top_process:
        top_process_html += f"""
        <tr>
            <td>{proc['pid']}</td>
            <td>{proc['name']}</td>
            <td>{proc['cpu']}</td>
            <td>{proc['memory']}</td>
        </tr>
        """


        # Active networks
    net_data = get_data("active network data")
    

    active_networks_html = ""
    for active in net_data.values():
        activeNetwork_name = active["Network name"]
        data_downloaded = active["Data downloaded"]
        data_uploaded = active["Data uploaded"]
        packets_uploaded = active["Total packets uploaded"]
        packets_received = active["Total packets received"]

        active_networks_html += f"""
        <tr>
            <td>{activeNetwork_name}</td>
            <td>{data_downloaded}</td>
            <td>{data_uploaded}</td>
            <td>{packets_uploaded}</td>
            <td>{packets_received}</td>
        </tr>
        """

    def HTML():

        network_html = ""
        for names in network:
            network_html += f"<td>{names}</td>\n"

        content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Your PC Results</title>
            <link rel="stylesheet" href="style.css">
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Anton&family=Mozilla+Headline:wght@200..700&family=Noto+Color+Emoji&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=WDXL+Lubrifont+TC&display=swap');
            </style>
        </head>
        <body>
            <h1 class="text">Hello { machine_name }, this is the Results of the diagnose.</h1>
            
            <section>
                <h3>About OS:</h3>
                <table>
                    <tr>
                        <th>Property</th>
                        <th>Results</th>
                    </tr>
                    <tr>
                        <td>Machine name</td>
                        <td>{ machine_name }</td>
                    </tr>
                    <tr>
                        <td>OS name</td>
                        <td>{ OS_name }</td>
                    </tr>
                    <tr>
                        <td>OS release</td>
                        <td>{ OS_release }</td>
                    </tr>
                    <tr>
                        <td>OS version</td>
                        <td>{ OS_version }</td>
                    </tr>
                    <tr>
                        <td>Processor architecture</td>
                        <td>{ pross_arch }</td>
                    </tr>
                    <tr>
                        <td>Processor</td>
                        <td>{ pross }</td>
                    </tr>
                </table>
            </section>

            <section>
                <h3>About CPU:</h3>
                <table>
                    <tr>
                        <th>Property</th>
                        <th>Results</th>
                    </tr>
                    <tr>
                        <td>Logical CPU</td>
                        <td>{ logical_CPU }</td>
                    </tr>
                    <tr>
                        <td>Physical CPU</td>
                        <td>{ Physical_CPU }</td>
                    </tr>
                    <tr>
                        <td>Threads per core</td>
                        <td>{ Thread_perCore }</td>
                    </tr>
                    <tr>
                        <td>CPU usage</td>
                        <td>{ CPU_usage }</td>
                    </tr>
                </table>
            </section>

            <section>
                <h3>About RAM (Memory)</h3>
                
                <h4>Actual RAM</h4>
                <table>
                    <tr>
                        <th>Property</th>
                        <th>Results</th>
                    </tr>
                    <tr>
                        <td>Total memory</td>
                        <td>{ total_aRAM }</td>
                    </tr>
                    <tr>
                        <td>Free memory</td>
                        <td>{ free_aRAM }</td>
                    </tr>
                    <tr>
                        <td>Consumed memory</td>
                        <td>{ consumed_aRAM }</td>
                    </tr>
                    <tr>
                        <td>Used-up memory</td>
                        <td>{ used_aRAM }</td>
                    </tr>
                </table>

                <h4>Virtual RAM</h4>
                <table>
                    <tr>
                        <th>Property</th>
                        <th>Results</th>
                    </tr>
                    <tr>
                        <td>Total memory</td>
                        <td>{ total_vRAM }</td>
                    </tr>
                    <tr>
                        <td>Free memory</td>
                        <td>{ free_vRAM }</td>
                    </tr>
                    <tr>
                        <td>Consumed memory</td>
                        <td>{ consumed_vRAM }</td>
                    </tr>
                    <tr>
                        <td>Used-up memory</td>
                        <td>{ used_vRAM }</td>
                    </tr>
                </table>
            </section>

            <section>
                <h3>About Network</h3>
                <table>
                    <tr>
                        <th>Network name</th>
                        <th>Data downloaded</th>
                        <th>Data uploaded</th>
                        <th>Packets uploaded</th>
                        <th>Packets received</th>
                    </tr>
                    {active_networks_html}
                </table>
                <table>
                    <tr>
                        <th>deactivated network</th>
                    </tr>
                    <tr>
                        {network_html}
                    </tr>
                </table>
                <h3>Top Processes</h3>
                <table>
                    <tr>
                        <th>PID</th>
                        <th>Name</th>
                        <th>CPU (%)</th>
                        <th>Memory (MB)</th>
                    </tr>
                    {top_process_html}
                </table>
            </section>
            <section>
                <img src="{MEMORYINFO_GRAPH}" alt="Memory info graph process" width="600" height="500">
                <img src="{MEMORYPROC_GRAPH}" alt="Memory use by top 10 process" width="600" height="500">
                <img src="{CPU_GRAPH}" alt="CPU consumption" width="600" height="500">
            </section>
        </body>
        </html>
        '''
        return content
    def CSS():
        css = '''
        :root {
            --primary: #4a6cf7;
            --secondary: #764ba2;
            --accent: #ff6b6b;
            --success: #27ae60;
            --warning: #f39c12;
            --danger: #e74c3c;
            --dark: #2c3e50;
            --light: #f8f9fa;
            --gray: #ecf0f1;
            --card-bg: rgba(255, 255, 255, 0.95);
            --text-dark: #2c3e50;
            --text-light: #7f8c8d;
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: var(--text-dark);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at top right, rgba(255,255,255,0.1) 0%, transparent 30%);
            z-index: -1;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .text {
            text-align: center;
            font-family: 'Anton', sans-serif;
            font-size: 2.5rem;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            padding: 20px;
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 30px;
            position: relative;
            overflow: hidden;
        }

        .text::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shine 3s infinite;
        }

        @keyframes shine {
            100% {
                left: 100%;
            }
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }

        section {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 18px;
            box-shadow: var(--shadow);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.3);
            transition: var(--transition);
            position: relative;
            overflow: hidden;
        }

        section:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 45px rgba(0,0,0,0.2);
        }

        section::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary), var(--secondary));
        }

        h3 {
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--text-dark);
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--primary);
            display: flex;
            align-items: center;
            gap: 12px;
        }

        h3 i {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
        }

        h4 {
            font-family: 'Poppins', sans-serif;
            font-size: 1.3rem;
            font-weight: 500;
            color: var(--text-dark);
            margin: 25px 0 15px 0;
            padding-left: 15px;
            border-left: 4px solid var(--warning);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: #fff;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 5px 20px rgba(0,0,0,0.05);
            position: relative;
        }

        th {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            font-weight: 500;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 18px 15px;
            text-align: left;
            position: relative;
        }

        th::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--accent), var(--warning));
        }

        td {
            padding: 15px;
            border-bottom: 1px solid var(--gray);
            font-size: 0.95rem;
            transition: var(--transition);
        }

        tr:nth-child(even) td {
            background-color: var(--light);
        }

        tr:hover td {
            background-color: #e3f2fd;
        }

        td:first-child {
            font-weight: 600;
            color: var(--text-dark);
            background: linear-gradient(90deg, var(--light), transparent);
            min-width: 180px;
        }

        td:not(:first-child) {
            font-family: 'Roboto Mono', monospace;
            font-weight: 500;
        }

        .network-section table:first-of-type th {
            background: linear-gradient(135deg, var(--success), #229954);
            font-size: 0.85rem;
        }

        .network-section table:first-of-type td {
            text-align: center;
            font-size: 0.9rem;
        }

        .network-section table:nth-of-type(2) th {
            background: linear-gradient(135deg, var(--danger), #c0392b);
        }

        .network-section table:nth-of-type(2) td {
            color: var(--danger);
            font-style: italic;
            text-align: center;
        }

        .network-section table:nth-of-type(3) th {
            background: linear-gradient(135deg, var(--warning), #e67e22);
        }

        .network-section table:nth-of-type(3) td:nth-child(3),
        .network-section table:nth-of-type(3) td:nth-child(4) {
            text-align: right;
            font-weight: bold;
        }

        .images-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 20px;
        }

        .images-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); /* minimum size increased for clarity */
    gap: 25px;
    margin-top: 20px;
}

.image-card {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    transition: var(--transition);
    width: 100%;
    height: auto; /* remove fixed height for flexibility */
    aspect-ratio: 16/9; /* maintains proportions while scaling */
}

.image-card img {
    width: 100%;
    height: 100%;
    object-fit: contain; /* keeps entire chart visible without cropping */
    transition: var(--transition);
}

/* Medium screens */
@media (max-width: 768px) {
    .images-container {
        grid-template-columns: 1fr; /* single column */
    }
    .image-card {
        aspect-ratio: 4/3; /* taller on smaller screens */
    }
}

/* Small screens */
@media (max-width: 480px) {
    .image-card {
        aspect-ratio: 1/1; /* square for very small displays */
    }
}

        .image-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.25);
        }

        .image-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: var(--transition);
        }

        .image-card:hover img {
            transform: scale(1.05);
        }

        .image-card .caption {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: 500;
            transform: translateY(100%);
            transition: var(--transition);
        }

        .image-card:hover .caption {
            transform: translateY(0);
        }

        .status-good {
            color: var(--success) !important;
            font-weight: bold;
        }

        .status-warning {
            color: var(--warning) !important;
            font-weight: bold;
        }

        .status-critical {
            color: var(--danger) !important;
            font-weight: bold;
        }

        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }

        .status-good .status-indicator {
            background: var(--success);
            box-shadow: 0 0 8px var(--success);
        }

        .status-warning .status-indicator {
            background: var(--warning);
            box-shadow: 0 0 8px var(--warning);
        }

        .status-critical .status-indicator {
            background: var(--danger);
            box-shadow: 0 0 8px var(--danger);
        }

        .footer {
            text-align: center;
            padding: 30px;
            color: rgba(255,255,255,0.7);
            font-size: 0.9rem;
            margin-top: 20px;
        }

        @media (max-width: 1100px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .text {
                font-size: 2rem;
                padding: 15px;
            }
            
            section {
                padding: 25px 20px;
            }
            
            h3 {
                font-size: 1.6rem;
            }
            
            h4 {
                font-size: 1.2rem;
            }
            
            th, td {
                padding: 12px 10px;
            }
            
            .image-card {
                height: 220px;
            }
        }

        @media (max-width: 480px) {
            body {
                padding: 15px;
            }
            
            .text {
                font-size: 1.8rem;
            }
            
            h3 {
                font-size: 1.4rem;
            }
            
            th {
                font-size: 0.8rem;
            }
            
            td {
                font-size: 0.85rem;
                padding: 10px 8px;
            }
            
            .images-container {
                grid-template-columns: 1fr;
            }
        }
    
'''
        return css
    if want == "html":
        return HTML()
    elif want == "css":
        return CSS()
    else:
        raise Exception("Wrong file command")



    

def create_webpage():
    write_html = content("html")
    write_css = content("css")
    if not os.path.exists(os.path.join(ABS_LOCATION,"content")):
        os.makedirs(os.path.join(ABS_LOCATION,"content"))
    
    with open(HTML_LOCATE,'w') as f:
        f.write(write_html)
    with open(CSS_LOCATE,'w') as f:
        f.write(write_css)


def main():
    create_webpage()
    return 0
if __name__ == "__main__":
    main()
