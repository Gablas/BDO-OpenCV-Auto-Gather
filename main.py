import pyautogui as pyag
import pydirectinput as pydi
import time
import cv2 as cv
import numpy as np
from screengrab import cap
import threading

cascade = cv.CascadeClassifier('cascade/cascade.xml')


def draw_rectangles(haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

def draw_template_match(img, res):
    h, w, _ = healthbar.shape
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    return cv.rectangle(img,top_left, bottom_right, 255, 2)

def get_click_points(rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = (x + int(w/2)) * 2
            center_y = (y + int(h/2)) * 2
            # Save the points
            points.append((center_x, center_y))

        return points

def gather():
    print("Going to gather")
    time.sleep(4)
    loop_amount = 3
    collected = False
    for i in range(loop_amount):
        if(collected):
            break
        res = pyag.locateOnScreen("./needles/gather.png", confidence=0.5)
        if(res):
            print("Gathering")
            pydi.press("r")
            pydi.press("r")
            pydi.press("r")
            for j in range(5):
                if(pyag.locateOnScreen("./needles/getall.png", confidence=0.75)):
                    print("Collecting")
                    pydi.press("r")
                    pydi.press("r")
                    pydi.press("r")
                    collected = True
                    break;

def smooth_mouse(point, steps):
    for i in range(steps):
        pydi.moveTo(point[0]+(steps-i), point[1]+(steps-i))

def smooth_mouse_rel(point,steps):
    for i in range(steps):
        pydi.moveRel(point[0]//(steps), point[1]//(steps))

def show_rectangles(screenshot, rectangles):
    recs = draw_rectangles(screenshot, rectangles)

    # display the images
    cv.imshow('Matches', recs)

    cv.waitKey(1)

def save_every_image(image):
    cv.imwrite("./debug/"+str(time.time())+".jpg",image)


gather_amount = 0

while(True):
    # get an updated image of the game
    #screenshot = pyag.screenshot("screennow.png")
    #cap("screennow.png")

    #screenshot = cv.imread("screennow.png")

    if(gather_amount == -1):
        pydi.press("2")

    screenshot = pyag.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    screenshot = cv.resize(screenshot, (screenshot.shape[1]//2, screenshot.shape[0]//2))

    threading.Thread(target=save_every_image, args=(screenshot,)).start()

    rectangles = cascade.detectMultiScale(screenshot, 1.1)

    show_rectangles(screenshot, rectangles)

    click_points = get_click_points(rectangles)

    print(len(click_points))

    gathered = False

    for point in click_points:
        if gathered:
            break
        print("searching after kuku")
        smooth_mouse(point, 3)
        x_mp, y_mp = pyag.position()
        try:
            for i in range(2):
                #pyag.screenshot("mousecheck.png", region=(x_mp-200, y_mp-200, 300, 300))
                res = pyag.locateOnScreen("./needles/health.png", region=(x_mp-200, y_mp-200, 300, 300), confidence=0.6)
                if(res):
                    print("Found kuku")
                    pydi.click(duration=.5)
                    gather()
                    gathered = True
                    gather_amount += 1
                    break
        except:
            print("Don't do that again!")

            
        
    print("Turning around")
    pydi.press("ctrl")
    time.sleep(.5)
    smooth_mouse_rel((5000,0), 10)
    time.sleep(.5)
    pydi.press("ctrl")