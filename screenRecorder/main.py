import datetime

from PIL import ImageGrab
import numpy as np
import cv2
from win32api import GetSystemMetrics

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

timestamp = datetime.datetime.now().strftime('%Y-%m-%d- %H-%M-%S')
filename = f"{timestamp}.mp4"

#Encoding
fourcc = cv2.VideoWriter.fourcc('m','p','4','v')
captured_video = cv2.VideoWriter(filename,fourcc,20.0,(width,height))
webcam = cv2.VideoCapture(0)

while True:
    img = ImageGrab.grab(bbox=(0, 0, width, height))
    img_np = np.array(img)
    image_final = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    _,frame = webcam.read()
    fr_width, fr_height,_ = frame.shape
    image_final[0:fr_width, 0:fr_height, :] = frame[0:fr_width, 0:fr_height, :]
    cv2.imshow('Screen Recorder', image_final)
    captured_video.write(image_final)
    if cv2.waitKey(10) == ord('q'):
        break
