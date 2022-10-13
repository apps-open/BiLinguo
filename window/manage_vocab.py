from window.interface.manage_vocab_interface import Ui_Dialog
from PyQt5 import QtWidgets

class Manage_Vocab(QtWidgets.QDialog):
    def __init__(self, database):
        super(Manage_Vocab, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = database
        self.fill_list()
    
    def set_vocab_edit_text(self, item):
        value = item.text()
        self.ui.vocab_edit.setText(value)

    def fill_list(self):
        self.ui.vocabs_list.clear()
        for row in self.db.fetchall("SELECT name FROM vocabs"):
            self.ui.vocabs_list.addItem(row[0])
        self.ui.vocabs_list.itemClicked.connect(self.set_vocab_edit_text)
