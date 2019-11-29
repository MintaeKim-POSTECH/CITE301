# Referenced by
# https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class PicButton(QAbstractButton) :
    def __init__(self, imgdir_n, imgdir_r, imgdir_c, parent=None):
        super(PicButton, self).__init__(parent)
        self.img_n = QPixmap(imgdir_n)
        self.img_r = QPixmap(imgdir_r)
        self.img_c = QPixmap(imgdir_c)

        self.pressed.connect(self.update)
        self.released.connect(self.slot_released)

    def registerButtonHandler(self, func, aux):
        self.handler = func
        self.aux = aux

    def paintEvent(self, event):
        pix = self.img_r if self.underMouse() else self.img_n
        if self.isDown():
            pix = self.img_c

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def slot_released(self):
        self.update()
        (self.handler)(self.aux)

    def sizeHint(self):
        return QSize(80, 80)