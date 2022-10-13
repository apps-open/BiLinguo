from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from window.interface.vocabulary_interface import Ui_MainWindow
from window.script.qtablewidgetdisableditem import QTableWidgetDisabledItem
from libretranslatepy import LibreTranslateAPI
from window.manage_vocab import Manage_Vocab
from window.select_vocab import Select_Vocab
from window.test import Test
from window.about import About
from window.message import MessageBox
from window.translate import Translate
from window.script.message_text import MessageText
from window.script.database import Database
from window.translate import Translate
import os
import pyperclip

THEME = "light"

class Vocabulary(QMainWindow):
    def __init__(self):
        super(Vocabulary, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.table = ""
        self.rows = 0
        home_dir = os.path.expanduser("~")
        is_install = False
        db_file = os.path.exists(f"{home_dir}/.BiLinguo/data.db")
        if not db_file:
            is_install = not is_install
            os.system(f"mkdir {home_dir}/.BiLinguo/")
            with open(f"{home_dir}/.BiLinguo/data.db", "w") as file:
                pass
        self.db = Database(
            f"{home_dir}/.BiLinguo/data.db", is_install=is_install)
        self.msg = MessageBox()
        self.ui.load_button.clicked.connect(
            self.show_select_vocabulary_window)
        self.ui.create_button.clicked.connect(
            self.show_manage_vocabulary_window)
        self.translate = LibreTranslateAPI("https://translate.argosopentech.com/")
        self.ui.delete_button.clicked.connect(self.delete_word)
        self.ui.add_word_button.clicked.connect(self.word_add)
        self.ui.save_button.clicked.connect(self.save_table)
        self.ui.test_button.clicked.connect(self.show_test_window)
        self.ui.search_button.clicked.connect(self.search)
        self.ui.clear_search.clicked.connect(self.clear_search)
        self.ui.close_button.clicked.connect(self.vocab_close)
        self.ui.info_button.clicked.connect(self.show_about)
        self.ui.translate_button.clicked.connect(self.show_translate_window)
        self.Size = QTableWidgetDisabledItem(self.ui.vocabulary_table)
        self.ui.vocabulary_table.setItemDelegateForColumn(0, self.Size)

    def clear_search(self):
        self.ui.search_edit.clear()
        if self.table:
            self.fill_table(request=f"SELECT * FROM \"{self.table}\"")

    def search(self):
        self.save_table()
        to_search = self.ui.search_edit.text()
        if to_search:
            try:
                if self.table:
                    request = f"SELECT * FROM \"{self.table}\""
                    data = self.db.fetchall(request)
                    to_fill = []
                    for tup in data:
                        for cell in tup:
                            cell = str(cell)
                            if to_search.lower() in cell.lower():
                                to_fill.append(tup)
                                break
                    if to_fill:
                        self.fill_table(data=to_fill)
                    else:
                        self.fill_table(request=request)
                        text = "There is no results related to your request."
                        self.ui.statusBar.showMessage(text)
                else:
                    self.msg.show(type_=QMessageBox.Information,
                                    text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Warning!")
            except Exception as e:
                self.msg.show(type_=QMessageBox.Critical, err=e,
                                text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
        else:
            text = "Enter search query first!"
            self.msg.show(type_=QMessageBox.Information,
                            buttons=QMessageBox.Ok, text=text, title="Warning!")

    def vocab_close(self):
        if self.table:
            self.save_table()
            self.db.current_table = ""
            self.ui.vocabulary_table.clear()
            self.ui.vocabulary_table.setHorizontalHeaderLabels(
                ("Word", "Translation", "Notes"))
            self.table = ""
            self.setWindowTitle("BiLinguo")
            self.ui.vocabulary_table.setRowCount(0)
        else:
            text = "Nothing to close."
            self.ui.statusBar.showMessage(text)

    def delete_vocab(self):
        name = self.manage_vocab.ui.vocab_edit.text()
        if name:
            text = f"Are you sure to delete table \"{name}\"? All data associated with the vocabulary will be lost!"
            reply = self.msg.show(type_=QMessageBox.Warning, buttons=QMessageBox.Yes |
                                    QMessageBox.No, text=text, title="Attention!")
            if reply == QMessageBox.Yes:
                try:
                    self.db.execute(f"DROP TABLE \"{name}\"")
                    self.db.execute(f"DROP TABLE \"{name}_statistics\"")
                    self.db.execute(f"DROP TABLE \"{name}_word_repeats\"")
                    self.db.execute(
                        f"DELETE FROM vocabs WHERE name=\"{name}\"")
                    self.manage_vocab.fill_list()
                except Exception as e:
                    self.msg.show(type_=QMessageBox.Critical, err=e,
                                    text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Warning!")
        self.manage_vocab.fill_list()
        if name == self.table:
            self.table_close()
        self.manage_vocab.ui.vocab_edit.clear()

    def create_vocab(self):
        try:
            name = self.manage_vocab.ui.vocab_edit.text()
            if name:
                res = self.db.fetchall(f"SELECT * FROM \"vocabs\" WHERE name=\"{name}\"")
                if not res:
                    self.db.execute(
                        f"CREATE TABLE \"{name}\" (\"id\" INTEGER UNIQUE NOT NULL, \"word\" TEXT NOT NULL UNIQUE, \"translation\" TEXT NOT NULL, \"notes\" TEXT)")
                    self.db.execute(f"""CREATE TABLE \"{name}_statistic\" (
                        \"date\"	REAL NOT NULL UNIQUE,
                        \"tests\"	INTEGER NOT NULL,
                        \"total_pts\"	INTEGER NOT NULL,
                        \"accuracy\"	REAL NOT NULL,
                        \"avg_accuracy\"	REAL NOT NULL,
                        \"total_words\"	INTEGER NOT NULL,
                        \"learned_words\"	INTEGER NOT NULL
                    )""")
                    self.db.execute(
                        f"CREATE TABLE \"{name}_word_repeats\" (\"word\" TEXT NOT NULL UNIQUE, \"repeats\" INTEGER NOT NULL)")

                    self.db.execute(f"INSERT INTO vocabs VALUES (\"{name}\")")
                    self.manage_vocab.fill_list()
                else:
                    self.msg.show(type_=QMessageBox.Information, 
                        text="Such table already exists! Try another name.", title="Information")
            else:
                self.msg.show(type_=QMessageBox.Information,
                                text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Warning!")
        except Exception as e:
            self.msg.show(type_=QMessageBox.Critical, err=e,
                            text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
        self.manage_vocab.ui.vocab_edit.clear()

    def word_add(self):
        if self.table:
            self.ui.vocabulary_table.setRowCount(self.ui.vocabulary_table.rowCount()+1)
            cellinfo = QTableWidgetItem(str(self.ui.vocabulary_table.rowCount()))
            self.ui.vocabulary_table.setItem(self.ui.vocabulary_table.rowCount() - 1, 0, cellinfo)
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Information")

    def save_table(self):
        is_word_added = False
        if self.table:
            try:
                for row in range(self.ui.vocabulary_table.rowCount()):
                    word = self.ui.vocabulary_table.item(row, 1)
                    translation = self.ui.vocabulary_table.item(row, 2)
                    note = self.ui.vocabulary_table.item(row, 3)
                    id = int(self.ui.vocabulary_table.item(row, 0).text())
                    if not note:
                        note = QTableWidgetItem("")
                    if id and word and translation:
                        request = f"SELECT word FROM \"{self.table}\" WHERE word=\"{word.text()}\""
                        res = self.db.fetchall(request)
                        if res and row <= self.rows:
                            request = f"UPDATE \"{self.table}\" SET word=\"{word.text()}\", translation=\"{translation.text()}\", notes=\"{note.text()}\" WHERE id={id}"
                            self.db.execute(request)
                        elif not res and row > self.rows:
                            self.rows += 1
                            self.db.execute(
                                f"INSERT INTO \"{self.table}\" VALUES ({id}, \"{word.text()}\", \"{translation.text()}\", \"{note.text()}\")")
                            self.db.execute(
                                f"INSERT INTO \"{self.table}_word_repeats\" VALUES (\"{word.text()}\", 0)")
                            is_word_added = True
                    else:
                        self.ui.statusBar.showMessage(MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION)
                msg = "A new word(-s) added."
                if is_word_added:
                    self.ui.statusBar.showMessage(msg + " Changes applied!")
                else:
                    self.ui.statusBar.showMessage("Changes applied!")
            except Exception as e:
                self.msg.show(type_=QMessageBox.Critical, err=e,
                                text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Information")
        if self.table:
            self.fill_table(f"SELECT * FROM \"{self.table}\"")

    def fill_table(self, request="", data=None):
        if request and not data:
            data = self.db.fetchall(request)
        header = self.ui.vocabulary_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.rows = len(data)
        self.ui.vocabulary_table.setRowCount(len(data))
        if data:
            row = 0
            for tup in data:
                col = 0
                for item in tup:
                    cellinfo = QTableWidgetItem(str(item))
                    self.ui.vocabulary_table.setItem(row, col, cellinfo)
                    col += 1
                row += 1
        else:
            text = f"There is no data to display because of empty SQL query response"
            self.ui.statusBar.showMessage(text)

    def translate_word(self):
        word_translate = self.translate_window.ui.phrase_edit.text()
        translate_from = self.translate_window.ui.translate_from.currentText()[
            :2]
        translate_to = self.translate_window.ui.translate_to.currentText()[
            :2]
        if word_translate and translate_from and translate_to:
            try:
                output = self.translate.translate(
                    word_translate, translate_from, translate_to)
                self.translate_window.ui.output_edit.setText(output)
            except Exception as e:
                self.msg.show(type_=QMessageBox.Critical, err=e,
                                text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Information")

    def copy_translation(self):
        if self.translate_window.ui.output_edit.text():
            pyperclip.copy(self.translate_window.ui.output_edit.text())
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=f"There is no output to copy", title="Information")

    def delete_word(self):
        if self.table:
            try:
                for item in self.ui.vocabulary_table.selectedItems():
                    if item.column() < 1:
                        request = f"SELECT word FROM \"{self.table}\" WHERE word=\"{item.text()}\""
                        res = self.db.fetchall(request)
                        if res:
                            request = f"DELETE FROM \"{self.table}\" WHERE word=\"{item.text()}\""
                            self.db.execute(request)
                            request = f"DELETE FROM \"{self.table}_word_repeats\" WHERE word=\"{item.text()}\""
                            self.db.execute(request)
                        else:
                            self.ui.vocabulary_table.removeRow(item.row())
            except Exception as e:
                self.msg.show(type_=QMessageBox.Critical, err=e,
                                text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Information")
        if self.table:
            self.fill_table(request=f"SELECT * FROM \"{self.table}\"")

    def load_vocabulary(self):
        try:
            if self.select_vocab.ui.vocab_list.count() > 0:
                value = self.select_vocab.ui.vocab_list.currentItem().text()
                if self.table:
                    self.table_close()
                self.table = value
                self.db.current_table = value
                self.fill_table(request=f"SELECT * FROM \"{self.table}\"")
                self.select_vocab.close()
                self.setWindowTitle(f"Vocabulary - \"{self.table}\"")
            else:
                self.msg.show(type_=QMessageBox.Information,
                                text="You don't have any dictionary yet!", title="Error!")
        except Exception as e:
            self.msg.show(type_=QMessageBox.Critical, err=e,
                            text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")

    def show_translate_window(self):
        self.translate_window = Translate()
        langs = self.translate.languages()
        self.langs = {}
        for item in langs:
            self.langs[f"{item['code']}"] = f"{item['name']}"
        for k, v in self.langs.items():
            self.translate_window.ui.translate_to.addItem(f"{k}: {v}")
            self.translate_window.ui.translate_from.addItem(f"{k}: {v}")
        self.translate_window.ui.translate_button.clicked.connect(
            self.translate_word)
        self.translate_window.ui.copy_button.clicked.connect(
            self.copy_translation)
        self.translate_window.exec_()

    def show_select_vocabulary_window(self):
        self.select_vocab = Select_Vocab(self.db)
        self.select_vocab.ui.open_button.clicked.connect(
            self.load_vocabulary)
        self.select_vocab.fill_list()
        self.select_vocab.exec_()

    def show_test_window(self):
        if self.table:
            self.test = Test(self.db)
            self.test.exec_()
        else:
            self.msg.show(type_=QMessageBox.Information,
                            text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Warning!")

    def show_manage_vocabulary_window(self):
        self.manage_vocab = Manage_Vocab(self.db)
        self.manage_vocab.ui.create_button.clicked.connect(
            self.create_vocab)
        self.manage_vocab.ui.delete_button.clicked.connect(
            self.delete_vocab)
        self.manage_vocab.exec_()

    def show_about(self):
        self.about = About()
        self.about.exec_()


app = QApplication([])
application = Vocabulary()
application.show()

app.exec_()
