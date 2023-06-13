import math
import cv2
import numpy as np
import time
import requests


uri = 'kapivepalet.mp4'
requestLink = 'https://safari.imeryazilim.com/pos/test'
image_name = ''
points = []  # Polygonun köşelerini tutacak bir liste
polygons = []
original_width = None
original_height = None


def SendToSystem():
    params = {
        'uri': uri,
        'image_name': image_name,
        'points': str(points)
    }
    try:
        response = requests.post(requestLink, data=params, timeout=10, files={
                                 'image': open(image_name, 'rb')})
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        print(response.text)
        return True
    except requests.exceptions.RequestException as e:
        return False


def mouse_callback(event, x, y, flags, param):
    global original_width, original_height
    if event == cv2.EVENT_LBUTTONDOWN:
        # Noktaların orijinal boyuta göre ayarlanması
        scaled_x = x * (original_width / frame.shape[1])
        scaled_y = y * (original_height / frame.shape[0])
        x_per = x / original_width * 100
        y_per = y / original_height * 100
        # x_per and y_per max 5 digit
        x_per = math.floor(x_per * 100000) / 100000
        y_per = math.floor(y_per * 100000) / 100000
        points.append((x_per, y_per))
        polygons.append((scaled_x, scaled_y))
    if event == cv2.EVENT_RBUTTONDOWN:
        # delete last point
        points.pop()
        polygons.pop()


video_capture = cv2.VideoCapture(uri)
original_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
original_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

cv2.namedWindow('Video')
cv2.setMouseCallback('Video', mouse_callback)

while True:
    ret, frame = video_capture.read()
    if len(polygons) >= 2:
        pts = np.array(polygons, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], isClosed=True, color=(
            0, 255, 0), thickness=2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        name = time.strftime("%Y%m%d-%H_%M_%S")+".jpg"
        image_name = name
        cv2.imwrite(image_name, frame)
        print(points)
        # SendToSystem()

video_capture.release()
cv2.destroyAllWindows()


# import math
# import cv2
# import numpy as np
# import time
# import requests


# uri = './2222.jpeg'
# requestLink = 'https://safari.imeryazilim.com/pos/test'
# image_name = ''
# points = []  # Polygonun köşelerini tutacak bir liste
# polygons = []
# original_width = None
# original_height = None


# def SendToSystem():
#     params = {
#         'uri': uri,
#         'image_name': image_name,
#         'points': str(points)
#     }
#     try:
#         response = requests.post(requestLink, data=params, timeout=10, files={
#                                  'image': open(image_name, 'rb')})
#         response.raise_for_status()  # Raise an exception for non-2xx status codes
#         print(response.text)
#         return True
#     except requests.exceptions.RequestException as e:
#         return False


# def mouse_callback(event, x, y, flags, param):
#     global original_width, original_height
#     if event == cv2.EVENT_LBUTTONDOWN:
#         # Noktaların orijinal boyuta göre ayarlanması
#         scaled_x = x * (original_width / frame.shape[1])
#         scaled_y = y * (original_height / frame.shape[0])
#         x_per = x / original_width * 100
#         y_per = y / original_height * 100
#         # x_per and y_per max 5 digit
#         x_per = math.floor(x_per * 100000) / 100000
#         y_per = math.floor(y_per * 100000) / 100000
#         points.append((x_per, y_per))
#         polygons.append((scaled_x, scaled_y))
#     if event == cv2.EVENT_RBUTTONDOWN:
#         # delete last point
#         points.pop()
#         polygons.pop()


# video_capture = cv2.VideoCapture(uri)
# video_capture = cv2.imread(uri)
# original_width = video_capture.shape[1]
# original_height = video_capture.shape[0]


# # original_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
# # original_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)


# cv2.namedWindow('Video')
# cv2.setMouseCallback('Video', mouse_callback)

# while True:
#     frame = video_capture
#     if len(polygons) >= 2:
#         pts = np.array(polygons, np.int32)
#         pts = pts.reshape((-1, 1, 2))
#         cv2.polylines(frame, [pts], isClosed=True, color=(
#             0, 255, 0), thickness=2)

#     cv2.imshow('Video', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         name = time.strftime("%Y%m%d-%H_%M_%S")+".jpg"
#         image_name = name
#         cv2.imwrite(image_name, frame)
#         print(points)
#         # SendToSystem()

# video_capture.release()
# cv2.destroyAllWindows()
