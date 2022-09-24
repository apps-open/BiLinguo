import sqlite3


class Database:
	def __init__(self, path, is_install: bool):
		self.__connection = sqlite3.connect(path)
		self.__cursor = self.__connection.cursor()
		if is_install:
			self.execute("CREATE TABLE vocabs (\"name\" TEXT NOT NULL UNIQUE)")
		self.current_table = ""

	def execute(self, request):
		self.__cursor.execute(request)
		self.__connection.commit()

	def fetchall(self, request):
		res = self.__cursor.execute(request)
		return res.fetchall()
