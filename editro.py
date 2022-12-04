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


class AppImg:
    def __init__(self, img, minX, maxX, minY, maxY):
        self.img = img
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY



mouse = Mouse(1, 0, 0)
appImg = AppImg(1, 1, 1, 1, 1)
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

    img, screenX, screenY = fitScreenImg(img, display, True, screenWidth, screenHeight)

    global appImg
    appImg.img = display
    appImg.minX = round((display.shape[1] - screenX) / 2)
    appImg.maxX = appImg.minX + screenX
    appImg.minY = round((display.shape[0] - screenY) / 2)
    appImg.maxY = appImg.minY + screenY

    cv.imshow("output", display)
    cv.setMouseCallback("output", clickOnApp)
    cv.waitKey(0)


def clickOnApp(event, x, y, flags, param):
    global mouse
    if event == cv.EVENT_LBUTTONDOWN:
        mouse.mouseDownState += 1
        mouse.checkMouseDownState()
        selectAction(x, y)


def selectAction(x, y):
    if x < appImg.minX:
        x = appImg.minX
    elif x > appImg.maxX:
        x = appImg.maxX

    if y < appImg.minY:
        y = appImg.minY
    elif y > appImg.maxY:
        y = appImg.maxY

    display = appImg.img.copy()
    actionButton = buttonCheck(x, y)

    if actionButton != 0:
        global mouse
        mouse.mouseDownState = 1
        selectButton(actionButton)

    else:
        display = selectArea(display, x, y)

    Update(display)


def selectArea(display, x, y):
    if mouse.mouseDownState == 3:
        cv.rectangle(display, (mouse.oldX, mouse.oldY), (x, y), (255, 0, 0), -1)

    elif mouse.mouseDownState == 2:
        cv.circle(display, (x, y), 10, (255, 0, 0), -1)
        mouse.oldX = x
        mouse.oldY = y

    return display

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