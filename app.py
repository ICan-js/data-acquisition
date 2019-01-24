import sys

from PyQt5.QtWidgets import QApplication
from data_app.gui.image_widgets import Window

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()

    # Work!
    window.startThread()
    window.show()

    # Definitions
    window.showWelcomeDialog()
    window.definePathToSave()

    sys.exit(app.exec())
