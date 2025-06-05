import pandas as pd 
from src.model.dados_model import DadosModel
from src.model.prompt_model import PromptModel

class PromptController:
  def __init__(self, dataset_prompt: str, data_inicio:str, data_fim:str):
    """Classe para manipulação de dados.

    Args:
      dataset (str): Caminho do arquivo CSV a ser manipulado.
      data_inicio (str): Data de início do dataset no formato 'YYYY-MM-DD'.
      data_fim (str): Data de fim do dataset no formato 'YYYY-MM-DD'.
    """
    self.dataset = dataset_prompt
    self.data_inicio = data_inicio
    self.data_fim = data_fim

  def prompt(self):
    """Gera o prompt para o modelo.

    Returns:
      str: Prompt gerado.
    """
    dados_model = DadosModel(self.dataset, self.data_inicio, self.data_fim)
    dados_prompt, dados_exatos = dados_model.dados_prompt()
    prompt_model = PromptModel(dados_prompt, 'ZERO-SHOT')
    prompt = prompt_model.prompt()
