import sqlite3

class Crud:
  def __init__(self):
    self.connection = sqlite3.connect('database.db')
    self.cursor = self.connection.cursor()

  def insert(self, table: str, **kwargs) -> bool:
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
        kwargs.get('horas'),
        kwargs.get('modelo'),
        kwargs.get('temperatura_modelo'),
        kwargs.get('prompt'),
        kwargs.get('tipo_prompt'),
        kwargs.get('valores_exatos'),
        kwargs.get('valores_previstos'),
        kwargs.get('smape'),
        kwargs.get('top_k'),
        kwargs.get('max_tokens'),
        kwargs.get('total_tokens_saida'),
        kwargs.get('total_tokens_entrada'),
        kwargs.get('total_tokens')
      )
      self.cursor.execute(
        f"""
        INSERT INTO  {table}(
          data_inicio,
          data_fim,
          horas,
          modelo,
          temperatura_modelo,
          prompt,
          tipo_prompt,
          valores_exatos,
          valores_previstos,
          smape,
          top_k,
          max_tokens,
          total_tokens_saida,
          total_tokens_entrada,
          total_tokens
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
      )
      self.connection.commit()
      print("[INFO] Dados inseridos com sucesso na tabela {table}.")
      return True
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao inserir dados na tabela {table}: {e}")
      return False
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()

  def select(self, table: str, **kwargs) -> list:
    """Selecionar dados da tabela especificada.
    Args:
      table (str): Nome da tabela de onde os dados serão selecionados.
      **kwargs: Condições para a seleção dos dados.

    Returns:
      list: Lista de tuplas com os dados selecionados.
    """
    try:
      query = f"SELECT * FROM {table}"
      self.cursor.execute(query)
      rows = self.cursor.fetchall()
      return rows
    except sqlite3.Error as e:
      print(f"[ERROR] Erro ao selecionar dados da tabela {table}: {e}")
      return []
    finally:
      print("[INFO] Fechando conexão com o banco de dados.")
      self.connection.close()