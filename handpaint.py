# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PySide2.QtCore import *
from PySide2.QtGui import *
from ImageViewer import *
from ShowVideo import ShowVideo
from Panel import Panel

if __name__ == "__main__":
    app = QApplication(sys.argv)

    video = ShowVideo()
    thread = QThread()

    video.moveToThread(thread)
    thread.start()

    image_viewer = ImageViewer()
    video.VideoSignal.connect(image_viewer.setImage)

    button_layout = QVBoxLayout()

    start_button = QPushButton('Start')
    start_button.clicked.connect(video.startVideo)
    button_layout.addWidget(start_button)

    image_layout = QVBoxLayout()
    image_layout.addWidget(image_viewer)

    panel_layout = QVBoxLayout()

    panel = Panel()
    #thread2 = QThread()
    #panel.moveToThread(thread2)
    #thread2.start()

    canvas_viewer = ImageViewer()
    panel.ImageSignal.connect(canvas_viewer.setImage)
    panel_layout.addWidget(canvas_viewer)

    red_button = QPushButton('red')
    red_button.clicked.connect(panel.changeRed)

    green_button = QPushButton('green')
    green_button.clicked.connect(panel.changeGreen)

    blue_button = QPushButton('blue')
    blue_button.clicked.connect(panel.changeBlue)

    video.changeImage.connect(panel.draw)

    button_layout.addWidget(red_button)
    button_layout.addWidget(green_button)
    button_layout.addWidget(blue_button)

    main_layout = QHBoxLayout()
    main_layout.addLayout(button_layout)


    main_layout.addLayout(panel_layout)
    main_layout.addLayout(image_layout)

    layout_widget = QWidget()
    layout_widget.setLayout(main_layout)

    main_window = QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()

    sys.exit(app.exec_())
