import tkinter as tk
from tkinter import filedialog
import cv2 as cv
import pyautogui
import numpy as np

def openImg():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("All Files", "*.*")))
    return cv.imread(file_path)

def displayImg(img):
    screenWidth, screenHeight = pyautogui.size()
    display = 0 * np.ones(shape=[screenHeight, screenWidth, 3], dtype=np.uint8)

    cv.imshow("output", display)
    cv.waitKey(0)