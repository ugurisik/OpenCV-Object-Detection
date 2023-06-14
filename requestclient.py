import requests as req
import logs
import os
import time


class RequestClient:
    def __init__(self):
        self.requests = req
        self.logs = logs.Logs('log.txt')
        self.os = os
        self.time = time

    def run(self):
        print("Requests.run() is running...")

    def SendScreenShot(self):
        try:
            print("SendScreenShot() is running...")
            files = self.os.listdir('./screenshots')
            images = {}
            data = {}
            for file in files:
                filename = self.os.path.basename(file)
                file_extension = self.os.path.splitext(filename)[1]
                filename_without_extension = self.os.path.splitext(filename)[0]
                print(f'./screenshots/{filename}')
                if file_extension == '.jpg':
                    images[str(filename_without_extension)] = {
                        'image': f'./screenshots/thumb/{filename}',
                    }
                if file_extension == '.txt':
                    with open(f'./screenshots/{filename}', 'r') as f:
                        data[str(filename_without_extension)] = {
                            'text': f.read(),
                        }

            files = {}
            for key, value in images.items():
                files[key] = ('image', open(value['image'], 'rb'))

            datas = {}
            for key, value in data.items():
                datas[key] = value['text'] + ' '
            datas['ss'] = 'ss'
            url = 'https://securiteye.ai/API/detect.php'
            try:
                response = self.requests.post(
                    url, files=files, data=datas, timeout=(10, 200))
                response.raise_for_status()  # Non-2xx status codes will raise an exception
                print(f'SendScreenShot() Response: {response.text}')
            except Exception as e:
                print(f'SendScreenShot() Exception: {e}')

        except Exception as e:
            print(e)

    def SendAlert(self, guid, image_path, alarm_type=1000, now_detected=''):
        try:
            url = 'https://securiteye.ai/API/detect.php'
            files = {'screenshot': open(image_path, 'rb')}
            data = {
                'cam_id': guid,
                'alarm_type': alarm_type,
                'now_detected': now_detected,
                'screenshot': image_path
            }
            print('******************************************************************************************************************************************')
            print(
                f'Alarm Sent! Guid: {guid} Image: {image_path} Alarm Type: {alarm_type} Now Detected: {now_detected}')
            print('******************************************************************************************************************************************')
            try:

                response = self.requests.post(
                    url, files=files, data=data, timeout=(10, 200))
                response.raise_for_status()  # Non-2xx status codes will raise an exception
                self.logs.write_to_log(
                    f'Alarm sending for GUID {guid} Alarm Type: {alarm_type} Now Detected: {now_detected} Response: {response.text} Image: {image_path}')
                return True
            except Exception as e:
                self.logs.write_to_log(e)
                print(f'Alarm not sent for cam id: {guid} Exception: {e}')
                return False
        except Exception as e:
            self.logs.write_to_log(e)
            return False
