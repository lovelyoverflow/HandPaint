import cv2
import numpy as np
from collections import deque
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

blueLower = np.array([100, 60, 60])
blueUpper = np.array([140, 255, 255])

kernel = np.ones((5, 5), np.uint8)

que = deque(maxlen=512)


class ShowVideo(QObject):
    camera = cv2.VideoCapture(0, cv2.CAP_V4L)

    ret, image = camera.read()
    #height, width = image.shape[:2]
    width = 400
    height = 400

    VideoSignal = Signal(QImage)
    changeImage = Signal(tuple)

    def __init__(self, parent = None):
        super(ShowVideo, self).__init__(parent)

    @Slot()
    def startVideo(self):
        global image
        global que

        run_video = True

        while run_video:
            #ret, image = self.camera.read()
            #color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            (grabbed, frame) = self.camera.read()
            frame = cv2.flip(frame, 1)
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            if not grabbed:
                break

            # Determine which pixels fall within the blue boundaries and then blur the binary image
            blueMask = cv2.inRange(hsv, blueLower, blueUpper)
            blueMask = cv2.erode(blueMask, kernel, iterations=2)
            blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
            blueMask = cv2.dilate(blueMask, kernel, iterations=1)

            (cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            center = None

            #print(cnts)

            center = (0, 0)
            # Check to see if any contours were found
            if len(cnts) > 0:
                # Sort the contours and find the largest one -- we
                # will assume this contour correspondes to the area of the bottle cap
                cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
                # Get the radius of the enclosing circle around the found contour
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)

                # Get the moments to calculate the center of the contour (in this case Circle)
                M = cv2.moments(cnt)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                que.append(center)
                #cv2.circle(color_frame, (int(center[0]), int(center[1])), 1, (0, 255, 255), 2);
                #print(center)


            start = ()
            end = ()

            color = (255, 128, 128)
            for i in range(len(que)):
                start = end
                end = que[i]
                #cv2.circle(color_frame, (end[0], end[1]), 1, (0, 255, 255), 3)
                if start != () and end != ():
                    cv2.line(color_frame, start, end, color, 2)
                    #print(start, end)

            qt_image = QImage(color_frame.data,
                self.width,
                self.height,
                color_frame.strides[0],
                QImage.Format_RGB888)

            self.VideoSignal.emit(qt_image)

            if center != (0, 0):
                self.changeImage.emit(center)
