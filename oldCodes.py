# v8main.py

# DefaultModel = 'best-5.pt'
# model = torch.hub.load('ultralytics/yolov5', 'custom',
#                        f'{WeightPath}{DefaultModel}')
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# model.to(device)
# if torch.cuda.is_available():
#     torch.cuda.synchronize()

# model = YOLO(f'{WeightPath}{DefaultModel}')


# port = 8080


# def DeleteFiles():
#     shutil.rmtree(ScreenShotPath)

#     for file in os.listdir(AlertsPath):
#         os.remove(os.path.join(AlertsPath, file))


# def Port():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     result = sock.connect_ex(('localhost', port))
#     if result == 0:
#         print(f"Port {port} is already open.")
#     else:
#         print(f"Port {port} is closed. Opening the port...")
#         try:
#             subprocess.Popen(['python3', '-m', 'http.server', str(port)])
#             print(f"Port {port} is now open.")
#         except Exception as e:
#             print(f"Failed to open port {port}: {e}")

# DeleteFiles()
# Port()


# cameraList = {
#     '5': {
#         'name': 'Vorderseite',
#         'url': 'rtsp://admin:W9bz7rza!@192.168.163.5:554',
#         'zones': {
#             '1': [(100, 86.55555), (75.875, 44.55555), (22.5625, 41.44444), (0, 80.0), (0, 100), (100, 100)],
#         },
#         'detection': [
#             {
#                 'class': 'forklift',
#                 'confidence': 0.6,
#             },
#             {
#                 'class': 'forklift',
#                 'confidence': 0.6,
#             },
#             {
#                 'class': 'ameise',
#                 'confidence': 0.6,
#             }
#         ],

#         'alarm_sending_time': 180,
#     },
#     '23': {
#         'name': 'k.A',
#         'url': 'rtsp://admin:W9bz7rza!@192.168.163.23:554',
#         'zones': {},
#         'detection': [
#             {
#                 'class': 'person',
#                 'confidence': 0.61,
#             },
#             {
#                 'class': 'forklift',
#                 'confidence': 0.6,
#             },
#             {
#                 'class': 'ameise',
#                 'confidence': 0.6,
#             }
#         ],

#         'alarm_sending_time': 180,
#     },
#     '26': {
#         'name': 'Raucherbereich',
#         'url': 'rtsp://admin:W9bz7rza!@192.168.163.26:554',
#         'zones': {
#             '1': [(0, 0), (50.375, 0), (50.6875, 47.22222), (44.625, 46.44444), (38.5625, 53.44444), (40.0625, 82.0), (38.6875, 85.88888), (59.3125, 89.77777), (59.875, 86.0), (62.9375, 79.77777), (63.5625, 49.33333), (50.875, 47.22222), (50.4375, 0), (99.75, 0), (100, 100), (0, 100)],
#         },
#         'detection': [
#             {
#                 'class': 'CgOnFace',
#                 'confidence': 0.6,
#             },
#             {
#                 'class': 'person',
#                 'confidence': 0.61,
#             }
#         ],

#         'alarm_sending_time': 180,
#     },
#     '31': {
#         'name': 'Forklift Test',
#         'url': 'rtsp://admin:W9bz7rza!@192.168.163.31:554',
#         'zones': {},
#         'detection': [
#             {
#                 'class': 'person',
#                 'confidence': 0.61,
#             },
#             {
#                 'class': 'forklift',
#                 'confidence': 0.6,
#             },
#             {
#                 'class': 'ameise',
#                 'confidence': 0.6,
#             }
#         ],

#         'alarm_sending_time': 180,
#     },
#     '21': {
#         'name': 'Forklift Test',
#         'url': 'rtsp://admin:W9bz7rza!@192.168.163.21:554',
#         'zones': {},
#         'detection': [
#             {
#                 'class': 'person',
#                 'confidence': 0.61,
#             },
#             {
#                 'class': 'forklift',
#                 'confidence': 0.6,
#             },
#             {
#                 'class': 'ameise',
#                 'confidence': 0.6,
#             }
#         ],

#         'alarm_sending_time': 180,
#     }
# }

# '1': {
#     'name': 'Bahçe',
#     'url': 0,
#     'zone': [(0, 0), (0, 50), (50, 50), (50, 0)],
#     'zones': {
#         '1': [(50, 50), (50, 100), (100, 100), (100, 50)],
#         '2': [(0, 0), (0, 49), (49, 49), (49, 0)]
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


"""
OLD CODES FROM PROCESS2.PY
"""

# if defModel is False:
#     # self.cv2.logLevel = 'SILENT'
#     # self.model = self.torch.hub.load(
#     #     'ultralytics/yolov5', 'custom', f'{self.weight_path}{model}')
#     # self.device = 'cuda' if self.torch.cuda.is_available() else 'cpu'
#     # self.model.to(self.device)
#     # if self.torch.cuda.is_available():
#     #     self.torch.cuda.synchronize()
#     model = YOLO(f'{self.weight_path}{model}')
#     self.model = model
# else:
#     self.model = model

# for i in range(len(self.polygons)):
#     x = self.polygons[i][0]
#     y = self.polygons[i][1]
#     xper = (x*self.video_width/100)
#     yper = (y*self.video_height/100)
#     self.polygons[i] = (self.math.ceil(xper), self.math.ceil(yper))

# self.polygon_converted = self.Polygon(self.polygons)


# polygon_converted = self.Polygon(coordinates)
# cv2.imwrite(name, thresholded_area_inside)
# img = self.cv2.imread(
#     f"{self.screen_shot_path}/{self.guid}.jpg")
# self.cv2.imwrite(name, img)

# if self.polygon_converted.is_empty:
#     in_zone = True
# else:
#     center = (
#         int(center[0]), int(center[1]))
#     poly = np.array(
#         self.polygons, dtype=np.int32)
#     is_inside = self.cv2.pointPolygonTest(
#         poly, center, False)
#     print(f'is_inside {is_inside}')

#     if is_inside == 1.0:
#         in_zone = True
#     else:
#         in_zone = False
#                            self.DrawRectWithText(frame, class_name, left, top, right, bottom, conf, color)

# response = requests.get(
#     'https://securiteye.ai/API/Camera/CameraList.php?camlist=kayseri2023')
# if response.status_code == 200:
#     global cameraList
#     cameraList = response.json()
#     print(cameraList)
# else:
#     print('Error: ', response.status_code)
# time.sleep(10)
# get jsonFile
