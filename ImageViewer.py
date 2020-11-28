# This Python file uses the following encoding: utf-8

import cv2
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class ImageViewer(QWidget):
    def __init__(self, parent = None):
        super(ImageViewer, self).__init__(parent)
        self.image = QImage()
        self.setAttribute(Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @Slot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("image null")

        self.image = image

        if image.size() != self.size():
           self.setFixedSize(image.size())

        self.update()
