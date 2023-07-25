import cv2
import time
import numpy as np

#Initialize the camera

camera = cv2.VideoCapture(0)

while True:

    lower_red = np.array([160, 100, 20])
    higher_red = np.array([179, 255, 255])
    res, frame = camera.read()
    if res:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(hsv,lower_red, higher_red)
        result = cv2.bitwise_and(frame, frame, mask=color_mask)

        # cv2.imshow('Camera_output', frame)
        # cv2.imshow('hsv', hsv)
        cv2.imshow('color mask', color_mask)
        cv2.imshow('Final Result', result)

    if cv2.waitKey(1) == 27:
        break


