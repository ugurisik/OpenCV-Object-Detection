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

# cameraList = {
#     # '1': {
#     #     'name': 'Bahçe',
#     #     'url': 0,
#     #     'zone': [(0, 0), (0, 50), (50, 50), (50, 0)],
#     #     'zones': {
#     #         '1': [(50, 50), (50, 100), (100, 100), (100, 50)],
#     #         '2': [(0, 0), (0, 49), (49, 49), (49, 0)]
#     #     },
#     #     'detection': [
#     #         {'class': 'person', 'confidence': 0.3},
#     #         {'class': 'ylk-yok', 'confidence': 0.4},
#     #         {'class': 'ksk-yok', 'confidence': 0.4},
#     #         {'class': 'ylk', 'confidence': 0.4},
#     #         {'class': 'ksk', 'confidence': 0.4},
#     #     ],
#     #
#     #     'alarm_sending_time': 10,
#     # },
#     # '2': {
#     #     'name': 'Bahçe',
#     #     'url': 0,
#     #     'zone': [(0, 0), (0, 50), (50, 50), (50, 0)],
#     #     'zones': {
#     #         '1': [(3.20312, 8.33333), (3.20312, 13.05555), (3.125, 18.05555), (3.28125, 25.83333), (3.20312, 30.69444), (3.04687, 33.88888), (9.84375, 34.30555), (15.54687, 34.44444), (16.09375, 8.05555), (12.89062, 8.19444), (13.04687, 30.0), (5.70312, 30.27777), (5.78125, 9.02777)],
#     #         '2': [(26.79687, 11.94444), (26.79687, 40.83333), (41.25, 40.55555), (41.25, 27.77777), (32.10937, 28.05555), (32.10937, 31.38888), (39.60937, 31.38888), (39.45312, 37.08333), (29.45312, 37.08333), (29.60937, 15.83333), (41.01562, 15.27777), (41.01562, 11.52777)],
#     #         '3': [(45.3125, 20.27777), (45.0, 45.69444), (58.82812, 45.13888), (58.82812, 20.41666), (56.48437, 20.69444), (56.32812, 40.55555), (47.8125, 40.55555), (48.04687, 20.41666)],
#     #         '4': [(62.96874, 20.83333), (62.96874, 46.38888), (65.0, 46.38888), (65.15625, 35.55555), (68.51562, 45.83333), (70.3125, 45.97222), (66.25, 33.05555), (70.15625, 32.91666), (70.07812, 21.11111)],
#     #     },
#     #     'detection': [
#     #         {'class': 'person', 'confidence': 0.3},
#     #         {'class': 'ylk-yok', 'confidence': 0.4},
#     #         {'class': 'ksk-yok', 'confidence': 0.4},
#     #         {'class': 'ylk', 'confidence': 0.4},
#     #         {'class': 'ksk', 'confidence': 0.4},
#     #     ],
#     #
#     #     'alarm_sending_time': 10,
#     # },
#     '1': {
#         'name': 'Bahçe',
#         'url': 'rtsp://admin:safarimedia.de@88.248.145.53:3838',
#         'zones': {
#             '1': [(36.556603773584904, 99.13793103448276),
#                   (27.830188679245282, 56.896551724137936),
#                   (51.061320754716974, 45.9051724137931),
#                   (35.37735849056604, 0.0),
#                   (100.0, 0.0),
#                   (100.0, 100.0)]
#         },
#         'detection': [
#             {'class': 'ins', 'confidence': 0.3},
#             {'class': 'ylk-yok', 'confidence': 0.4},
#             {'class': 'ksk-yok', 'confidence': 0.4},
#             {'class': 'ylk', 'confidence': 0.4},
#             {'class': 'ksk', 'confidence': 0.4},
#         ],

#         'alarm_sending_time': 10,
#     },
#     '5': {
#         'name': 'Kapı',
#         'url': 'rtsp://88.248.145.53:3839/media/video1',
#         'zones': {},
#         'detection': [
#             {'class': 'ins', 'confidence': 0.3},
#             {'class': 'ylk-yok', 'confidence': 0.4},
#             {'class': 'ksk-yok', 'confidence': 0.4},
#             {'class': 'ylk', 'confidence': 0.4},
#             {'class': 'ksk', 'confidence': 0.4},
#         ],

