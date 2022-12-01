import tkinter as tk
from tkinter import filedialog
import cv2 as cv

def openImg():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=(("png", "*.png"), ("jpg", "*.jpg"), ("All Files", "*.*")))
    return cv.imread(file_path)