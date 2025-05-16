from datetime import date
import pandas as pd

class DadosModel:
  def __init__(self, dataset: str, data_inicio:date, data_fim:date):
    """Classe para manipulação de dados.

    Args:
      dataset (pd.DataFrame): Dataset a ser manipulado.
      data_inicio (date): Data de início do dataset.
      data_fim (date): Data de fim do dataset.
    """
    self.dataset = dataset
    self.data_inicio = data_inicio
    self.data_fim = data_fim 

  def exibir_dados(self) -> pd.DataFrame:
    """Exibe os dados do dataset.

    Args:
      dados (DadosModel): Objeto da classe DadosModel.
    """
    try:
      dataset = pd.read_csv(self.dataset, sep=",", encoding="utf-8")
      return dataset
    except FileNotFoundError as e:
      print(f"[ERROR] Arquivo não encontrado: {e}")
      return None
    except pd.errors.EmptyDataError as e:
      print(f"[ERROR] Arquivo vazio: {e}")   
      return None

  def selecao_periodo(self) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Seleciona os dados do dataset entre as datas de início e fim. E retorna os valores exatos a serem previstos.

    Returns:
      tuple[pd.DataFrame, pd.DataFrame]: Dataframes com os dados entre as datas de início e fim e os dados exatos a serem previstos.
    """
    try:
      dataset = self.exibir_dados()
      if dataset.empty:
        raise ValueError("O dataset está vazio.")
      if self.data_inicio > self.data_fim:
        raise ValueError("A data de início não pode ser maior que a data de fim.")
      
      df = dataset.query(f"date >= '{self.data_inicio}' and date <= '{self.data_fim}'")
      df_exatos = dataset.query(f"date > '{self.data_fim}'")
      return df, df_exatos
    except ValueError as e:
      print(f"[ERROR] {e}")
      return None, None
    except Exception as e:
      print(f"[ERROR] Ocorreu um erro inesperado: {e}")
      return None, None
    
  def dados_prompt(self) -> tuple[list[float], list[float]]:
    """Retorna os dados do dataset em formato de lista.

    Returns:
      tuple[list[float], list[float]]: Dados do dataset em formato de lista.
    """
    try:
      dataset, df_exatos = self.selecao_periodo()
      if dataset is None or df_exatos is None:
        raise ValueError("Os dados não foram carregados corretamente.")
      if dataset.empty or df_exatos.empty:
        raise ValueError("Os dados estão vazios.")
        
      print(f"[INFO] Dados entre {self.data_inicio} e {self.data_fim} carregados com sucesso.")
      dados_prompt = dataset['OT'].to_list()
      dados_prompt = [round(i, 3) for i in dados_prompt]

      dados_exatos = df_exatos['OT'].to_list()
      dados_exatos = [round(i, 3) for i in dados_exatos]
      return dados_prompt, dados_exatos
    except ValueError as e:
      print(f"[ERROR] {e}")
      return None, None
    except Exception as e:
      print(f"[ERROR] Ocorreu um erro inesperado: {e}")
      return None, None