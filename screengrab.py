from mss import mss
import numpy as np
import cv2 as cv
import time
import cv2 as cv
import pyautogui as pyag

sct = mss()

def capture_model_pics():
    while(True):
        time.sleep(0.5)
        sct.shot(output="./debug/"+str(time.time())+".jpg")


def cap(filename):
    sct.shot(output=filename)


def record():
    while(True):
        screenshot = pyag.screenshot()
        screenshot = np.array(screenshot)
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

        cv.imshow("frame", screenshot)

        cv.waitKey(1)
