

import json
import time
import requests
import os
import multiprocessing
from CameraControl import CameraControl
from process3 import Process
import logs

logs = logs.Logs('log.txt')

ScreenShotPath = './screenshots'
AlertsPath = './alerts'
WeightPath = './weights/'
ApiURL = 'http://localhost:5000/api/cameras'
jsonFile = 'camlist.json'
cameraList = {}


def FileStructure():
    global ScreenShotPath, AlertsPath, WeightPath, ApiURL
    if not os.path.exists(ScreenShotPath):
        os.mkdir(ScreenShotPath, 0o777)
    if not os.path.exists(ScreenShotPath + '/thumb'):
        os.mkdir(ScreenShotPath + '/thumb', 0o777)
    if not os.path.exists(AlertsPath):
        os.mkdir(AlertsPath, 0o777)


def main():
    processes = []
    while True:
        with open(jsonFile, 'r') as f:
            cameraList = json.load(f)
        time.sleep(1)

        current_list = cameraList.items()
        for guid, value in current_list:
            if any(proc.name == guid for proc in processes):
                for proc in processes:
                    if (guid == proc.name and value != proc.value):
                        print(f'{proc} terminated')
                        proc.terminate()
                        processes.remove(proc)
            else:
                process = Process(guid, value, ScreenShotPath,
                                  AlertsPath, WeightPath, ApiURL)
                p = multiprocessing.Process(target=process.run, daemon=True)
                p.name = guid
                p.value = value
                processes.append(p)
        try:
            for process in processes:
                if not process.is_alive():
                    print(f'{process} started')
                    process.start()
        except KeyboardInterrupt:
            exit()


if __name__ == '__main__':
    FileStructure()
    main()
