from numpy import char
from window.interface.test_interface import Ui_Dialog
from window.statistic import Statistic
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from fuzzywuzzy import fuzz
from window.message import MessageBox
from window.script.message_text import MessageText
import random
import time


class Test(QDialog):
	def __init__(self, database):
		super(Test, self).__init__()
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
		self.db = database
		self.pts = 0
		self.msg = MessageBox()
		self.accuracy = []
		self.avg_accuracy = 0.0
		self.total_words = 0
		self.learned_words = 0
		self.tests = 0
		self.correct = 0
		self.incorrect = 0
		self.all = 0
		self.reps = []
		self.is_translation = False
		self.ui.check_button.clicked.connect(self.main)
		self.ui.statistic_button.clicked.connect(self.show_statistic)
		self.load_stats()

	def show_statistic(self):
		self.stats = Statistic(self.db)
		self.stats.show()

	def load_stats(self):
		try:
			if self.db.current_table:
				data = self.db.fetchall(f"SELECT * FROM \"{self.db.current_table}_statistic\"")
				if data:
					self.tests = data[len(data)-1][1] + 1
					self.pts = data[len(data)-1][2]
					for i in range(len(data)):
						self.accuracy.append(data[len(data)-1][3])
					self.avg_accuracy = data[len(data)-1][4]
					self.total_words = data[len(data)-1][5]
					self.learned_words = data[len(data)-1][6]
				else:
					self.tests = 1
					request = f"INSERT INTO \"{self.db.current_table}_statistic\" VALUES (\"{time.time()}\",\"{self.tests}\",\"{self.pts}\",0,\"{self.avg_accuracy}\",\"{self.total_words}\",\"{self.learned_words}\")"
					self.db.execute(request)
				self.main()
			else:
				text = "You need to load or create any database first."
				self.msg.show(type_=QMessageBox.Warning, text=text, title="Warning!")
				self.close()
		except Exception as e:
				self.msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")

	def is_correct(self, txt):
		if txt:
			text = ""
			symbs = "!@#$%^&*()-_=+/|\\,><./~`'\"1234567890№;:"
			for chr in txt:
				if chr not in symbs:
					text += char
			txt = text
			if self.db.current_table:
				try:
					request = f"SELECT \"word\", \"translation\", \"notes\" FROM \"{self.table}\" FROM \"{self.db.current_table}\" WHERE word=\"{self.word}\" OR translation=\"{self.word}\""
					res = self.db.fetchall(request)
					if self.is_translation and fuzz.partial_ratio(res[0][0].lower(), txt.lower()) > 80:
						return True
					elif not self.is_translation and fuzz.partial_ratio(res[0][1].lower(), txt.lower()) > 80:
						return True
					else:
						return False
				except Exception as e:
					self.msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")
		else:
			return False

	def get_random_word(self):
		if self.db.current_table:
			try:
				num = random.randint(0, 1)
				if num == 0:
					request = f"SELECT word FROM \"{self.db.current_table}\""
					data = self.db.fetchall(request)
					self.total_words = len(data)
					self.is_translation = False
					random_word = data[random.randint(0, len(data)-1)][0]
					self.word = random_word
				else:
					request = f"SELECT translation FROM \"{self.db.current_table}\""
					data = self.db.fetchall(request)
					self.total_words = len(data)
					self.is_translation = True
					random_word = data[random.randint(0, len(data)-1)][0]
					self.word = random_word
			except Exception as e:
				self.msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")


	def main(self):
		try:
			if self.is_correct(self.ui.translation_edit.text()):
				self.pts += 1
				self.correct += 1
				request = f"SELECT word FROM \"{self.db.current_table}\" WHERE translation=\"{self.word}\""
				res = self.db.fetchall(request)
				if res:
					self.word = res[0][0]
				request = f"UPDATE \"{self.db.current_table}_word_repeats\" SET repeats=repeats+1 WHERE word=\"{self.word}\""
				self.db.execute(request)
				self.ui.check_button_2.setStyleSheet("*{image: url(:/correct_icon/icons8-approval-24.png);\n\nborder-radius: 5px;\nborder: 0px solid;\nheight: 32px;}")
			else:
				if self.pts > 0:
					self.pts -=  1
				self.incorrect += 1
				self.ui.check_button_2.setStyleSheet("*{image: url(:/incorrect_icon/icons8-close-window-24.png);\n\nborder-radius: 5px;\nborder: 0px solid;\nheight: 32px;}")
			request = f"SELECT repeats FROM \"{self.db.current_table}_word_repeats\" WHERE repeats>30"
			data = self.db.fetchall(request)
			self.learned_words = len(data)
			self.all += 1
			self.get_random_word()
			self.accuracy.append(self.correct * 100 / self.all)
			sum = 0.0
			for i in range(len(self.accuracy)):
				sum += self.accuracy[i]
			self.avg_accuracy = sum / len(self.accuracy)
			self.ui.accuracy_label.setText(f"Accuracy: {self.avg_accuracy:.2f}%")
			self.ui.pts_label.setText(f"Points: {self.pts}")
			request = f"INSERT INTO \"{self.db.current_table}_statistic\" VALUES (\"{time.time()}\",\"{self.tests}\",\"{self.pts}\",\"{self.accuracy[len(self.accuracy)-1]}\",\"{self.avg_accuracy}\",\"{self.total_words}\",\"{self.learned_words}\")"
			self.db.execute(request)
			self.ui.word_label.setText(self.word)
			self.ui.translation_edit.clear()
			self.ui.accuracy_progressbar.setValue(int(self.avg_accuracy))
		except Exception as e:
				self.msg.show(type_=QMessageBox.Critical, err=e, text=MessageText.AN_ERROR_OCCURED_WHILE_ACTION, title="Error!")