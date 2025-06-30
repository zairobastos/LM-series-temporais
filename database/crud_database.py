import sqlite3

class Crud:
	def __init__(self):
		self.connection = sqlite3.connect('./database/database.db')
		self.cursor = self.connection.cursor()

	def insert(self, **kwargs) -> bool:
		"""Inserir dados na tabela especificada.
		Args:
			table (str): Nome da tabela onde os dados serão inseridos.
			**kwargs: Dados a serem inseridos na tabela.

		Returns:
			bool: True se a inserção for bem-sucedida, False caso contrário.
		"""
		try:
			valores_para_inserir = (
				kwargs.get('data_inicio'),
				kwargs.get('data_fim'),
				kwargs.get('periodos'),
				kwargs.get('modelo'),
				kwargs.get('temperatura_modelo'),
				kwargs.get('prompt'),
				kwargs.get('tipo_prompt'),
				kwargs.get('valores_exatos'),
				kwargs.get('valores_previstos'),
				kwargs.get('smape'),
				kwargs.get('mae'),
				kwargs.get('rmse'),
				kwargs.get('total_tokens_resposta'),
				kwargs.get('total_tokens_prompt'),
				kwargs.get('total_tokens'),
				kwargs.get('base_dados')
			)
			self.cursor.execute(
				f"""
				INSERT INTO llm4time (
					data_inicio,
					data_fim,
					periodos,
					modelo,
					temperatura_modelo,
					prompt,
					tipo_prompt,
					valores_exatos,
					valores_previstos,
					smape,
					mae,
					rmse,
					total_tokens_resposta,
					total_tokens_prompt,
					total_tokens,
					base_dados
				) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", valores_para_inserir
			)
			self.connection.commit()
			print(f"[INFO] Dados inseridos com sucesso na tabela llm4time.")
		except sqlite3.Error as e:
			print(f"[ERROR] Erro ao inserir dados na tabela llm4time: {e}")
			return False
		finally:
			print("[INFO] Fechando conexão com o banco de dados.")
			self.connection.close()
			return True

	def insert_dataset(self, table: str, col_data: str, col_valor: str) -> bool:
		"""Inserir dados na tabela de dataset.
			Args:
				table (str): Nome da tabela onde os dados serão inseridos.
				col_data (str): Nome da coluna de data.
				col_valor (str): Nome da coluna de valor.

			Returns:
				bool: True se a inserção for bem-sucedida, False caso contrário.
			"""
		try:
			self.cursor.execute(
				"""
				INSERT INTO dataset(
					nome_dataset,
					coluna_data,
					coluna_valor
				) VALUES (?, ?, ?)""", (table, col_data, col_valor)
			)
			self.connection.commit()
			print(f"[INFO] Dados inseridos com sucesso na tabela {table}.")
			return True
		except sqlite3.Error as e:
			print(f"[ERROR] Erro ao inserir dados na tabela {table}: {e}")
			return False
		finally:
			print("[INFO] Fechando conexão com o banco de dados.")
			self.connection.close()
		

	def select(self, table: str, tipo_prompt: list[str]) -> list:
		"""
		Seleciona dados da tabela 'llm4time' com base na base_dados e na lista de tipo_prompt.

		Args:
			table (str): Nome da base de dados (base_dados).
			tipo_prompt (list[str]): Lista de tipos de prompt a serem filtrados.

		Returns:
			list: Lista de tuplas com os dados selecionados.
		"""
		try:
			placeholders = ','.join(['?'] * len(tipo_prompt))
			query = f"SELECT * FROM llm4time WHERE base_dados = ? AND tipo_prompt IN ({placeholders})"
			
			# Junta o valor da base com a lista de tipos
			params = [table] + tipo_prompt
			
			self.cursor.execute(query, params)
			rows = self.cursor.fetchall()
			return rows
		except sqlite3.Error as e:
			print(f"[ERROR] Erro ao selecionar dados da tabela llm4time: {e}")
			return []
		finally:
			print("[INFO] Fechando conexão com o banco de dados.")
			self.connection.close()
