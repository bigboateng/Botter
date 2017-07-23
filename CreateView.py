import sys
import os
import cv2

from PyQt5 import uic, QtWidgets
from PIL import ImageGrab
import numpy as np
from datetime import datetime

qtViewFile = "./Design/Create.ui"  # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtViewFile)


class CreateView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.box = 0
        self.capture_screen = False

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.start_rec_bt.clicked.connect(self.onclicked_start)
        self.analyse_rec_bt.clicked.connect(self.onclicked_analyse)
        self.stop_rec_bt.clicked.connect(self.onclicked_stop)

        self.fullsc_radb.setChecked(True)
        self.fullsc_radb.toggled.connect(self.full_screen_radb)
        self.boxsc_radb.toggled.connect(self.box_screen_radb)

    def onclicked_start(self):
        print("start", self.frequency_spin_box.value())
        self.capture_screen = True
        speed = self.frequency_spin_box.value()

        time_folder = datetime.now().strftime('%m%d_%H:%M:%S')

        directory = "./" + time_folder
        if not os.path.exists(directory):
            os.makedirs(directory)

        if isinstance(self.box, int):
            while self.capture_screen:
                im = ImageGrab.grab()
                im.save("./"+time_folder+"/"+datetime.now().strftime('%m%d_%H_%M_%S')+".png")
        else:
            while self.capture_screen:
                im = ImageGrab.grab(self.box)
                im.save("./"+time_folder+"/"+datetime.now().strftime('%m%d_%H_%M_%S')+".png")



    def onclicked_stop(self):
        print("stop")

    def onclicked_analyse(self):
        print("analyse")
        print(self.keyboard_chb.isChecked())
        print(self.mouse_chb.isChecked())

    def full_screen_radb(self):
        if self.fullsc_radb.isChecked():
            self.box = 0
            self.screen_mode.setText("Current mode: Full screen")

    def box_screen_radb(self):
        if self.boxsc_radb.isChecked():
            im = ImageGrab.grab()
            im.save("./image.png")

            img = cv2.imread('./image.png')

            # Select ROI
            showCrosshair = False
            fromCenter = False
            r = cv2.selectROI("Choose box and press any key", img, fromCenter, showCrosshair)
            self.screen_mode.setText("Current mode: not Full screen")

            print([int(r[0]), int(r[1]), int(r[2]), int(r[3])]) #x, y, width, height

            # Crop image
            imCrop = img[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            # Display cropped image
            cv2.imshow("Press any key to finish", imCrop)
            cv2.waitKey(0)
            cv2.waitKey(0)
            cv2.destroyAllWindows()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CreateView()
    window.show()
    sys.exit(app.exec_())