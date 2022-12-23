import cv2 as cv
import pyautogui


class Image:
    def __init__(self, originalImg, displayed):
        self.originalImg = originalImg
        self.displayed = displayed


image = 1


def selectButton(action, display):
    if action == 1:
        print("zoom out")
    elif action == 2:
        display = zoomIn(display)

    return display


def fitScreenImg(img, display, original, x, y):
    if original:
        global image
        image = Image(img, 1)

    if img.shape[1] / img.shape[0] < 1.1:
        imgSizeY = (round(y * 0.70))
        minY = round((display.shape[0] - imgSizeY) / 2)
        maxY = minY + imgSizeY

        imgSizeX = (round(y * 0.70))
        minX = round((display.shape[1] - imgSizeX) / 2)
        maxX = minX + imgSizeX

    else:
        imgSizeX = (round(x * 0.70))
        minX = round((display.shape[1] - imgSizeX) / 2)
        maxX = minX + imgSizeX

        imgSizeY = (round(y * (imgSizeX / x)))
        minY = round((display.shape[0] - imgSizeY) / 2)
        maxY = minY + imgSizeY


    img = cv.resize(img, (imgSizeX, imgSizeY))
    image.displayed = img
    display[minY: maxY, minX: maxX] = img

    return [display, imgSizeX, imgSizeY]


def zoomIn(display):
    global image
    img = image.displayed
    displayImg = img[round(img.shape[1]*0.05): round(img.shape[1]*0.95), round(img.shape[0]*0.05): round(img.shape[0]*0.95)]
    screenWidth, screenHeight = pyautogui.size()
    screenHeight = round(screenHeight * (1 - 78 / 1080))
    return fitScreenImg(displayImg, display, False, screenWidth, screenHeight)[0]
    #return display