# import numpy as np
# import cv2
# from numpy import *
# import math
# from shapely.geometry import Polygon

# video = cv2.VideoCapture('rtsp://88.248.145.53:3839/media/video1')
# # video = cv2.imread('20230606-17_24_48.jpg')
# video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# video_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
# video_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))


# # FOTOĞRAFTA BUNU AÇ
# # video_width = int(video.shape[1])
# # video_height = int(video.shape[0])

# alan_koordinatlari = array([(58.98437, 5.69444), (58.82812, 10.69444), (73.35937, 12.91666), (73.35937, 8.19444)],
#                            int32)
# for i in range(len(alan_koordinatlari)):
#     x = alan_koordinatlari[i][0]
#     y = alan_koordinatlari[i][1]
#     xper = (x*video_width/100)
#     yper = (y*video_height/100)
#     alan_koordinatlari[i] = (math.ceil(xper), math.ceil(yper))

# polygon_converted = Polygon(alan_koordinatlari)


# while True:
#     ret, frame_next = video.read()
#     # if not ret:
#     #     break,
#     # Fotoğrafta Aç
#     # frame_next = video
#     isClosed = True
#     color = (0, 255, 0)
#     thickness = 2
#     poly = array(alan_koordinatlari, dtype=int32)
#     cv2.polylines(frame_next, [poly],
#                   isClosed, color, thickness)
#     mask = zeros(frame_next.shape[:2], dtype=uint8)
#     cv2.fillPoly(mask, [poly], (255))
#     area_inside = cv2.bitwise_and(frame_next, frame_next, mask=mask)
#     area_inside_gray = cv2.cvtColor(area_inside, cv2.COLOR_BGR2GRAY)
#     _, thresholded_area_inside = cv2.threshold(
#         area_inside_gray, 90, 255, cv2.THRESH_BINARY)

#     TotalPx = thresholded_area_inside.shape[0] * \
#         thresholded_area_inside.shape[1]
#     whitePX = cv2.countNonZero(thresholded_area_inside)
#     blackPx = TotalPx - whitePX
#     tt = (blackPx / whitePX)
#     print("Alan içindeki beyaz piksel sayısı:", whitePX)
#     print("Alan içindeki siyah piksel sayısı:", blackPx)
#     print("Siyah-Beyaz Oranı:", tt)
#     frame_bw = cv2.cvtColor(frame_next, cv2.COLOR_BGR2GRAY)
#     area_values = thresholded_area_inside[nonzero(thresholded_area_inside)]
#     cv2.imwrite("alan.png", thresholded_area_inside)

#     cv2.imshow("Video", frame_next)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
cap = cv2.VideoCapture('rtsp://admin:safarimedia.de@88.248.145.53:3838')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2()

while (1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    gmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame', fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
