from typing import Any, List, Literal
from enum import Enum

from prompts.zero_shot import ZERO_SHOT
from prompts.cot import COT
from prompts.few_shot import FEW_SHOT
from prompts.cot_few import COT_FEW

class PromptType(str, Enum):
	ZERO_SHOT = 'ZERO-SHOT'
	FEW_SHOT = 'FEW-SHOT'
	COT = 'COT'
	COT_FEW = 'COT-FEW'

class PromptModel:
	HORAS_DIA = 24

	def __init__(self, lista_prompt: List[Any], tipo_prompt: PromptType, tam_previsao: int):
		"""
		Classe responsável por gerar prompts com base em um tipo definido.

		Args:
			lista_prompt (List[Any]): Lista com dados de entrada.
			tipo_prompt (PromptType): Tipo de prompt a ser utilizado.
			tam_previsao (int): Número de dias a serem previstos.
		"""
		if not isinstance(lista_prompt, list) or len(lista_prompt) == 0:
			raise ValueError("lista_prompt deve ser uma lista não vazia.")
			
		if not isinstance(tam_previsao, int) or tam_previsao <= 0:
			raise ValueError("tam_previsao deve ser um inteiro positivo.")
			
		self.lista_prompt = lista_prompt
		self.tipo_prompt = tipo_prompt
		self.tam_periodos = len(lista_prompt)
		self.tam_previsao = tam_previsao

	def prompt(self) -> str:
		"""
		Gera o prompt formatado com base no tipo escolhido.

		Returns:
			str: Prompt formatado para entrada no modelo.
		"""
		base_kwargs = {
			"periodos": self.tam_periodos,
			"inicio_previsao": self.lista_prompt[:4],
			"saida": self.HORAS_DIA,
			"exemplo_saida": self.lista_prompt[:24],
			"dados_prompt": self.lista_prompt,
			"n": self.tam_previsao * self.HORAS_DIA,
		}

		if self.tipo_prompt == PromptType.ZERO_SHOT:
			return ZERO_SHOT.format(**base_kwargs)

		elif self.tipo_prompt == PromptType.FEW_SHOT or self.tipo_prompt == PromptType.COT_FEW:
			# Verificação se há dados suficientes
			if len(self.lista_prompt) < 96:
				raise ValueError("Para FEW-SHOT ou COT-FEW, lista_prompt deve conter pelo menos 96 elementos.")
				
			exemplos = {
				"periodo1": self.lista_prompt[:24],
				"periodo2": self.lista_prompt[24:48],
				"periodo3": self.lista_prompt[48:72],
				"periodo4": self.lista_prompt[72:96],
			}
			base_kwargs.update(exemplos)

			if self.tipo_prompt == PromptType.FEW_SHOT:
				return FEW_SHOT.format(**base_kwargs)
			else:
				return COT_FEW.format(**base_kwargs)

		elif self.tipo_prompt == PromptType.COT:
			return COT.format(**base_kwargs)

		else:
			raise ValueError(f"Tipo de prompt inválido: {self.tipo_prompt}")

teste = PromptModel([i for i in range(100)], PromptType.COT, 1)
print(teste.prompt())