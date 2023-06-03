from CameraControl import CameraControl
from process2 import Process
import threading
import os
import torch
import socket
import subprocess
import logs
import time
from ultralytics import YOLO

logs = logs.Logs('log.txt')

cameraList = {
    '1': {
        'name': 'Bahçe',
        'url': 'rtsp://admin:safarimedia.de@88.248.145.53:3838',
        'zone': [(36.556603773584904, 99.13793103448276),
                 (27.830188679245282, 56.896551724137936),
                 (51.061320754716974, 45.9051724137931),
                 (35.37735849056604, 0.0),
                 (100.0, 0.0),
                 (100.0, 100.0)],
        'detection': [
            {'class': 'person', 'confidence': 0.2},
             {'class': 'couch', 'confidence': 0.2},
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '5': {
        'name': 'Kapı',
        'url': 'rtsp://88.248.145.53:3839/media/video1',
        'zone': [],
        'detection': [
            {
                'class': 'person',
                'confidence': 0.5,
            }
        ],
        'model':None,
        'alarm_sending_time': 10,
    },
    '8': {
        'name': 'Kapı',
        'url': 'rtsp://admin:safarimedia.de@88.248.145.53:3841/Streaming/Channels/101',
        'zone': [(76.0, 0.0),
                 (68.77794089079042, 55.27399865555604),
                 (28.86278545666913, 99.0),
                 (99.0, 99.0),
                 (99.0, 40.27399582866441),
                 (99.0, 0.0)],
        'detection': [
            {
                'class': 'person',
                'confidence': 0.5,
            }
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '9': {
        'name': 'Kapı',
        'url': 'rtsp://88.248.145.53:554/user=admin_password=nTBCS19C_channel=1_stream=0.sdp?real_stream',
        'zone': [],
        'detection': [
            {
                'class': 'person',
                'confidence': 0.5,
            },
            {
                'class': 'refrigerator',
                'confidence': 0.3,
            }
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '10': {
        'name': 'Kapı',
        'url': 'rtsp://admin:W9bz7rza!@5.tcp.eu.ngrok.io:14450',
        'zone': [],
        'detection': [
            {
                'class': 'person',
                'confidence': 0.5,
            }
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
}

list = cameraList.items()

ScreenShotPath = './screenshots'
AlertsPath = './alerts'
WeightPath = './weights/'
ApiURL = 'http://localhost:5000/api/cameras'
DefaultModel = 'yolov8n.pt'
port = 8080

# model = torch.hub.load('ultralytics/yolov5', 'custom',
#                        f'{WeightPath}{DefaultModel}')
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# model.to(device)
# if torch.cuda.is_available():
#     torch.cuda.synchronize()

model = YOLO(f'{WeightPath}{DefaultModel}')

def DeleteFiles():
    for file in os.listdir(ScreenShotPath):
        os.remove(os.path.join(ScreenShotPath, file))
    for file in os.listdir(AlertsPath):
        os.remove(os.path.join(AlertsPath, file))


def Port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    if result == 0:
        print(f"Port {port} is already open.")
    else:
        print(f"Port {port} is closed. Opening the port...")
        try:
            subprocess.Popen(['python3', '-m', 'http.server', str(port)])
            print(f"Port {port} is now open.")
        except Exception as e:
            print(f"Failed to open port {port}: {e}")




def main():
    threads = []
    if not os.path.exists(ScreenShotPath):
        os.mkdir(ScreenShotPath, 0o777)
    if not os.path.exists(AlertsPath):
        os.mkdir(AlertsPath, 0o777)

    cc = CameraControl(ScreenShotPath)

    t = threading.Thread(target=cc.run,  daemon=True)
    threads.append(t)

    for guid, value in list:
        mdl = value['model']
        if mdl is None:
            mdl = model
            defModel = True
        else:
            defModel = False
        process = Process(guid, value, ScreenShotPath,
                          AlertsPath, WeightPath, ApiURL, mdl, defModel)
        t = threading.Thread(target=process.run, daemon=True)
        threads.append(t)
    try:
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print("Ctrl-C pressed...")
        print("Exiting...")
        logs.write_to_log('--- Program Exited ---')
        exit()
    except Exception as e:
        logs.write_to_log(e)


DeleteFiles()
Port()
try:
    logs.write_to_log('--- Program Started ---')
    while True:
        main()
except Exception as e:
    logs.write_to_log(e)