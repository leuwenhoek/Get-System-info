import platform
import psutil
import json

def getOS():
    os_name = platform.system()
    os_release = platform.release()
    os_version = platform.version()
    machine_name = platform.node()
    architecture = platform.architecture()
    processor = platform.processor()

    os_dict = {
        "OS" : {
            "Machine name" : machine_name,
            "OS name" : os_name,
            "OS release" : os_release,
            "OS version" : os_version,
            "Processor architecture" : architecture,
            "Processor" : processor
        }
    }

    return os_dict

def create_JSON():
    data = getOS()
    with open("data.json","w") as f:
        json.dump(data,f,indent=4)

    return 0

def main():
    create_JSON()
    return 0

if __name__ == "__main__":
    main()