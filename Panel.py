# This Python file uses the following encoding: utf-8

import cv2
import numpy as np
from collections import deque
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

que = deque(maxlen=512)
color_que = deque(maxlen=512)

class Panel(QObject):
    width = 400
    height = 400

    ImageSignal = Signal(QImage)
    colorIdx = 0

    def __init__(self, parent = None):
        super(Panel, self).__init__(parent)

    @Slot()
    def changeRed(self):
        self.colorIdx = 0

    @Slot()
    def changeGreen(self):
        self.colorIdx = 1
        print('ad')
    @Slot()
    def changeBlue(self):
        self.colorIdx = 2

    @Slot(tuple)
    def draw(self, center):
        global image
        global color
        global que
        global color_que

        image = np.full((self.width, self.height, 3), 255, np.uint8)

        print(self.colorIdx)

        que.append(center)
        color_que.append(self.colorIdx)


        start = ()
        end = ()

        for i in range(len(que)):
            start = end
            end = que[i]
            #cv2.circle(color_frame, (end[0], end[1]), 1, (0, 255, 255), 3)
            if start != () and end != ():

                if color_que[i] == 0:
                    color = (255, 0, 0)
                elif color_que[i] == 1:
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)

                cv2.line(image, start, end, color, 2)
                #print(start, end)

        cv2.circle(image, center, 5, color, 1)

        qt_image = QImage(image.data,
            self.width,
            self.height,
            image.strides[0],
            QImage.Format_RGB888)

        self.ImageSignal.emit(qt_image)