#         'alarm_sending_time': 10,
#     },
#     '8': {
#         'name': 'Kapı',
#         'url': 'rtsp://admin:safarimedia.de@88.248.145.53:3841/Streaming/Channels/101',
#         'zones': {
#             '1': [(76.0, 0.0),
#                   (68.77794089079042, 55.27399865555604),
#                   (28.86278545666913, 99.0),
#                   (99.0, 99.0),
#                   (99.0, 40.27399582866441),
#                   (99.0, 0.0)],
#         },
#         'detection': [
#             {'class': 'ins', 'confidence': 0.3},
#             {'class': 'ylk-yok', 'confidence': 0.4},
#             {'class': 'ksk-yok', 'confidence': 0.4},
#             {'class': 'ylk', 'confidence': 0.4},
#             {'class': 'ksk', 'confidence': 0.4},
#         ],

#         'alarm_sending_time': 10,
#     },
#     '9': {
#         'name': 'Kapı',
#         'url': 'rtsp://88.248.145.53:554/user=admin_password=nTBCS19C_channel=1_stream=0.sdp?real_stream',
#         'zones': {},
#         'detection': [
#             {'class': 'ins', 'confidence': 0.3},
#             {'class': 'ylk-yok', 'confidence': 0.4},
#             {'class': 'ksk-yok', 'confidence': 0.4},
#             {'class': 'ylk', 'confidence': 0.4},
#             {'class': 'ksk', 'confidence': 0.4},
#         ],

#         'alarm_sending_time': 10,
#     }
# }


cameraList = {
    '5': {
        'name': 'Vorderseite',
        'url': 'rtsp://admin:W9bz7rza!@192.168.163.5:554',
        'zones': {
            '1': [(100, 86.55555), (75.875, 44.55555), (22.5625, 41.44444), (0, 80.0), (0, 100), (100, 100)],
        },
        'detection': [
            {
                'class': 'forklift',
                'confidence': 0.6,
            },
            {
                'class': 'forklift',
                'confidence': 0.6,
            },
            {
                'class': 'ameise',
                'confidence': 0.6,
            }
        ],

        'alarm_sending_time': 180,
    },
    '23': {
        'name': 'k.A',
        'url': 'rtsp://admin:W9bz7rza!@192.168.163.23:554',
        'zones': {},
        'detection': [
            {
                'class': 'person',
                'confidence': 0.61,
            },
            {
                'class': 'forklift',
                'confidence': 0.6,
            },
            {
                'class': 'ameise',
                'confidence': 0.6,
            }
        ],

        'alarm_sending_time': 180,
    },
    '26': {
        'name': 'Raucherbereich',
        'url': 'rtsp://admin:W9bz7rza!@192.168.163.26:554',
        'zones': {
            '1': [(0, 0), (50.375, 0), (50.6875, 47.22222), (44.625, 46.44444), (38.5625, 53.44444), (40.0625, 82.0), (38.6875, 85.88888), (59.3125, 89.77777), (59.875, 86.0), (62.9375, 79.77777), (63.5625, 49.33333), (50.875, 47.22222), (50.4375, 0), (99.75, 0), (100, 100), (0, 100)],
        },
        'detection': [
            {
                'class': 'CgOnFace',
                'confidence': 0.6,
            },
            {
                'class': 'person',
                'confidence': 0.61,
            }
        ],

        'alarm_sending_time': 180,
    },
    '31': {
        'name': 'Forklift Test',
        'url': 'rtsp://admin:W9bz7rza!@192.168.163.31:554',
        'zones': {},
        'detection': [
            {
                'class': 'person',
                'confidence': 0.61,
            },
            {
                'class': 'forklift',
                'confidence': 0.6,
            },
            {
                'class': 'ameise',
                'confidence': 0.6,
            }
        ],

        'alarm_sending_time': 180,
    },
    '21': {
        'name': 'Forklift Test',
        'url': 'rtsp://admin:W9bz7rza!@192.168.163.21:554',
        'zones': {},
        'detection': [
            {
                'class': 'person',
                'confidence': 0.61,
            },
            {
                'class': 'forklift',
                'confidence': 0.6,
            },
            {
                'class': 'ameise',
                'confidence': 0.6,
            }
        ],

        'alarm_sending_time': 180,
    }
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

# model = YOLO(f'{WeightPath}{DefaultModel}')


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

        process = Process(guid, value, ScreenShotPath,
                          AlertsPath, WeightPath, ApiURL)
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
