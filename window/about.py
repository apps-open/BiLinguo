from window.interface.about_interface import Ui_Dialog
from PyQt5 import QtWidgets


class About(QtWidgets.QDialog):
    def __init__(self):
        super(About, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)