from window.interface.manage_vocab_interface import Ui_MainWindow
from PyQt5 import QtWidgets

class Manage_Vocab(QtWidgets.QMainWindow):
    def __init__(self, database):
        super(Manage_Vocab, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__db = database
        self.fill_list()
    
    def __set_vocab_edit_text(self, item):
        value = item.text()
        self.ui.vocab_edit.setText(value)

    def fill_list(self):
        self.ui.vocabs_list.clear()
        for row in self.__db.fetchall("SELECT name FROM vocabs"):
            self.ui.vocabs_list.addItem(row[0])
        self.ui.vocabs_list.itemClicked.connect(self.__set_vocab_edit_text)
