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
import shutil

logs = logs.Logs('log.txt')

cameraList = {
    '123': {
        'name': 'Bahçe',
        'url': 0,
        'zone': [(0, 0), (0, 50), (50, 50), (50, 0)],
        'zones': {
            '1': [(50, 50), (50, 100), (100, 100), (100, 50)],
            '2': [(0, 0), (0, 49), (49, 49), (49, 0)]
        },
        'detection': [
            {'class': 'person', 'confidence': 0.3},
            {'class': 'ylk-yok', 'confidence': 0.4},
            {'class': 'ksk-yok', 'confidence': 0.4},
            {'class': 'ylk', 'confidence': 0.4},
            {'class': 'ksk', 'confidence': 0.4},
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    # '2': {
    #     'name': 'Bahçe',
    #     'url': 0,
    #     'zone': [(0, 0), (0, 50), (50, 50), (50, 0)],
    #     'zones': {
    #         '1': [(3.20312, 8.33333), (3.20312, 13.05555), (3.125, 18.05555), (3.28125, 25.83333), (3.20312, 30.69444), (3.04687, 33.88888), (9.84375, 34.30555), (15.54687, 34.44444), (16.09375, 8.05555), (12.89062, 8.19444), (13.04687, 30.0), (5.70312, 30.27777), (5.78125, 9.02777)],
    #         '2': [(26.79687, 11.94444), (26.79687, 40.83333), (41.25, 40.55555), (41.25, 27.77777), (32.10937, 28.05555), (32.10937, 31.38888), (39.60937, 31.38888), (39.45312, 37.08333), (29.45312, 37.08333), (29.60937, 15.83333), (41.01562, 15.27777), (41.01562, 11.52777)],
    #         '3': [(45.3125, 20.27777), (45.0, 45.69444), (58.82812, 45.13888), (58.82812, 20.41666), (56.48437, 20.69444), (56.32812, 40.55555), (47.8125, 40.55555), (48.04687, 20.41666)],
    #         '4': [(62.96874, 20.83333), (62.96874, 46.38888), (65.0, 46.38888), (65.15625, 35.55555), (68.51562, 45.83333), (70.3125, 45.97222), (66.25, 33.05555), (70.15625, 32.91666), (70.07812, 21.11111)],
    #     },
    #     'detection': [
    #         {'class': 'person', 'confidence': 0.3},
    #         {'class': 'ylk-yok', 'confidence': 0.4},
    #         {'class': 'ksk-yok', 'confidence': 0.4},
    #         {'class': 'ylk', 'confidence': 0.4},
    #         {'class': 'ksk', 'confidence': 0.4},
    #     ],
    #
    #     'alarm_sending_time': 10,
    # },
    '9': {
        'name': 'Kapı',
        'url': 'rtsp://88.248.145.53:554/user=admin_password=nTBCS19C_channel=1_stream=0.sdp?real_stream',
        'zones': {},
        'detection': [
            {'class': 'person', 'confidence': 0.4},
            {'class': 'no-helmet', 'confidence': 0.4},
            {'class': 'no-vest', 'confidence': 0.4},
            {'class': 'ameise', 'confidence': 0.4},
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '1': {
        'name': 'Bahçe',
        'url': 'rtsp://admin:safarimedia.de@88.248.145.53:3838',
        'zones': {
            '1': [(36.556603773584904, 99.13793103448276),
                  (27.830188679245282, 56.896551724137936),
                  (51.061320754716974, 45.9051724137931),
                  (35.37735849056604, 0.0),
                  (100.0, 0.0),
                  (100.0, 100.0)]
        },
        'detection': [
            {'class': 'person', 'confidence': 0.4},
            {'class': 'no-helmet', 'confidence': 0.4},
            {'class': 'no-vest', 'confidence': 0.4},
            {'class': 'ameise', 'confidence': 0.4},
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '5': {
        'name': 'Kapı',
        'url': 'rtsp://88.248.145.53:3839/media/video1',
        'zones': {},
        'detection': [
            {'class': 'person', 'confidence': 0.4},
            {'class': 'no-helmet', 'confidence': 0.4},
            {'class': 'no-vest', 'confidence': 0.4},
            {'class': 'ameise', 'confidence': 0.4},
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '8': {
        'name': 'Kapı',
        'url': 'rtsp://admin:safarimedia.de@88.248.145.53:3841/Streaming/Channels/101',
        'zones': {
            '1': [(76.0, 0.0),
                  (68.77794089079042, 55.27399865555604),
                  (28.86278545666913, 99.0),
                  (99.0, 99.0),
                  (99.0, 40.27399582866441),
                  (99.0, 0.0)],
        },
        'detection': [
            {'class': 'person', 'confidence': 0.4},
            {'class': 'no-helmet', 'confidence': 0.4},
            {'class': 'no-vest', 'confidence': 0.4},
            {'class': 'ameise', 'confidence': 0.4},
        ],
        'model': None,
        'alarm_sending_time': 10,
    },
    '10': {
        'name': 'Kapı',
        'url': 'output.mp4',
        'zones': {},
        'detection': [
            {'class': 'door_open', 'confidence': 3000, "time": 50, "zone": [
                (92.91666, 28.33333), (92.86458, 30.18518), (99.01041, 35.18518), (99.11458, 33.24074)]},
        ],
        'model': None,
        'alarm_sending_time': 200,
    },
    '11': {
        'name': 'Palet',
        'url': 'output.mp4',
        'zones': {
            '1': [(79.58333, 32.59259), (44.16666, 32.59259), (29, 100), (100, 100), (100, 64.16666), (100, 60.37037)]
        },
        'detection': [
            {'class': 'grey-palet', 'confidence': 0.0000000000000000001}
        ],
        'model': 'best-15.pt',
        'alarm_sending_time': 200,
    },
    '12': {
        'name': 'Tır',
        'url': 'tir.mp4',
        'zones': {},
        'detection': [
            {'class': 'lkw', 'confidence': 0.3},
        ],
        'model': None,
        'alarm_sending_time': 200,
    }
}

list = cameraList.items()

ScreenShotPath = './screenshots'
AlertsPath = './alerts'
WeightPath = './weights/'
ApiURL = 'http://localhost:5000/api/cameras'
DefaultModel = 'best-6.pt'
port = 8080

# model = torch.hub.load('ultralytics/yolov5', 'custom',
#                        f'{WeightPath}{DefaultModel}')
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# model.to(device)
# if torch.cuda.is_available():
#     torch.cuda.synchronize()

model = YOLO(f'{WeightPath}{DefaultModel}')


def DeleteFiles():
    shutil.rmtree(ScreenShotPath)

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
    if not os.path.exists(ScreenShotPath+'/thumb'):
        os.mkdir(ScreenShotPath+'/thumb', 0o777)
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
            print(f'Using default model for {value["name"]}')
        else:
            print(f'Using {mdl} for {value["name"]}')
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


# DeleteFiles()
# Port()
try:
    logs.write_to_log('--- Program Started ---')
    while True:
        main()
except Exception as e:
    logs.write_to_log(e)
