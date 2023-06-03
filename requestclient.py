import requests as req
import logs

class RequestClient:
    def __init__(self):
        self.requests = req
        self.logs = logs.Logs('log.txt')

    def run(self):
        print("Requests.run() is running...")

    def SendAlert(self, guid, image_path, alarm_type=1000, now_detected = ''):
        try:
            params = {'cam_id': 5,
                  'alarm_type': alarm_type, 'screenshot': image_path, 'now_detected': now_detected}
            print('******************************************************************************************************************************************')
            print(f'Alarm Sent! Guid: {guid} Image: {image_path} Alarm Type: {alarm_type} Now Detected: {now_detected}')
            print('******************************************************************************************************************************************')
            url = 'https://securiteye.ai/API/detect.php?' + \
                '&'.join([f"{k}={v}" for k, v in params.items()])
            try:
                response = self.requests.get(url, timeout=3)
                response.raise_for_status()  # Raise an exception for non-2xx status codes
                return True
            except Exception as e:
                self.logs.write_to_log(e)
                print(f'Alarm not sent for cam id: {guid} Exception: {e}')
                return False
        except Exception as e:
            self.logs.write_to_log(e)
            return False
