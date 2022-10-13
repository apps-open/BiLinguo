from window.interface.select_vocab_interface import Ui_Dialog
from PyQt5 import QtWidgets

class Select_Vocab(QtWidgets.QDialog):
    def __init__(self, database):
        super(Select_Vocab, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = database
        self.fill_list()

    def fill_list(self):
        self.ui.vocab_list.clear()
        for row in self.db.fetchall("SELECT name FROM vocabs"):
            self.ui.vocab_list.addItem(row[0])
            