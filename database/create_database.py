import sqlite3
from contextlib import closing
from sqlite3 import Cursor, Connection
from schema_tables import TABLE_SCHEMA_ETTH, TABLE_SCHEMA_DATASET


def create_table(cursor: Cursor, table_name: str) -> None:
	"""
	Cria uma tabela no banco de dados com o nome especificado, utilizando o schema definido.

	Args:
		cursor (Cursor): Cursor do banco de dados.
		table_name (str): Nome da tabela a ser criada.
	"""
	try:
		print(f"[INFO] Criando a tabela '{table_name}'...")
		if table_name == 'dataset':
			cursor.execute(TABLE_SCHEMA_DATASET.format(table_name=table_name))
		else:
			cursor.execute(TABLE_SCHEMA_ETTH.format(table_name=table_name))
		print(f"[SUCCESS] Tabela '{table_name}' criada com sucesso.")
	except sqlite3.Error as e:
		print(f"[ERROR] Falha ao criar a tabela '{table_name}': {e}")
		raise


def create_database(db_path: str = './database/database.db') -> None:
	"""
	Cria um banco de dados SQLite e as suas tabelas definidas no schema.

	Args:
		db_path (str, optional): Caminho do arquivo do banco de dados. Defaults to './database/database.py''.
	"""
	print(f"[INFO] Inicializando criação do banco de dados em '{db_path}'...")
	try:
		with closing(sqlite3.connect(db_path)) as conn:
			with closing(conn.cursor()) as cursor:
				for table in ['etth1', 'etth2', 'dataset']:
					create_table(cursor, table)
			conn.commit()
		print("[SUCCESS] Banco de dados e tabelas criados com sucesso.")
	except sqlite3.Error as e:
		print(f"[ERROR] Falha ao criar o banco de dados: {e}")
		raise


if __name__ == "__main__":
	print("[DEBUG] Schema da tabela:")
	create_database()
