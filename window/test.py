from window.interface.test_interface import Ui_MainWindow
from window.statistic import Statistic
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from fuzzywuzzy import fuzz
from window.message import MessageBox
from window.script.message_text import MessageText
import random
import time


class Test(QMainWindow):
	def __init__(self, database):
		super(Test, self).__init__()
		self.__ui = Ui_MainWindow()
		self.__ui.setupUi(self)
		self.__db = database
		self.__pts = 0
		self.__msg = MessageBox()
		self.__accuracy = []
		self.__avg_accuracy = 0.0
		self.__total_words = 0
		self.__learned_words = 0
		self.__tests = 0
		self.__correct = 0
		self.__incorrect = 0
		self.__all = 0
		self.__reps = []
		self.__is_translation = False
		self.__ui.check_button.clicked.connect(self.__main)
		self.__ui.statistic_button.clicked.connect(self.__show_statistic)
		self.__load_stats()

	def __show_statistic(self):
		self.__stats = Statistic(self.__db)
		self.__stats.show()

	def __load_stats(self):
		try:
			if self.__db.current_table:
				data = self.__db.fetchall(f"SELECT * FROM \"{self.__db.current_table}_statistic\"")
				if data:
					self.__tests = data[len(data)-1][1] + 1
					self.__pts = data[len(data)-1][2]
					for i in range(len(data)):
						self.__accuracy.append(data[len(data)-1][3])
					self.__avg_accuracy = data[len(data)-1][4]
					self.__total_words = data[len(data)-1][5]
					self.__learned_words = data[len(data)-1][6]
				else:
					self.__tests = 1
					request = f"INSERT INTO \"{self.__db.current_table}_statistic\" VALUES (\"{time.time()}\",\"{self.__tests}\",\"{self.__pts}\",0,\"{self.__avg_accuracy}\",\"{self.__total_words}\",\"{self.__learned_words}\")"
					self.__db.execute(request)
				self.__main()
			else:
				text = "You need to load or create any database first."
				self.__msg.show(type_=QMessageBox.Warning, text=text, title="Warning!")
				self.close()
		except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")

	def __is_correct(self, txt):
		if txt:
			if self.__db.current_table:
				try:
					request = f"SELECT * FROM \"{self.__db.current_table}\" WHERE word=\"{self.__word}\" OR translation=\"{self.__word}\""
					res = self.__db.fetchall(request)
					if self.__is_translation and fuzz.partial_ratio(res[0][0].lower(), txt.lower()) > 80:
						print(res[0][0].lower(), txt.lower())
						return True
					elif not self.__is_translation and fuzz.partial_ratio(res[0][1].lower(), txt.lower()) > 80:
						print(res[0][1].lower(), txt.lower())
						return True
					else:
						return False
				except Exception as e:
					self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			return False

	def __get_random_word(self):
		if self.__db.current_table:
			try:
				num = random.randint(0, 1)
				if num == 0:
					request = f"SELECT word FROM \"{self.__db.current_table}\""
					data = self.__db.fetchall(request)
					self.__total_words = len(data)
					self.__is_translation = False
					random_word = data[random.randint(0, len(data)-1)][0]
					self.__word = random_word
				else:
					request = f"SELECT translation FROM \"{self.__db.current_table}\""
					data = self.__db.fetchall(request)
					self.__total_words = len(data)
					self.__is_translation = True
					random_word = data[random.randint(0, len(data)-1)][0]
					self.__word = random_word
			except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")


	def __main(self):
		try:
			if self.__is_correct(self.__ui.translation_edit.text()):
				self.__pts += 1
				self.__correct += 1
				request = f"SELECT word FROM \"{self.__db.current_table}\" WHERE translation=\"{self.__word}\""
				res = self.__db.fetchall(request)
				if res:
					self.__word = res[0][0]
				request = f"UPDATE \"{self.__db.current_table}_word_repeats\" SET repeats=repeats+1 WHERE word=\"{self.__word}\""
				self.__db.execute(request)
				self.__ui.check_button_2.setStyleSheet("*{image: url(:/correct_icon/icons8-approval-24.png);\nbackground: #424242;\nborder-radius: 5px;\nborder: 0px solid;\nheight: 32px;}")
			else:
				if self.__pts > 0:
					self.__pts -=  1
				self.__incorrect += 1
				self.__ui.check_button_2.setStyleSheet("*{image: url(:/incorrect_icon/icons8-close-window-24.png);\nbackground: #424242;\nborder-radius: 5px;\nborder: 0px solid;\nheight: 32px;}")
			request = f"SELECT repeats FROM \"{self.__db.current_table}_word_repeats\" WHERE repeats>30"
			data = self.__db.fetchall(request)
			self.__learned_words = len(data)
			self.__all += 1
			self.__get_random_word()
			self.__accuracy.append(self.__correct * 100 / self.__all)
			sum = 0.0
			for i in range(len(self.__accuracy)):
				sum += self.__accuracy[i]
			self.__avg_accuracy = sum / len(self.__accuracy)
			self.__ui.accuracy_label.setText(f"Accuracy: {self.__avg_accuracy:.2f}%")
			self.__ui.pts_label.setText(f"Points: {self.__pts}")
			request = f"INSERT INTO \"{self.__db.current_table}_statistic\" VALUES (\"{time.time()}\",\"{self.__tests}\",\"{self.__pts}\",\"{self.__accuracy[len(self.__accuracy)-1]}\",\"{self.__avg_accuracy}\",\"{self.__total_words}\",\"{self.__learned_words}\")"
			self.__db.execute(request)
			self.__ui.word_label.setText(self.__word)
			self.__ui.translation_edit.clear()
			self.__ui.accuracy_progressbar.setValue(int(self.__avg_accuracy))
		except Exception as e:
				self.__msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")