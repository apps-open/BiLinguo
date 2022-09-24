from PyQt5.QtWidgets import *


class MessageBox(QMessageBox):
	def __init__(self):
		super(MessageBox, self).__init__()

	def show(self, type_=QMessageBox.Information, err=None, buttons=QMessageBox.Ok, text="", title="Message"):
		try:
			self.setIcon(type_)
			self.setText(text)
			if err:
				self.setDetailedText(str(err))
			self.setWindowTitle(title)
			self.setStandardButtons(buttons)
			retval = self.exec_()
		except Exception as e:
			text = f"An error occured while executing notification\n\n{e}"
			self.show(type_=QMessageBox.Critical, err=e, text=text, title="Error!")
		return retval