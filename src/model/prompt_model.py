from typing import Literal
import permetrics

from prompts.zero_shot import ZERO_SHOT
""" from prompts.few_shot import FEW_SHOT
from prompts.cot import COT
from prompts.cot_few import COT_FEW """

class PromptModel:
  def __init__(self, lista_prompt: list[any], tipo_prompt: Literal['ZERO-SHOT', 'FEW-SHOT', 'COT', 'COT-FEW'], tam_previsao: int):
    """Classe para manipulação de dados.

    Args:
      dataset (str): Caminho do arquivo CSV a ser manipulado.
      tipo_prompt (str): Tipo de prompt a ser utilizado. Options: 'ZERO-SHOT', 'FEW-SHOT', 'COT', 'COT-FEW'.
      tam_previsao (int): Tamanho da previsão a ser realizada.
    """
    self.tam_periodos = len(lista_prompt)
    self.tipo_prompt = tipo_prompt
    self.lista_prompt = lista_prompt
    self.tam_previsao = tam_previsao
  def prompt(self):
    """Gera o prompt para o modelo.

    Returns:
      str: Prompt gerado.
    """
    if self.tipo_prompt == 'ZERO-SHOT':
      prompt = ZERO_SHOT.format(
        periodos= self.tam_periodos,
        inicio_previsao= self.lista_prompt[:4],
				saida= 24,
				exemplo_saida= self.lista_prompt[:24],
				dados_prompt= self.lista_prompt,
				n= self.tam_previsao*24,
      )
    elif self.tipo_prompt == 'FEW-SHOT':
      prompt = FEW_SHOT
    elif self.tipo_prompt == 'COT':
      prompt = COT
    elif self.tipo_prompt == 'COT-FEW':
      prompt = COT_FEW
    
    return prompt
""" 
teste = PromptModel([i for i in range(500)], 'ZERO-SHOT', 1)
print(teste.prompt()) """