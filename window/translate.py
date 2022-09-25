from window.interface.translate_interface import Ui_MainWindow
from PyQt5 import QtWidgets


class Translate(QtWidgets.QMainWindow):

    def __init__(self):
        super(Translate, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)