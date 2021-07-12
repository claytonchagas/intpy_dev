import sqlite3

class Banco():
	def __init__(self, nomeBanco):
		self.conexao = sqlite3.connect(nomeBanco)
		self.cursor = self.conexao.cursor()

	def executarComandoSQLSemRetorno(self, sql, arguments=()):
		self.cursor.execute(sql, arguments)

	def executarComandoSQLSelect(self, sql, arguments=()):
		self.cursor.execute(sql, arguments)
		return self.cursor.fetchall()

	def salvarAlteracoes(self):
		self.conexao.commit()

	def fecharConexao(self):
		self.conexao.close()
