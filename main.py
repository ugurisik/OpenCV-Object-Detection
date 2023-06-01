from CameraControl import CameraControl
from process import Process
import threading
import os
import torch
import socket
import subprocess


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
            {'class': 'bicycle', 'confidence': 0.2},
            {'class': 'car', 'confidence': 0.2},
            {'class': 'motorcycle', 'confidence': 0.2},
            {'class': 'airplane', 'confidence': 0.2},
            {'class': 'bus', 'confidence': 0.2},
            {'class': 'train', 'confidence': 0.2},
            {'class': 'truck', 'confidence': 0.2},
            {'class': 'boat', 'confidence': 0.2},
            {'class': 'traffic light', 'confidence': 0.2},
            {'class': 'fire hydrant', 'confidence': 0.2},
            {'class': 'stop sign', 'confidence': 0.2},
            {'class': 'parking meter', 'confidence': 0.2},
            {'class': 'bench', 'confidence': 0.2},
            {'class': 'bird', 'confidence': 0.2},
            {'class': 'cat', 'confidence': 0.2},
            {'class': 'dog', 'confidence': 0.2},
            {'class': 'horse', 'confidence': 0.2},
            {'class': 'sheep', 'confidence': 0.2},
            {'class': 'cow', 'confidence': 0.2},
            {'class': 'elephant', 'confidence': 0.2},
            {'class': 'bear', 'confidence': 0.2},
            {'class': 'zebra', 'confidence': 0.2},
            {'class': 'giraffe', 'confidence': 0.2},
            {'class': 'backpack', 'confidence': 0.2},
            {'class': 'umbrella', 'confidence': 0.2},
            {'class': 'handbag', 'confidence': 0.2},
            {'class': 'tie', 'confidence': 0.2},
            {'class': 'suitcase', 'confidence': 0.2},
            {'class': 'frisbee', 'confidence': 0.2},
            {'class': 'skis', 'confidence': 0.2},
            {'class': 'snowboard', 'confidence': 0.2},
            {'class': 'sports ball', 'confidence': 0.2},
            {'class': 'kite', 'confidence': 0.2},
            {'class': 'baseball bat', 'confidence': 0.2},
            {'class': 'baseball glove', 'confidence': 0.2},
            {'class': 'skateboard', 'confidence': 0.2},
            {'class': 'surfboard', 'confidence': 0.2},
            {'class': 'tennis racket', 'confidence': 0.2},
            {'class': 'bottle', 'confidence': 0.2},
            {'class': 'wine glass', 'confidence': 0.2},
            {'class': 'cup', 'confidence': 0.2},
            {'class': 'fork', 'confidence': 0.2},
            {'class': 'knife', 'confidence': 0.2},
            {'class': 'spoon', 'confidence': 0.2},
            {'class': 'bowl', 'confidence': 0.2},
            {'class': 'banana', 'confidence': 0.2},
            {'class': 'apple', 'confidence': 0.2},
            {'class': 'sandwich', 'confidence': 0.2},
            {'class': 'orange', 'confidence': 0.2},
            {'class': 'broccoli', 'confidence': 0.2},
            {'class': 'carrot', 'confidence': 0.2},
            {'class': 'hot dog', 'confidence': 0.2},
            {'class': 'pizza', 'confidence': 0.2},
            {'class': 'donut', 'confidence': 0.2},
            {'class': 'cake', 'confidence': 0.2},
            {'class': 'chair', 'confidence': 0.2},
            {'class': 'couch', 'confidence': 0.2},
            {'class': 'potted plant', 'confidence': 0.2},
            {'class': 'bed', 'confidence': 0.2},
            {'class': 'dining table', 'confidence': 0.2},
            {'class': 'toilet', 'confidence': 0.2},
            {'class': 'tv', 'confidence': 0.2},
            {'class': 'laptop', 'confidence': 0.2},
            {'class': 'mouse', 'confidence': 0.2},
            {'class': 'remote', 'confidence': 0.2},
            {'class': 'keyboard', 'confidence': 0.2},
            {'class': 'cell phone', 'confidence': 0.2},
            {'class': 'microwave', 'confidence': 0.2},
            {'class': 'oven', 'confidence': 0.2},
            {'class': 'toaster', 'confidence': 0.2},
            {'class': 'sink', 'confidence': 0.2},
            {'class': 'refrigerator', 'confidence': 0.2},
            {'class': 'book', 'confidence': 0.2},
            {'class': 'clock', 'confidence': 0.2},
            {'class': 'vase', 'confidence': 0.2},
            {'class': 'scissors', 'confidence': 0.2},
            {'class': 'teddy bear', 'confidence': 0.2},
            {'class': 'hair drier', 'confidence': 0.2},
            {'class': 'toothbrush', 'confidence': 0.2}
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
            },
            {
                'class': 'chair',
                'confidence': 0.2,
            },
            {
                'class': 'bench',
                'confidence': 0.5,
            },
            {
                'class': 'backpack',
                'confidence': 0.5,
            },
            {
                'class': 'umbrella',
                'confidence': 0.5,
            },
            {
                'class': 'handbag',
                'confidence': 0.5,
            },
            {
                'class': 'tie',
                'confidence': 0.5,
            },
            {
                'class': 'bottle',
                'confidence': 0.5,
            },
            {
                'class': 'wine glass',
                'confidence': 0.5,
            },
            {
                'class': 'cup',
                'confidence': 0.5,
            },
            {
                'class': 'couch',
                'confidence': 0.5,
            },
            {
                'class': 'bed',
                'confidence': 0.5,
            },
            {
                'class': 'refrigerator',
                'confidence': 0.1,
            }
        ],
        'model': 'yolov5n.pt',
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
            }
        ],
        'model': 'best20.pt',
        'alarm_sending_time': 10,
    },

}
# [(50.9375, 0.83333), (42.03125, 9.86111), (42.57812, 52.91666), (45.23437, 53.61111), (47.65625, 60.41666), (47.73437, 65.55555), (50.07812, 68.19444), (53.75, 70.41666), (55.46875, 71.25), (55.54687, 75.83333), (55.70312, 76.66666), (56.875, 77.5), (58.4375, 79.44444), (59.6875, 81.38888), (60.85937, 84.86111), (61.40624, 88.75), (62.03125, 92.36111), (62.5, 96.52777), (63.04687, 99.30555), (66.64062, 99.58333), (69.14062, 99.16666), (70.0, 99.02777), (70.39062, 95.83333), (71.25, 88.19444), (71.95312, 82.91666), (72.42187, 81.25), (72.1875, 0.41666)]
# cameraList = {
#     '12': {
#         'name': 'Bahçe',
#         'url': 0,
#         'zone': [],
#         'detection': [
#             {
#                 'class': 'person',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'chair',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'bench',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'backpack',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'umbrella',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'handbag',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'tie',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'bottle',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'wine glass',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'cup',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'couch',
#                 'confidence': 0.5,
#             },
#             {
#                 'class': 'bed',
#                 'confidence': 0.5,
#             },
#         ],
#         'model': 'yolov5n.pt',
#         'alarm_sending_time': 10,
#     },
# }

list = cameraList.items()

ScreenShotPath = './screenshots'
AlertsPath = './alerts'
WeightPath = './weights/'
ApiURL = 'http://localhost:5000/api/cameras'
DefaultModel = 'yolov5n.pt'
port = 8080

model = torch.hub.load('ultralytics/yolov5', 'custom',
                       f'{WeightPath}{DefaultModel}')
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)
if torch.cuda.is_available():
    torch.cuda.synchronize()


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
        exit()


DeleteFiles()
Port()
try:
    while True:
        main()
except Exception as e:
    exit()
