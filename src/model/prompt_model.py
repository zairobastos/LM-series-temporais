from typing import Any, List, Literal
from enum import Enum

from src.prompts.zero_shot import ZERO_SHOT
from src.prompts.cot import COT
from src.prompts.few_shot import FEW_SHOT
from src.prompts.cot_few import COT_FEW

class PromptType(str, Enum):
	ZERO_SHOT = 'ZERO_SHOT'
	FEW_SHOT = 'FEW_SHOT'
	COT = 'COT'
	COT_FEW = 'COT_FEW'

class PromptModel:
	def __init__(self, lista_prompt: List[Any], tipo_prompt: PromptType, tam_previsao: int):
		"""
		Classe responsável por gerar prompts com base em um tipo definido.

		Args:
			lista_prompt (List[Any]): Lista com dados de entrada.
			tipo_prompt (PromptType): Tipo de prompt a ser utilizado.
			tam_previsao (int): Número de dias a serem previstos.
		"""
			
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
			"saida": self.tam_previsao,
			"exemplo_saida": self.lista_prompt[:24],
			"dados_prompt": self.lista_prompt,
			"n": self.tam_previsao,
		}

		if self.tipo_prompt == PromptType.ZERO_SHOT:
			print(f"[INFO] Prompt ZERO-SHOT gerado com {self.tam_periodos} períodos.")
			return ZERO_SHOT.format(**base_kwargs)

		elif self.tipo_prompt == PromptType.FEW_SHOT or self.tipo_prompt == PromptType.COT_FEW:
			print(f"[INFO] Prompt FEW-SHOT ou COT-FEW gerado com {self.tam_periodos} períodos.")
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
			print(f"[INFO] Prompt COT gerado com {self.tam_periodos} períodos.")
			return COT.format(**base_kwargs)

		else:
			raise ValueError(f"Tipo de prompt inválido: {self.tipo_prompt}")