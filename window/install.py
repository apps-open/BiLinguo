from window.interface.install_path_interface import Ui_MainWindow
from PyQt5 import QtWidgets


class Install(QtWidgets.QMainWindow):
    def __init__(self):
        super(Install, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        