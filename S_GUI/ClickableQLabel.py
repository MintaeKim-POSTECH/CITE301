# Referenced by
# https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt

from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import *

class PicButton(QLabel) :
    def __init__(self, imgdir_n, imgdir_r, imgdir_c, parent):
        QLabel.__init__(self, parent)

        self.img_n = QPixmap(imgdir_n)
        self.img_n = self.img_n.scaledToHeight(80)

        self.img_r = QPixmap(imgdir_r)
        self.img_r = self.img_r.scaledToHeight(80)

        self.img_c = QPixmap(imgdir_c)
        self.img_c = self.img_c.scaledToHeight(80)

        self.setMouseTracking(True)

    def registerButtonHandler(self, func, aux):
        self.handler = func
        self.aux = aux

    def mouseMoveEvent(self, event):
        self.repaint(self.img_r)

    def mousePressEvent(self, event):
        self.repaint(self.img_c)
        self.handler(self.aux)