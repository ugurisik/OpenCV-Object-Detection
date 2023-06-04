import time
import cv2
import torch
import numpy as np
import math
import pyshine as ps
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from unidecode import unidecode
import requestclient
import os
import asyncio
import logs
from ultralytics import YOLO
os.environ["OPENCV_LOG_LEVEL"] = "SILENT"


class Process:
    def __init__(self, guid, value, screen_shot_path, alerts_path, weight_path, api_url, model=None, defModel=False):
        self.guid = guid
        self.screen_shot_path = screen_shot_path
        self.alerts_path = alerts_path
        self.weight_path = weight_path
        self.api_url = api_url

        self.name = value['name']
        self.url = value['url']
        self.zone = value['zone']
        self.detection = value['detection']
        self.alarm_sending_time = value['alarm_sending_time']

        self.time = time
        self.cv2 = cv2
        self.torch = torch
        self.np = np
        self.math = math
        self.ps = ps
        self.Point = Point
        self.Polygon = Polygon
        self.unidecode = unidecode
        self.Requests = requestclient.RequestClient()
        self.asyncio = asyncio
        self.logs = logs.Logs('log.txt')

        self.last_alerts = {
            0: self.time.strftime(
                '%Y-%m-%d %H:%M:%S', self.time.localtime(time.time() - 10))
        }

        if defModel is False:
            # self.cv2.logLevel = 'SILENT'
            # self.model = self.torch.hub.load(
            #     'ultralytics/yolov5', 'custom', f'{self.weight_path}{model}')
            # self.device = 'cuda' if self.torch.cuda.is_available() else 'cpu'
            # self.model.to(self.device)
            # if self.torch.cuda.is_available():
            #     self.torch.cuda.synchronize()
            model = YOLO(f'{self.weight_path}{model}')
            self.model = model
        else:
            self.model = model

        self.cap = self.cv2.VideoCapture(self.url)
        self.video_width = int(self.cap.get(self.cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(self.cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.cap.get(self.cv2.CAP_PROP_FPS))

        self.labels = self.model.names
        self.polygons = self.zone

        for i in range(len(self.polygons)):
            x = self.polygons[i][0]
            y = self.polygons[i][1]
            xper = (x*self.video_width/100)
            yper = (y*self.video_height/100)
            self.polygons[i] = (self.math.ceil(xper), self.math.ceil(yper))

        self.polygon_converted = self.Polygon(self.polygons)

        self.counter = 0

    def run(self):
        # try:
            
        # except Exception as e:
        #     self.logs.write_to_log(f'GUID: {self.guid} Error: {e}')
        print(
            f"Process.run() is running... {self.guid} {self.screen_shot_path} {self.alerts_path}")
        loop = asyncio.new_event_loop()
        self.asyncio.set_event_loop(loop)
        loop.run_until_complete(self.CameraProcess())
        loop.close()
        
    def TakeScreenShot(self, frame, alarm_type, detections):
        print('------------------------------------------------------------------')
        print(f'Alarm Taken! Guid: {self.guid} Alarm Type: {alarm_type}')
        print('------------------------------------------------------------------')
        if alarm_type != 0:
            name = f"{self.alerts_path}/{self.guid}_{self.time.strftime('%Y%m%d-%H-%M-%S')}.jpg"
        else:
            name = f"{self.screen_shot_path}/{self.guid}_{self.time.strftime('%Y%m%d-%H-%M-%S')}.jpg"
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, 75]
        self.cv2.imwrite(name, frame, compression_params)
        alarm_times = 0
        if self.last_alerts.get(str(alarm_type)) is None:
            alarm_times = 0
            send_alert = True
        else:
            alarm_times = self.alarm_sending_time 
            if self.time.strftime('%Y-%m-%d %H:%M:%S', self.time.localtime(time.time() - alarm_times)) >= self.last_alerts.get(str(alarm_type)):
                send_alert = True
            else:
                send_alert = False

        if send_alert:
            detectionString = ''
            for detect in detections:
                if detections.get(detect) > 0:
                    detectionString += f'{detections.get(detect)} {detect}|'

            detectionString = detectionString[:-1]
            self.Requests.SendAlert(
                self.guid, name, alarm_type, detectionString)
            self.last_alerts[str(alarm_type)] = self.time.strftime(
                '%Y-%m-%d %H:%M:%S')

    def TakeOneScreenShot(self, frame,detections):
        detectionString = ''
        for detect in detections:
            if detections.get(detect) > 0:
                detectionString += f'{detections.get(detect)} {detect}|'

        detectionString = detectionString[:-1]
        name = f"{self.screen_shot_path}/{self.guid}.jpg"
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, 75]
        self.cv2.imwrite(name, frame, compression_params)
        with open(f"{self.screen_shot_path}/{self.guid}.txt", "w") as f:
            f.write(detectionString)

        img=self.cv2.imread(f"{self.screen_shot_path}/{self.guid}.jpg")
        thumb = self.cv2.resize(img, None,fx = 0.2, fy = 0.2)
        self.cv2.imwrite(f"{self.screen_shot_path}/thumb/{self.guid}.jpg", thumb, compression_params)

        print(f'One ScreenShot Taken! Guid: {self.guid}')

    def DrawRectWithText(self, image, label, x, y, width, height, confidence=0.0):
        confidence = round(confidence, 2)
        self.cv2.rectangle(image, (x, y), (width, height), (0, 0, 255), 2)

        font = self.cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 2

        (text_width, text_height), _ = self.cv2.getTextSize(
            label+str(confidence)+"  ", font, font_scale, font_thickness)
        text_x = x
        text_y = y-10 if y >= 20 else y+height+30

        self.cv2.rectangle(image, (x, text_y+5), (x+text_width,
                           text_y-text_height-5), (0, 0, 255), -1)
        self.cv2.putText(image, f'{label} {confidence}', (text_x, text_y), font,
                         font_scale, (0, 0, 0), font_thickness, self.cv2.LINE_AA)

    async def ReConnect(self):
        await self.asyncio.sleep(0.1)
        self.cap.release()
        cap = self.cv2.VideoCapture(self.url)
        if not cap.isOpened():
            print(f'Camera is not available... 10 Sec Waiting and Restarting... Guid: {self.guid}')
            await self.asyncio.sleep(10)
            self.ReConnect()
        else:
            return cap
    

    async def CameraStuff(self, cap):
        while True:
            # time.sleep(0.1)
            self.counter += 1
            detectionCount = {}
            for detect in self.detection:
                clss = detect['class']
                detectionCount[str(clss)] = 0
            ret, frame = cap.read()
            if not ret:
                print(
                    f"Camera is not available... Restarting... Guid: {self.guid}")
                return False
            else:
                if self.counter % int(self.fps) == 0:
                    alarm_type = 0
                    in_zone = False
                    results = self.model.predict(frame,verbose=False)
                    # results = self.model(frame)
                    self.cv2.polylines(frame, np.array(
                        [self.polygons]), True, (0, 0, 255), 2)
                    self.ps.putBText(frame, 'SecuritEye is watching!', 10,
                                     10, 10, 10, 0.7, (0, 200, 200), (250, 250, 250), 2)
                    self.ps.putBText(frame, self.time.strftime('%Y/%m/%d-%H:%M:%S'), 10,
                                     50, 10, 10, 0.7, (0, 200, 200), (250, 250, 250), 2)
                    result = results[0]

                    

                    if len(result.boxes) > 0:
                        box = result.boxes[0]

                        # for boxes in box.xyxy:
                        #     print(f'Boxes: {boxes}')
                        for box in result.boxes:
                            class_id = box.cls[0].item()
                            class_name = result.names[box.cls[0].item()]
                            cords = box.xyxy[0].tolist()
                            cords = [round(x) for x in cords]
                            conf = round(box.conf[0].item(), 2)
                            x1,y1,x2,y2 = cords
                            # print(f'x1: {x1} y1: {y1} x2: {x2} y2: {y2}')


                            width = x2-x1
                            height = y2-y1
                            center = [x1+(width/2), y1+(height/2)]
                            max_border = max(width, height)
                            left = max(int(center[0]-(max_border/2)), 0)
                            right = max(int(center[0]+(max_border/2)), 0)
                            top = max(int(center[1]-(max_border/2)), 0)
                            bottom = max(int(center[1]+(max_border/2)), 0)

                            

                            for detect in self.detection:
                                confi = detect['confidence']
                                clss = detect['class']
                                # detectionCount[str(clss)] = detectionCount.get(str(
                                #             clss)) + 1
                                # self.DrawRectWithText(frame, class_name, left, top, right, bottom, conf)
                                # self.TakeOneScreenShot(frame,detectionCount)
                                if class_name == clss and conf >= confi:
                                    if self.polygon_converted.is_empty:
                                        in_zone = True
                                    else:
                                        center = (
                                            int(center[0]), int(center[1]))
                                        poly = np.array(
                                            self.polygons, dtype=np.int32)
                                        is_inside = self.cv2.pointPolygonTest(
                                            poly, center, False)
                                        print(f'is_inside {is_inside}')

                                        if is_inside == 1.0:
                                            in_zone = True
                                        else:
                                            in_zone = False

                                    if in_zone:
                                        detectionCount[str(clss)] = detectionCount.get(str(
                                            clss)) + 1
                                        alarm_type = class_name
                                        self.DrawRectWithText(frame, class_name, left, top, right, bottom, conf)

                    if in_zone:
                        self.TakeScreenShot(
                            frame, alarm_type, detectionCount)
                    if self.counter % int(self.fps*2) == 0:
                        # self.cv2.polylines(frame, np.array(
                        # [self.polygons]), True, (0, 0, 255), 2)
                        # self.ps.putBText(frame, 'SecuritEye is wathing!', 10,
                        #                         10, 10, 10, 0.7, (0, 250, 250), (250, 250, 250), 2)
                        # self.ps.putBText(frame, self.time.strftime('%Y/%m/%d-%H:%M:%S'), 10,
                        #                         50, 10, 10, 0.7, (0, 200, 200), (250, 250, 250), 2)
                        self.TakeOneScreenShot(frame,detectionCount)
            await self.asyncio.sleep(0)

    async def CameraProcess(self):
        while True:
            self.cap = self.cv2.VideoCapture(self.url)
            
            if self.cap.isOpened():
                response = await self.CameraStuff(self.cap)
                if response == False:
                    self.cap = await self.ReConnect()
                    continue
            else:
                self.cap = self.ReConnect()
                continue
            await self.asyncio.sleep(0)