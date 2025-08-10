import os
import json
import plot as pt

# Global declarations
JSON_FILENAME = "db.json"
HTML_FILENAME = "index.html"
CSS_FILENAME = "style.css"
JS_FILENAME = "script.js"
ABS_LOCATION = os.path.join("main", "Scripts")
JSON_LOCATE = os.path.join(ABS_LOCATION, "Data", JSON_FILENAME)
HTML_LOCATE = os.path.join(ABS_LOCATION, "content", HTML_FILENAME)
CSS_LOCATE = os.path.join(ABS_LOCATION, "content", CSS_FILENAME)
JS_LOCATE = os.path.join(ABS_LOCATION, "content", JS_FILENAME)
CPU_GRAPH = "../IMAGE/CpuProcessInfo.png"
MEMORYINFO_GRAPH = "../IMAGE/MemoryInformation.png"
MEMORYPROC_GRAPH = "../IMAGE/MemoryProcessInfo.png"

def load_data():
    with open(JSON_LOCATE, 'r') as f:
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

        # --- HTML ---
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
                    <tr><th>Property</th><th>Results</th></tr>
                    <tr><td>Machine name</td><td>{ machine_name }</td></tr>
                    <tr><td>OS name</td><td>{ OS_name }</td></tr>
                    <tr><td>OS release</td><td>{ OS_release }</td></tr>
                    <tr><td>OS version</td><td>{ OS_version }</td></tr>
                    <tr><td>Processor architecture</td><td>{ pross_arch }</td></tr>
                    <tr><td>Processor</td><td>{ pross }</td></tr>
                </table>
            </section>
            <section>
                <h3>About CPU:</h3>
                <table>
                    <tr><th>Property</th><th>Results</th></tr>
                    <tr><td>Logical CPU</td><td>{ logical_CPU }</td></tr>
                    <tr><td>Physical CPU</td><td>{ Physical_CPU }</td></tr>
                    <tr><td>Threads per core</td><td>{ Thread_perCore }</td></tr>
                    <tr><td>CPU usage</td><td>{ CPU_usage }</td></tr>
                </table>
            </section>
            <section>
                <h3>About RAM (Memory)</h3>
                <h4>Actual RAM</h4>
                <table>
                    <tr><th>Property</th><th>Results</th></tr>
                    <tr><td>Total memory</td><td>{ total_aRAM }</td></tr>
                    <tr><td>Free memory</td><td>{ free_aRAM }</td></tr>
                    <tr><td>Consumed memory</td><td>{ consumed_aRAM }</td></tr>
                    <tr><td>Used-up memory</td><td>{ used_aRAM }</td></tr>
                </table>
                <h4>Virtual RAM</h4>
                <table>
                    <tr><th>Property</th><th>Results</th></tr>
                    <tr><td>Total memory</td><td>{ total_vRAM }</td></tr>
                    <tr><td>Free memory</td><td>{ free_vRAM }</td></tr>
                    <tr><td>Consumed memory</td><td>{ consumed_vRAM }</td></tr>
                    <tr><td>Used-up memory</td><td>{ used_vRAM }</td></tr>
                </table>
            </section>
            <section>
                <h3>About Network</h3>
                <table>
                    <tr>
                        <th>Network name</th>
                        <th>Data downloaded (GB)</th>
                        <th>Data uploaded (GB)</th>
                        <th>Packets uploaded</th>
                        <th>Packets received</th>
                    </tr>
                    {active_networks_html}
                </table>
                <table>
                    <tr><th>deactivated network</th></tr>
                    <tr>{network_html}</tr>
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
                <img src="{MEMORYINFO_GRAPH}" alt="Memory info graph process" width="300" height="200">
                <img src="{MEMORYPROC_GRAPH}" alt="Memory use by top 10 process" width="300" height="200">
                <img src="{CPU_GRAPH}" alt="CPU consumption" width="300" height="200">
            </section>

            <!-- Modal for fullscreen images -->
            <div id="imgModal" class="img-modal">
                <span class="close-btn" id="closeBtn">&times;</span>
                <img class="modal-content" id="modalImg" alt="Expanded image">
            </div>
        </body>
        <script src="\{JS_LOCATE}"></script>
        </html>
        '''
        return content

    def CSS():
        css = '''
        /* PC Results Stylesheet - Modern Dark Theme */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    background: linear-gradient(135deg, #0f1419 0%, #1a2332 25%, #2d1b69 75%, #0f1419 100%);
    color: #e8eaed;
    min-height: 100vh;
    padding: 20px;
    overflow-x: auto;
}

