import cv2 as cv
import numpy as np
import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter
import pydirectinput
from enum import Enum, auto
import pydirectinput
from tkinter import *
from time import sleep
import pyautogui
import keyboard
import os


class States(Enum):
    IDLE = auto()
    CAST = auto()
    HOOK = auto()
    REEL = auto()
    REPAIR = auto()
    BAIT = auto()
    REFOCUS = auto()


class Bot:
    def __init__(self) -> None:
        self.__state = States.REPAIR
        # self.__state = States.REFOCUS

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state


# initialize the WindowCapture class
wincap = WindowCapture('Windowed Projector (Preview)')

# initialize the Vision class
vision_click = Vision('images/click.png')
vision_level = Vision('images/fishhook.png')
vision_green = Vision('images/green.png')
vision_red = Vision('images/red.png')
vision_finished = Vision('images/f3.png')
vision_pole = Vision('images/pole.png')
vision_bait = Vision('images/bait.png')
vision_equip = Vision('images/equip.png')
vision_pointer = Vision('images/pointer.png')
vision_missed = Vision('images/missed.png')


# vision_limestone.init_control_gui()
hsv_filter = HsvFilter(0, 0, 13, 22, 107, 255, 0, 0, 0, 0)

finished = True
loop_time = time.time()
bot = Bot()
castcounter = 0
running = True
while(running):

    screenshot = wincap.get_screenshot()
    print('FPS {}; State:{}; Iteration: {}'.format(
        round(1 / (time.time() - loop_time), 1), bot.get_state(), castcounter), end='\r')
    loop_time = time.time()
    if bot.get_state() == States.IDLE:
        time.sleep(1)
        pydirectinput.keyDown("f3")
        time.sleep(1)
        bot.set_state(States.BAIT)
    elif bot.get_state() == States.CAST:
        pydirectinput.keyDown('b')
        rectangles = vision_click.find(screenshot, 0.7)
        if len(rectangles) > 0:
            pydirectinput.mouseDown(button="left")
            time.sleep(1.9)
            pydirectinput.mouseUp(button="left")
            castcounter += 1
            if castcounter > 50:
                bot.set_state(States.REPAIR)
                castcounter = 0
            else:
                bot.set_state(States.HOOK)
    elif bot.get_state() == States.HOOK:
        logging = vision_level.find(screenshot, 0.7)
        # # rectangles.append(logging)
        if len(logging) > 0:
            pydirectinput.mouseDown(button="left")
            pydirectinput.mouseUp(button="left")
            bot.set_state(States.REEL)
    elif bot.get_state() == States.REEL:
        green = vision_green.find(screenshot, 0.6)
        red = vision_red.find(screenshot, 0.6)
        finished = vision_finished.find(screenshot, 0.7)
        if len(green) > 0:
            pydirectinput.mouseDown(button="left")
        elif len(red) > 0:
            pydirectinput.mouseUp(button="left")
        elif len(finished) > 0:
            pydirectinput.mouseUp(button="left")
            time.sleep(1)
            bot.set_state(States.REFOCUS)
    elif bot.get_state() == States.REPAIR:
        time.sleep(1)

        pydirectinput.keyDown("tab")
        time.sleep(1)

        pole = vision_pole.find(screenshot, 0.5)
        # print(pole)
        if len(pole) > 0:
            pydirectinput.moveTo(pole[0][0] - 5,
                                 pole[0][1] + 50)
            time.sleep(1)

            pydirectinput.keyDown("r")
            pydirectinput.mouseDown(button="left")
            time.sleep(0.1)
            pydirectinput.mouseUp(button="left")

            time.sleep(0.4)

            pydirectinput.keyDown("e")

            time.sleep(0.1)
            pydirectinput.keyUp("tab")

            pydirectinput.keyDown("tab")
            time.sleep(0.1)

            pydirectinput.keyUp("e")

            pydirectinput.keyUp("r")
            bot.set_state(States.IDLE)
    elif bot.get_state() == States.BAIT:
        pydirectinput.keyDown('r')
        time.sleep(1)

        bait = vision_bait.find(screenshot, 0.7)
        equip = vision_equip.find(screenshot, 0.7)

        time.sleep(1)

        if len(bait) > 0 and len(equip) > 0:
            # print("found bait and equoü")

            pydirectinput.moveTo(bait[0][0] + 15,
                                 bait[0][1] + 40)

            time.sleep(1)

            pydirectinput.mouseDown(button="left")
            time.sleep(0.1)
            pydirectinput.mouseUp(button="left")
            time.sleep(0.1)

            pydirectinput.moveTo(equip[0][0] + 35,
                                 equip[0][1] + 50)
            time.sleep(1)

            pydirectinput.mouseDown(button="left")
            time.sleep(0.1)
            pydirectinput.mouseUp(button="left")
            time.sleep(2)
            pydirectinput.keyUp('r')

            bot.set_state(States.CAST)
    elif bot.get_state() == States.REFOCUS:
        pydirectinput.keyUp('b')

        bot.set_state(States.CAST)

    # elif finished:
    #     pass

    # logging = vision_level.find(screenshot, 0.6)
    # # rectangles.append(logging)
    # if len(logging) > 0:
    #     pydirectinput.mouseDown(button="left")
    #     pydirectinput.mouseUp(button="left")

    #     finished = True

    # # cv.imshow("Processed", processed_image)

    # # debug the loop rate

    # # press 'q' with the output window focused to exit.
    # # waits 1 ms every loop to process key presses

    #     cv.destroyAllWindows()
    #     break
    # elif key == ord('f'):
    #     cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    # elif key == ord('d'):
    #     cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)
