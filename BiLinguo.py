from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from window.interface.vocabulary_interface import Ui_MainWindow
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
import os, pyperclip


class Vocabulary(QMainWindow):
	def __init__(self):
		super(Vocabulary, self).__init__()
		self.__ui = Ui_MainWindow()
		self.__ui.setupUi(self)
		self.__table = ""
		self.__rows = 0
		home_dir = os.path.expanduser("~")
		is_install = False
		db_file = os.path.exists(f"{home_dir}/.BiLinguo/data.db")
		if not db_file:
			is_install = not is_install
			os.system(f"mkdir {home_dir}/.BiLinguo/")
			with open(f"{home_dir}/.BiLinguo/data.db", "w") as file:
				pass
		self.__db = Database(f"{home_dir}/.BiLinguo/data.db", is_install=is_install)
		self.__msg = MessageBox()
		self.__ui.load_button.clicked.connect(self.__show_select_vocabulary_window)
		self.__ui.create_button.clicked.connect(self.__show_manage_vocabulary_window)
		self.__ui.delete_button.clicked.connect(self.__delete_word)
		self.__ui.add_word_button.clicked.connect(self.__word_add)
		self.__ui.save_button.clicked.connect(self.__save_table)
		self.__ui.test_button.clicked.connect(self.__show_test_window)
		self.__ui.search_button.clicked.connect(self.__search)
		self.__ui.clear_search.clicked.connect(self.__clear_search)
		self.__ui.close_button.clicked.connect(self.__table_close)
		self.__ui.info_button.clicked.connect(self.__show_about)
		self.__ui.translate_button.clicked.connect(self.__show_translate_window)
		self.__ui.vocabulary_table.setColumnCount(3)
		
	def __clear_search(self):
		self.__ui.search_edit.clear()
		if self.__table:
			self.__fill_table(request=f"SELECT * FROM \"{self.__table}\"")
		
	def __search(self):
		to_search = self.__ui.search_edit.text()
		if to_search:
			try:
				if self.__table:
					request = f"SELECT * FROM \"{self.__table}\""
					data = self.__db.fetchall(request)
					to_fill = []
					for tup in data:
						for cell in tup:
							if to_search.lower() in cell.lower():
								to_fill.append(tup)
								break
					if to_fill:
						self.__fill_table(data=to_fill)
					else:
						self.__fill_table(request=request)
						text = "There is no results related to your request."
						self.__msg.show(type_=QMessageBox.Information, text=text, title="Information")
				else:
					self.__msg.show(type_=QMessageBox.Information, text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Warning!")
			except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			text = "Enter search query first!"
			self.__msg.show(type_=QMessageBox.Information, buttons=QMessageBox.Ok, text=text, title="Warning!")

	def __table_close(self):
		if self.__table:
			self.__save_table()
			self.__db.current_table = ""
			self.__ui.vocabulary_table.clear()
			self.__ui.vocabulary_table.setHorizontalHeaderLabels(("Word", "Translation", "Notes"))
			self.__table = ""
			self.setWindowTitle("Vocabulary")
			self.__ui.vocabulary_table.setRowCount(0)
		else:
			text = "Nothing to close."
			self.__msg.show(type_=QMessageBox.Information, buttons=QMessageBox.Ok, text=text, title="Information")

	def __delete_vocab(self):
		name = self.__manage_vocab.ui.vocab_edit.text()
		if name:
			text = f"Are you sure to delete table \"{name}\"? All data associated with the vocabulary will be lost!"
			reply = self.__msg.show(type_=QMessageBox.Warning, buttons=QMessageBox.Yes | QMessageBox.No, text=text, title="Attention!")
			if reply == QMessageBox.Yes:
				try:
					self.__db.execute(f"DROP TABLE \"{name}\"")
					self.__db.execute(f"DELETE FROM vocabs WHERE name=\"{name}\"")
					self.__manage_vocab.fill_list()
				except Exception as e:
					self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			self.__msg.show(type_=QMessageBox.Information, text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Warning!")
		self.__manage_vocab.fill_list()
		if name == self.__table:
			self.__table_close()
		self.__manage_vocab.ui.vocab_edit.clear()

	def __create_vocab(self):
		try:
			name = self.__manage_vocab.ui.vocab_edit.text()
			if name:
				self.__db.execute(f"CREATE TABLE \"{name}\" (\"word\" TEXT NOT NULL UNIQUE, \"translation\" TEXT NOT NULL, \"notes\" TEXT)")
				self.__db.execute(f"""CREATE TABLE \"{name}_statistic\" (
					\"date\"	REAL NOT NULL UNIQUE,
					\"tests\"	INTEGER NOT NULL,
					\"total_pts\"	INTEGER NOT NULL,
					\"accuracy\"	REAL NOT NULL,
					\"avg_accuracy\"	REAL NOT NULL,
					\"total_words\"	INTEGER NOT NULL,
					\"learned_words\"	INTEGER NOT NULL
				)""")
				self.__db.execute(f"CREATE TABLE \"{name}_word_repeats\" (\"word\" TEXT NOT NULL UNIQUE, \"repeats\" INTEGER NOT NULL)")

				self.__db.execute(f"INSERT INTO vocabs VALUES (\"{name}\")")
				self.__manage_vocab.fill_list()
			else:
				self.__msg.show(type_=QMessageBox.Information, text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Warning!")
		except Exception as e:
			self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")

	def __word_add(self):
		if self.__table:
			self.__ui.vocabulary_table.setRowCount(self.__ui.vocabulary_table.rowCount()+1)
		else:
			self.__msg.show(type_=QMessageBox.Information, text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Information")

	def __save_table(self):
		is_word_added = False
		if self.__table:
			try:
				for row in range(self.__ui.vocabulary_table.rowCount()):
					word = self.__ui.vocabulary_table.item(row, 0)
					translation = self.__ui.vocabulary_table.item(row, 1)
					note = self.__ui.vocabulary_table.item(row, 2)
					if not note:
						note = QTableWidgetItem("")
					if word and translation:
						request = f"SELECT word FROM \"{self.__table}\" WHERE word=\"{word.text()}\""
						res = self.__db.fetchall(request)
						if res and row < self.__rows:
							request = f"UPDATE \"{self.__table}\" SET word=\"{word.text()}\", translation=\"{translation.text()}\", notes=\"{note.text()}\" WHERE word=\"{word.text()}\""
							self.__db.execute(request)
						elif res and row >= self.__rows:
							text = f"Such word already exists in current vocabulary. To add more meanings for this word use \"note\" \
								column of appropriate word or use search line to find it thorough current dictionary."
							self.__msg.show(type_=QMessageBox.Information, text=text, title="Information")
						elif not res and row >= self.__rows:
							self.__rows += 1
							self.__db.execute(f"INSERT INTO \"{self.__table}\" VALUES (\"{word.text()}\", \"{translation.text()}\", \"{note.text()}\")")
							self.__db.execute(f"INSERT INTO \"{self.__table}_word_repeats\" VALUES (\"{word}\", 0)")
							is_word_added = True
					else:
						self.__msg.show(type_=QMessageBox.Information, text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Information")
				if is_word_added:
					self.__msg.show(type_=QMessageBox.Information, text=f"A new word(-s) added.", title="Congratulations!")
			except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			self.__msg.show(type_=QMessageBox.Information, text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Information")
		if self.__table:
			self.__fill_table(f"SELECT * FROM \"{self.__table}\"")

	def __fill_table(self, request="", data=None):
		if request and not data:
			data = self.__db.fetchall(request)
		header = self.__ui.vocabulary_table.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.Stretch)
		header.setSectionResizeMode(2, QHeaderView.Stretch)
		self.__rows = len(data)
		self.__ui.vocabulary_table.setRowCount(len(data))
		if data:
			row = 0
			for tup in data:
				col = 0
				for item in tup:
					cellinfo = QTableWidgetItem(item)
					self.__ui.vocabulary_table.setItem(row, col, cellinfo)
					col += 1
				row += 1
		else:
			text = f"There is no data to display because of empty SQL query response"
			self.__msg.show(type_=QMessageBox.Information, text=text, title="Information")

	def __translate_word(self):
		word_translate = self.__translate_window.ui.phrase_edit.text()
		translate_from = self.__translate_window.ui.translate_from.currentText()[:2]
		translate_to = self.__translate_window.ui.translate_to.currentText()[:2]
		if word_translate and translate_from and translate_to:
			try:
				output = self.__translate.translate(word_translate, translate_from, translate_to)
				self.__translate_window.ui.output_edit.setText(output)
			except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			self.__msg.show(type_=QMessageBox.Information, text=MessageText.FILL_REQUIRED_FIELDS_BEFORE_ACTION, title="Information")

	
	def __copy_translation(self):
		if self.__translate_window.ui.output_edit.text():
			pyperclip.copy(self.__translate_window.ui.output_edit.text())
		else:
			self.__msg.show(type_=QMessageBox.Information, text=f"There is no output to copy", title="Information")

	def __delete_word(self):
		if self.__table:
			try:
				for item in self.__ui.vocabulary_table.selectedItems():
					if item.column() < 1:
						request = f"SELECT word FROM \"{self.__table}\" WHERE word=\"{item.text()}\""
						res = self.__db.fetchall(request)
						if res:
							request = f"DELETE FROM \"{self.__table}\" WHERE word=\"{item.text()}\""
							self.__db.execute(request)
							request = f"DELETE FROM \"{self.__table}_word_repeats\" WHERE word=\"{item.text()}\""
							self.__db.execute(request)
						else:
							self.__ui.vocabulary_table.removeRow(item.row())
			except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			self.__msg.show(type_=QMessageBox.Information, text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Information")
		if self.__table:
			self.__fill_table(request=f"SELECT * FROM \"{self.__table}\"")

	def __load_vocabulary(self):
		try:
			if self.__select_vocab.ui.vocab_list.count() > 0:
				value = self.__select_vocab.ui.vocab_list.currentItem().text()
				if self.__table:
					self.__table_close()
				self.__table = value
				self.__db.current_table = value
				self.__fill_table(request=f"SELECT * FROM \"{self.__table}\"")
				self.__select_vocab.close()
				self.setWindowTitle(f"Vocabulary - \"{self.__table}\"")
			else:
				self.__msg.show(type_=QMessageBox.Information, text="You don't have any dictionary yet!", title="Error!")
		except Exception as e:
			self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")

	def __show_translate_window(self):
		self.__translate_window = Translate()
		self.__translate = LibreTranslateAPI("https://translate.argosopentech.com/")
		langs = self.__translate.languages()
		self.__langs = {}
		for item in langs:
			self.__langs[f"{item['code']}"] = f"{item['name']}"
		for k, v in self.__langs.items():
			self.__translate_window.ui.translate_to.addItem(f"{k}: {v}")
			self.__translate_window.ui.translate_from.addItem(f"{k}: {v}")
		self.__translate_window.ui.translate_button.clicked.connect(self.__translate_word)
		self.__translate_window.ui.copy_button.clicked.connect(self.__copy_translation)
		self.__translate_window.show()
		
	def __show_select_vocabulary_window(self):
		self.__select_vocab = Select_Vocab(self.__db)
		self.__select_vocab.ui.open_button.clicked.connect(self.__load_vocabulary)
		self.__select_vocab.fill_list()
		self.__select_vocab.show()

	def __show_test_window(self):
		if self.__table:
			self.__test = Test(self.__db)
			self.__test.show()
		else:
			self.__msg.show(type_=QMessageBox.Information, text=MessageText.LOAD_DICTIONARY_BEFORE_ACTION, title="Warning!")

	def __show_manage_vocabulary_window(self):
		self.__manage_vocab = Manage_Vocab(self.__db)
		self.__manage_vocab.ui.create_button.clicked.connect(self.__create_vocab)
		self.__manage_vocab.ui.delete_button.clicked.connect(self.__delete_vocab)
		self.__manage_vocab.show()
	
	def __show_about(self):
		self.about = About()
		self.about.show()

app = QApplication([])
application = Vocabulary()
application.show()

app.exec_()