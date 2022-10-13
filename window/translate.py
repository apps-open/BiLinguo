from window.interface.translate_interface import Ui_Dialog
from PyQt5 import QtWidgets


class Translate(QtWidgets.QDialog):

    def __init__(self):
        super(Translate, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)