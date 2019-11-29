# Referenced by
# https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import *

class PicButton(QLabel) :
    def __init__(self, imgdir_n, imgdir_r, imgdir_c, parent):
        QLabel.__init__(self, parent)
        self.imgdir_n = imgdir_n
        self.imgdir_r = imgdir_r
        self.imgdir_c = imgdir_c

        self.img = QPixmap(imgdir_n)
        self.img = self.img.scaledToHeight(80)
        self.setPixmap(self.img)

        self.setMouseTracking(True)

    def registerButtonHandler(self, func, aux):
        self.handler = func
        self.aux = aux

    def mouseMoveEvent(self, event):
        self.img.load(self.imgdir_r)
        self.img = self.img.scaledToHeight(80)
        self.setPixmap(self.img)

        self.repaint()

    def mousePressEvent(self, event):
        self.img.load(self.imgdir_c)
        self.img = self.img.scaledToHeight(80)
        self.setPixmap(self.img)

        self.repaint()

        self.handler(self.aux)