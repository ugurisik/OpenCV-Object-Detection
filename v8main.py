from CameraControl import CameraControl
from process2 import Process
import threading
import os
import logs

logs = logs.Logs('log.txt')

cameraList = {
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
            {'class': 'person', 'confidence': 0.3},
            {'class': 'helmet', 'confidence': 0.4},
            {'class': 'vest', 'confidence': 0.4},
        ],

        'alarm_sending_time': 30,
    },
    '5': {
        'name': 'Kapı',
        'url': 'rtsp://88.248.145.53:3839/media/video1',
        'zones': {},
        'detection': [
            {'class': 'person', 'confidence': 0.3},
            {'class': 'helmet', 'confidence': 0.4},
            {'class': 'vest', 'confidence': 0.4},
            {'class': 'door_open', 'confidence': 1500, 'time': 5, 'zone': [
                (58.98437, 5.69444), (58.82812, 10.69444), (73.35937, 12.91666), (73.35937, 8.19444)]},
        ],

        'alarm_sending_time': 30,
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
            {'class': 'person', 'confidence': 0.3},
            {'class': 'helmet', 'confidence': 0.4},
            {'class': 'vest', 'confidence': 0.4},
        ],

        'alarm_sending_time': 30,
    },
    '9': {
        'name': 'Kapı',
        'url': 'rtsp://88.248.145.53:554/user=admin_password=nTBCS19C_channel=1_stream=0.sdp?real_stream',
        'zones': {},
        'detection': [
            {'class': 'person', 'confidence': 0.3},
            {'class': 'helmet', 'confidence': 0.4},
            {'class': 'vest', 'confidence': 0.4},
            {'class': 'grey-palet', 'confidence': 0},
        ],
        'alarm_sending_time': 30,
    }
}


cameraList = cameraList.items()

ScreenShotPath = './screenshots'
AlertsPath = './alerts'
WeightPath = './weights/'
ApiURL = 'http://localhost:5000/api/cameras'


def main():
    threads = []
    if not os.path.exists(ScreenShotPath):
        os.mkdir(ScreenShotPath, 0o777)
    if not os.path.exists(ScreenShotPath+'/thumb'):
        os.mkdir(ScreenShotPath+'/thumb', 0o777)
    if not os.path.exists(ScreenShotPath+'/door'):
        os.mkdir(ScreenShotPath+'/door', 0o777)
    if not os.path.exists(AlertsPath):
        os.mkdir(AlertsPath, 0o777)

    cc = CameraControl(ScreenShotPath)

    t = threading.Thread(target=cc.run,  daemon=True)
    threads.append(t)

    for guid, value in cameraList:

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
        logs.write_to_log('--- Program Exited with Press Key ---')
        exit()
    except Exception as e:
        logs.write_to_log(e)


try:
    logs.write_to_log('--- Program Started ---')
    while True:
        main()
except Exception as e:
    logs.write_to_log(e)
