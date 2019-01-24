import cv2 as cv

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot


class StreamThread(QThread):
    imageSignal = pyqtSignal(QImage)

    def run(self):
        video = cv.VideoCapture(0)

        while True:
            ret, frame = video.read()

            if ret:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                frameInQtFormat = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                frameInQtFormat = frameInQtFormat.scaled(224, 224, Qt.KeepAspectRatio)
                # Stream image to GUI
                self.imageSignal.emit(frameInQtFormat)


class EmailSenderThread(QThread):
    """Thread to call a email sender
    """

    emailStatusSignal = pyqtSignal(bool)
    emailSender = None
    filename = None

    def run(self):
        try:
            self.emailSender.sendAttachEmail(self.filename)
            self.emailStatusSignal.emit(True)
        except BaseException as error:
            self.emailStatusSignal.emit(False)
