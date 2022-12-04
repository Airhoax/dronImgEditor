import cv2 as cv

class Image:
    def __init__(self, originalImg):
        self.originalImg = originalImg


image = 1


def selectButton(action):
    if action == 1:
        print("zoom out")
    elif action == 2:
        print("zoom in")

def fitScreenImg(img, display, original, x, y):
    if original:
        global image
        image = Image(img)

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
    display[minY: maxY, minX: maxX] = img

    return display