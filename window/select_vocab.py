from window.interface.select_vocab_interface import Ui_MainWindow
from PyQt5 import QtWidgets

class Select_Vocab(QtWidgets.QMainWindow):
    def __init__(self, database):
        super(Select_Vocab, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__db = database
        self.fill_list()

    def fill_list(self):
        self.ui.vocab_list.clear()
        for row in self.__db.fetchall("SELECT name FROM vocabs"):
            self.ui.vocab_list.addItem(row[0])
            