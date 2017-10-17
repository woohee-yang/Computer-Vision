import cv2
import sys
from enum import Enum

class Status(Enum) :
    INIT = 1
    CALC_HIST = 2
    TRACKING = 3

args = sys.argv
img = cv2.imread(args[-1])
cv2.namedWindow("lena", cv2.WINDOW_NORMAL)
cv2.imshow("lena", img)
cv2.waitKey(0)

class Rect :
    def __init__(self, x_init, y_init, width, height) :
        self.x = x_init
        self.y = y_init
        self.width = width
        self.height = height

    def __repr__(self) :
        return "".join(["Rect(", str(self.x), ",", str(self.y), ",", str(width), ",", str(height)")"])

origin = Rect(0,0,0,0)
selection = Rect(0,0,0,0)
blButtonDown = False
tracking = Status.INIT

def onMouse(mevent, x, y, flags, img) :
    if(blButtonDown) :
        selection_ptr[0] = min(x, origin_ptr[0])
