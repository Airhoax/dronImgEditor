import tkinter as tk
from tkinter import filedialog
import cv2 as cv
import pyautogui
import numpy as np
from imgFunctions import *


class Mouse:
    def __init__(self, mouseDownState, oldX, oldY):
        self.mouseDownState = mouseDownState
        self.oldX = oldX
        self.oldY = oldY

    def checkMouseDownState(self):
        if self.mouseDownState > 3:
            self.mouseDownState = 1


class Button:
    def __init__(self, minX, minY, maxX, maxY, buttonFunction):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        self.buttonFunction = buttonFunction


mouse = Mouse(1, 0, 0)
appImg = 1
buttons = []


def openImg():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("All Files", "*.*")))
    img = cv.imread(file_path)
    return img


def displayImg(img):
    screenWidth, screenHeight = pyautogui.size()
    screenHeight = round(screenHeight * (1 - 78/1080))

    display = 50 * np.ones(shape=[screenHeight, screenWidth, 3], dtype=np.uint8)

    zoomOut = cv.imread("C:/Users/ivanh/OneDrive/Desktop/Dorn/dronImgEditor/img/zoomOut.png")
    zoomIn = cv.imread("C:/Users/ivanh/OneDrive/Desktop/Dorn/dronImgEditor/img/zoomIn.png")

    display = newButton(screenWidth - 64, screenHeight - 64, screenWidth, screenHeight, 1, zoomOut, display)
    display = newButton(screenWidth - 64, screenHeight - 128, screenWidth, screenHeight - 64, 2, zoomIn, display)

    global appImg
    appImg = display

    cv.imshow("output", display)
    cv.setMouseCallback("output", clickOnApp)
    cv.waitKey(0)


def clickOnApp(event, x, y, flags, param):
    global mouse
    if event == cv.EVENT_LBUTTONDOWN:
        mouse.mouseDownState += 1
        mouse.checkMouseDownState()
        selectArea(x, y)


def selectArea(x, y):
    display = appImg.copy()
    action = buttonCheck(x, y)

    if action != 0:
        global mouse
        mouse.mouseDownState = 1
        selectButton(action)

    else:
        if mouse.mouseDownState == 3:
            cv.rectangle(display, (mouse.oldX, mouse.oldY), (x, y), (255, 0, 0), -1)

        elif mouse.mouseDownState == 2:
            cv.circle(display, (x, y), 10, (255, 0, 0), -1)
            mouse.oldX = x
            mouse.oldY = y

    Update(display)


def buttonCheck(x, y):
    if(len(buttons) > 0):
        for button in buttons:
            if x > button.minX and x < button.maxX and y > button.minY and y < button.maxY:
                return button.buttonFunction

    return 0


def newButton(minX, minY, maxX, maxY, buttonFunction, buttonImg, app):
    button = Button(minX, minY, maxX, maxY, buttonFunction)
    app[minY: maxY, minX: maxX] = buttonImg
    buttons.append(button)

    return app

def Update(display):
    cv.imshow("output", display)
    cv.waitKey(1)