/* Main heading */
.text {
    text-align: center;
    font-size: 2.5em;
    font-weight: 700;
    background: linear-gradient(135deg, #61dafb 0%, #21a1c4 50%, #a8dadc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 40px;
    text-shadow: 0 4px 8px rgba(97, 218, 251, 0.3);
    animation: fadeInDown 0.8s ease-out;
}

@keyframes fadeInDown {
    from {
        opacity: 0;
        transform: translateY(-30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Section styling */
section {
    background: rgba(43, 47, 49, 0.95);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(97, 218, 251, 0.2);
    border-radius: 16px;
    margin: 30px auto;
    padding: 30px;
    max-width: 1200px;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.4),
        0 0 0 1px rgba(255, 255, 255, 0.05);
    transition: all 0.3s ease;
    animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

section:hover {
    transform: translateY(-5px);
    box-shadow: 
        0 25px 50px rgba(97, 218, 251, 0.15),
        0 0 0 1px rgba(97, 218, 251, 0.3);
}

/* Section headings */
h3 {
    color: #61dafb;
    font-size: 1.8em;
    font-weight: 600;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(97, 218, 251, 0.3);
    position: relative;
    display: flex;
    align-items: center;
    gap: 15px;
}

h3::before {
    content: '⚡';
    font-size: 1.2em;
    background: linear-gradient(135deg, #61dafb, #21a1c4);
    padding: 8px 12px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}

h3::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, #61dafb, #21a1c4);
    border-radius: 1px;
}

/* OS Section */
section:nth-of-type(1) h3::before { content: '💻'; }
/* CPU Section */
section:nth-of-type(2) h3::before { content: '🔥'; }
/* RAM Section */
section:nth-of-type(3) h3::before { content: '⚡'; }
/* Network Section */
section:nth-of-type(4) h3::before { content: '🌐'; }

/* Subsection headings */
h4 {
    color: #a8dadc;
    font-size: 1.3em;
    font-weight: 500;
    margin: 25px 0 15px 0;
    padding: 10px 15px;
    background: rgba(97, 218, 251, 0.1);
    border-left: 4px solid #61dafb;
    border-radius: 8px;
}

/* Table styling */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: rgba(58, 63, 65, 0.8);
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

table:hover {
    transform: scale(1.01);
    box-shadow: 0 12px 32px rgba(97, 218, 251, 0.15);
}

th {
    background: linear-gradient(135deg, #61dafb 0%, #21a1c4 100%);
    color: #ffffff;
    padding: 16px 20px;
    font-weight: 600;
    font-size: 1em;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: left;
    position: relative;
}

th::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, rgba(255,255,255,0.3), transparent);
}

td {
    padding: 16px 20px;
    border-bottom: 1px solid rgba(97, 218, 251, 0.1);
    color: #e8eaed;
    font-weight: 400;
    transition: all 0.2s ease;
}

tr {
    transition: all 0.2s ease;
}

tr:hover {
    background: rgba(97, 218, 251, 0.08);
    transform: translateX(5px);
}

tr:hover td {
    color: #ffffff;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

/* First column (property names) styling */
td:first-child {
    font-weight: 500;
    color: #a8dadc;
    background: rgba(168, 218, 220, 0.05);
    position: relative;
}

td:first-child::before {
    content: '▸';
    color: #61dafb;
    margin-right: 8px;
    font-size: 0.9em;
}

/* Second column (values) styling */
td:nth-child(2) {
    color: #61dafb;
    font-family: 'Monaco', 'Consolas', monospace;
    font-weight: 500;
}

/* Network table specific styling */
section:nth-of-type(4) table:first-of-type th {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}

section:nth-of-type(4) table:nth-of-type(2) th {
    background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
}

/* Process table styling */
section:nth-of-type(4) table:last-of-type th {
    background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);
}

/* Image gallery styling */
section:last-of-type {
    text-align: center;
    padding: 40px 30px;
}

section:last-of-type img {
    margin: 15px;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    border: 2px solid rgba(97, 218, 251, 0.2);
}

section:last-of-type img:hover {
    transform: scale(1.05) rotate(1deg);
    box-shadow: 0 15px 35px rgba(97, 218, 251, 0.3);
    border-color: #61dafb;
}

/* Responsive design */
@media (max-width: 1024px) {
    .text {
        font-size: 2em;
    }
    
    section {
        padding: 25px;
        margin: 20px auto;
    }
    
    h3 {
        font-size: 1.5em;
    }
    
    table {
        font-size: 0.9em;
    }
    
    th, td {
        padding: 12px 15px;
    }
}

@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    
    .text {
        font-size: 1.6em;
        margin-bottom: 30px;
    }
    
    section {
        padding: 20px;
        margin: 15px auto;
    }
    
    h3 {
        font-size: 1.3em;
        flex-direction: column;
        text-align: center;
        gap: 10px;
    }
    
    h4 {
        font-size: 1.1em;
        padding: 8px 12px;
    }
    
    table {
        font-size: 0.8em;
        overflow-x: auto;
        display: block;
        white-space: nowrap;
    }
    
    th, td {
        padding: 10px 12px;
    }
    
    section:last-of-type img {
        width: 100%;
        max-width: 300px;
        height: auto;
        margin: 10px 0;
    }
}

@media (max-width: 480px) {
    .text {
        font-size: 1.4em;
    }
    
    h3 {
        font-size: 1.2em;
    }
    
    table {
        font-size: 0.75em;
    }
    
    th, td {
        padding: 8px 10px;
    }
    
    section {
        border-radius: 12px;
        padding: 15px;
    }
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* Selection styling */
::selection {
    background: rgba(97, 218, 251, 0.3);
    color: white;
}

/* Focus styles for accessibility */
*:focus {
    outline: 2px solid #61dafb;
    outline-offset: 2px;
}

/* Loading animation for dynamic content */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.7;
    }
}

.loading {
    animation: pulse 2s infinite;
}

/* Status indicators */
.status-good {
    color: #28a745;
    font-weight: 600;
}

.status-warning {
    color: #ffc107;
    font-weight: 600;
}

.status-critical {
    color: #dc3545;
    font-weight: 600;
}

/* Memory and CPU usage bars */
.usage-bar {
    width: 100%;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-top: 5px;
}

.usage-fill {
    height: 100%;
    background: linear-gradient(90deg, #28a745, #ffc107, #dc3545);
    border-radius: 4px;
    transition: width 0.3s ease;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #61dafb, #21a1c4);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #21a1c4, #61dafb);
}
/* ... (your current CSS remains unchanged, see previous response for full content) ... */

/* Modal styles */
.img-modal {
  display: none; 
  position: fixed; 
  z-index: 9999; 
  padding-top: 60px; 
  left: 0;
  top: 0;
  width: 100%; 
  height: 100%;
  overflow: auto; 
  background-color: rgba(0, 0, 0, 0.9);
}

.img-modal .modal-content {
  margin: auto;
  display: block;
  max-width: 90%;
  max-height: 80vh;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  animation: zoomIn 0.3s ease;
}

@keyframes zoomIn {
  from {transform: scale(0.7);}
  to {transform: scale(1);}
}

/* Close button styles */
.close-btn {
  position: fixed;
  top: 20px;
  right: 35px;
  color: #f1f1f1;
  font-size: 40px;
  font-weight: bold;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #bbb;
}
'''
        return css
    def JScript():
            write_it = '''
            // Get modal elements
            const modal = document.getElementById('imgModal');
            const modalImg = document.getElementById('modalImg');
            const closeBtn = document.getElementById('closeBtn');

            // Attach click event to all images inside the last section
            document.querySelectorAll('section:last-of-type img').forEach(img => {
                img.style.cursor = 'pointer';  // show pointer cursor on hover
                img.onclick = function() {
                    modal.style.display = 'block';
                    modalImg.src = this.src;
                    modalImg.alt = this.alt || "Expanded image";
                }
            });

            // Close modal on clicking close button
            closeBtn.onclick = function() {
                modal.style.display = 'none';
            }

            // Also close modal if clicking outside the image
            modal.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = 'none';
                }
            }
            '''
            return write_it
        
    if want == "html":
        return HTML()
    elif want == "css":
        return CSS()
    elif want == 'js':
        return JScript()
    else:
        raise Exception("Wrong file command")

def create_webpage():
    write_html = content("html")
    write_css = content("css")
    write_js = content('js')
    if not os.path.exists(os.path.join(ABS_LOCATION,"content")):
        os.makedirs(os.path.join(ABS_LOCATION,"content"))
    with open(HTML_LOCATE,'w',encoding='utf-8') as f:
        f.write(write_html)
    with open(CSS_LOCATE,'w',encoding='utf-8') as f:
        f.write(write_css)
    with open(JS_LOCATE,'w',encoding='utf-8') as f:
        f.write(write_js)

def main():
    create_webpage()
    return 0

if __name__ == "__main__":
    main()
