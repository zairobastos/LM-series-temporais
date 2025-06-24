import streamlit as st
from src.model.prompt_model import PromptModel, PromptType
from src.model.dados_model import DadosModel
from src.view.grafico import Grafico

class Prompt:
	def __init__(self, dataset:str, data_inicio:str, data_fim:str, qtd_periodos:int, tipo_prompt:PromptType, tipo_serie:str):
		"""
		Classe responsável por manipular o dataset.

		Args:
			dataset (str): Dataset a ser manipulado.
			data_inicio (str): Data de início do dataset.
			data_fim (str): Data de fim do dataset.
			qtd_periodos (int): Quantidade de períodos a serem previstos.
		"""
		self.dataset = dataset
		self.data_inicio = data_inicio
		self.data_fim = data_fim
		self.qtd_periodos = qtd_periodos
		self.tipo_prompt = tipo_prompt
		self.tipo_serie = tipo_serie

	def prompt(self):
		st.write('---')
		st.write('### Prompt')
		dataset = DadosModel(dataset=self.dataset, data_inicio=self.data_inicio, data_fim=self.data_fim, qtd_periodos=self.qtd_periodos)
		if self.tipo_serie == 'Numérica':
			lista_prompt, lista_exatos = dataset.dados_prompt()
		elif self.tipo_serie == 'Textual':
			lista_prompt, lista_promt2, lista_exatos = dataset.dados_prompt_str()
		prompt = PromptModel(lista_prompt=lista_prompt, tipo_prompt=self.tipo_prompt, tam_previsao=self.qtd_periodos).prompt()
		st.code(
			prompt,
			language='python',
			line_numbers=True,
		)
		if self.tipo_serie == 'Numérica':
			Grafico().amostragem(lista_prompt)
		elif self.tipo_serie == 'Textual':
			Grafico().amostragem(lista_promt2)
		return prompt, lista_exatos

