import platform
import psutil
import json
import os

#Global declarations
filename="data.json"
ABS_LOCATION = os.path.join("Scripts","Data")
JSON_LOCATE = os.path.join(ABS_LOCATION,filename)

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

    if not os.path.exists(ABS_LOCATION):
        os.makedirs(ABS_LOCATION)
    else:
        pass

    with open(JSON_LOCATE,"w") as f:
        json.dump(data,f,indent=4)


    return 0

def main():
    return 0

if __name__ == "__main__":
    create_JSON()
    main()