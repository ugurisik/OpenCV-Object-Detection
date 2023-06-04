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
                    # add filename to data as key filename_without_extension
                    images[str(filename_without_extension)] = {
                        'image': f'./screenshots/thumb/{filename}',
                    }
                if file_extension == '.txt':
                    # read txt file
                    with open(f'./screenshots/{filename}', 'r') as f:
                        data[str(filename_without_extension)] = {
                            'text': f.read(),
                        }

                
            files ={}
            for key, value in images.items():
                files[key] = ('image', open(value['image'], 'rb'))
                    
            datas = {}
            for key, value in data.items():
                datas[key] = value['text'] + ' '
            datas['ss'] = 'ss'
            # if files is empty array 
            url = 'https://securiteye.ai/API/detect.php'
            try:
                response = self.requests.post(url, files=files, data=datas, timeout=10)
                response.raise_for_status()  # Non-2xx status codes will raise an exception
                print(f'SendScreenShot() Response: {response.text}')
            except Exception as e:
                print(f'SendScreenShot() Exception: {e}')

        except Exception as e:
            print(e)
        
    def SendAlert(self, guid, image_path, alarm_type=1000, now_detected = ''):
        try:
            url = 'https://securiteye.ai/API/detect.php'
            files = {'screenshot': open(image_path, 'rb')}
            data = {
                'cam_id': 5,
                'alarm_type': alarm_type,
                'now_detected': now_detected,
                'screenshot': image_path
            }
            # params = {'cam_id': 5,
            #       'alarm_type': alarm_type, 'screenshot': image_path, 'now_detected': now_detected}
            print('******************************************************************************************************************************************')
            print(f'Alarm Sent! Guid: {guid} Image: {image_path} Alarm Type: {alarm_type} Now Detected: {now_detected}')
            print('******************************************************************************************************************************************')
            # url = 'https://securiteye.ai/API/detect.php?' + \
            #     '&'.join([f"{k}={v}" for k, v in params.items()])
            try:
                # response = self.requests.get(url, timeout=3)
                # response.raise_for_status()  # Raise an exception for non-2xx status codes

                response = self.requests.post(url, files=files, data=data, timeout=10)
                response.raise_for_status()  # Non-2xx status codes will raise an exception

                return True
            except Exception as e:
                self.logs.write_to_log(e)
                print(f'Alarm not sent for cam id: {guid} Exception: {e}')
                return False
        except Exception as e:
            self.logs.write_to_log(e)
            return False
