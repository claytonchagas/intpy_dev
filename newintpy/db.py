import sqlite3

class DB():
	def __init__(self, DBName):
		self.conn = sqlite3.connect(DBName)
		self.cursor = self.conn.cursor()

	def executeCmdSQLNoReturn(self, sql):
		self.cursor.execute(sql)

	def executeCmdSQLSelect(self, sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def saveChanges(self):
		self.conn.commit()

	def closeConection(self):
		self.conn.close()