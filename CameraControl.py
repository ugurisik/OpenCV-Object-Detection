import os
import time
import requestclient
import logs

class CameraControl:
    def __init__(self, filePath):
        self.filePath = filePath
        self.os = os
        self.time = time
        self.cams = []
        self.request = requestclient.RequestClient()
        self.logs = logs.Logs('log.txt')

    def run(self):

        
            print("CameraControl.run() is running...")
            while True:
                try:
                    files = self.os.listdir(self.filePath)
                    for file in files:
                        filepath = self.os.path.join(self.filePath, file)
                        filename = self.os.path.basename(filepath)
                        filename_without_extension = self.os.path.splitext(filename)[0]
                        file_extension = self.os.path.splitext(filename)[1]
                        file_modification_time = self.os.path.getmtime(filepath)
                        current_time_10min = self.time.strftime(
                            '%Y-%m-%d %H:%M:%S', self.time.localtime(time.time() - 300))  # dosya düzenleme zamanı 5 dakikadan eski ise alarm gönderiyoruz
                        if file_extension == '.jpg':
                            if not any(cam[0] == filename_without_extension for cam in self.cams):
                                self.cams.append([filename_without_extension, False])
                            modification_time = self.time.strftime(
                                '%Y-%m-%d %H:%M:%S', self.time.localtime(file_modification_time))
                            if modification_time < current_time_10min:
                                print(
                                    f'Cam ID: {filename_without_extension} is not working')
                                for cam in self.cams:
                                    if cam[0] == filename_without_extension and cam[1] == False:
                                        self.SendAlarm(cam[0])
                            else:
                                print(
                                    f'Cam ID: {filename_without_extension} is working')
                            self.CheckCams()
                    time.sleep(15)
                    print(f'cams count: {len(self.cams)}')
                except Exception as e:
                    logs.write_to_log(e)
    def CheckCams(self):
        for cam in self.cams:
            if cam[1]:
                current_time_3min = self.time.strftime(
                    '%Y-%m-%d %H:%M:%S', self.time.localtime(time.time() - 120))  #  dosya düzenleme zamanı 2 dakikadan yeni ise durumunu güncelliyoruz, current_time_10min'den küçük olması gerekiyor
                filename = cam[0] + '.jpg'
                filepath = self.os.path.join(self.filePath, filename)
                file_modification_time = self.os.path.getmtime(filepath)
                modification_time = self.time.strftime(
                    '%Y-%m-%d %H:%M:%S', self.time.localtime(file_modification_time))
                if modification_time > current_time_3min:
                    if self.request.SendAlert(cam[0], f'{cam[0]}.jpg', 1001):
                        cam[1] = False
                        print(
                            f'Alarm sent for cam id: {cam[0]} after working again')
                    else:
                        print(
                            f'Alarm not sent for cam id: {cam[0]} after working again')
                        cam[1] = True

    def SendAlarm(self, guid):
        for cam in self.cams:
            if cam[0] == guid:
                if self.request.SendAlert(cam[0], f'{cam[0]}.jpg'):
                    print(f'Alarm sent for cam id: {guid}')
                    cam[1] = True
                else:
                    print(f'Alarm not sent for cam id: {cam[0]}')
                    cam[1] = False
